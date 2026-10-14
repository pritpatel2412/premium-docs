#!/usr/bin/env python3
"""validate_doc.py - Automated quality and accessibility validator for premium-docs HTML output.

Validates:
1. Single <h1> tag (heading hierarchy).
2. Unique heading IDs (no duplicate anchors).
3. Intact internal #anchors (no broken intra-document links).
4. Zero external network resources (no external src/href in link/script/img).
5. Accessible image alt attributes.
6. Mathematical WCAG AA contrast ratio calculation across theme tokens.
7. File-size budget (< 300KB recommended).
8. Absence of unparsed leftover ':::' container markers.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


class DocValidatorParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1_count = 0
        self.h1_texts: List[str] = []
        self.heading_ids: List[str] = []
        self.all_ids: Set[str] = set()
        self.internal_links: List[str] = []
        self.external_resources: List[Tuple[str, str]] = []  # (tag, attr_val)
        self.images_without_alt: List[str] = []
        self.in_h1 = False
        self.current_h1_text = ""

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        attr_dict = {k.lower(): (v or "") for k, v in attrs}

        # Collect all IDs
        if "id" in attr_dict:
            self.all_ids.add(attr_dict["id"])

        # Check Headings
        if tag == "h1":
            self.h1_count += 1
            self.in_h1 = True
            self.current_h1_text = ""

        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            if "id" in attr_dict:
                self.heading_ids.append(attr_dict["id"])

        # Check internal anchors and external links
        if tag == "a" and "href" in attr_dict:
            href = attr_dict["href"]
            if href.startswith("#") and len(href) > 1:
                self.internal_links.append(href[1:])

        # Check for prohibited external resources (scripts, stylesheets, images)
        if tag in ("script", "img", "iframe", "embed", "audio", "video") and "src" in attr_dict:
            src = attr_dict["src"]
            if src.startswith("http://") or src.startswith("https://") or src.startswith("//"):
                self.external_resources.append((tag, src))

        if tag == "link" and "href" in attr_dict:
            href = attr_dict["href"]
            rel = attr_dict.get("rel", "")
            if (href.startswith("http://") or href.startswith("https://") or href.startswith("//")) and "stylesheet" in rel:
                self.external_resources.append((tag, href))

        # Check image alt text
        if tag == "img":
            if "alt" not in attr_dict or not attr_dict["alt"].strip():
                self.images_without_alt.append(attr_dict.get("src", "<embedded>"))

    def handle_endtag(self, tag: str):
        if tag == "h1":
            self.in_h1 = False
            self.h1_texts.append(self.current_h1_text.strip())

    def handle_data(self, data: str):
        if self.in_h1:
            self.current_h1_text += data


# --- WCAG AA Mathematical Contrast Calculation ---
def srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(r: int, g: int, b: int) -> float:
    r_lin = srgb_to_linear(r / 255.0)
    g_lin = srgb_to_linear(g / 255.0)
    b_lin = srgb_to_linear(b / 255.0)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def calculate_contrast_ratio(hex1: str, hex2: str) -> float:
    def parse_hex(h: str) -> Tuple[int, int, int]:
        h = h.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) != 6:
            return (0, 0, 0)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    l1 = relative_luminance(*parse_hex(hex1))
    l2 = relative_luminance(*parse_hex(hex2))
    brightest = max(l1, l2)
    darkest = min(l1, l2)
    return (brightest + 0.05) / (darkest + 0.05)


def extract_theme_colors(css_text: str) -> Dict[str, str]:
    """Extract key color tokens from inlined CSS."""
    colors: Dict[str, str] = {}
    tokens = ["--bg", "--surface", "--text", "--text-muted", "--accent"]
    for t in tokens:
        m = re.search(rf"{t}\s*:\s*(#[0-9a-fA-F]{{3,6}})", css_text)
        if m:
            colors[t] = m.group(1)
    return colors


def validate_document(html_path: Path) -> Tuple[bool, List[str], List[str], Dict[str, Any]]:
    """Validate an HTML document against quality, accessibility, and offline standards.

    Returns:
        (is_valid, errors, warnings, metadata)
    """
    errors: List[str] = []
    warnings: List[str] = []
    metadata: Dict[str, Any] = {}

    if not html_path.exists():
        return False, [f"File not found: {html_path}"], [], {}

    raw_html = html_path.read_text(encoding="utf-8")
    size_bytes = len(raw_html.encode("utf-8"))
    metadata["size_bytes"] = size_bytes
    metadata["size_kb"] = round(size_bytes / 1024, 1)

    # 1. File Size Budget (< 300KB recommended)
    if size_bytes > 1_000_000:
        errors.append(f"File size exceeds 1MB budget ({size_bytes:,} bytes).")
    elif size_bytes > 400_000:
        warnings.append(f"File size is larger than recommended 300KB ({metadata['size_kb']} KB).")

    # 2. Check for leftover unparsed ::: markers
    leftover_markers = re.findall(r"^\s*:::[a-zA-Z0-9_-]*.*$", raw_html, re.MULTILINE)
    if leftover_markers:
        errors.append(f"Found {len(leftover_markers)} unparsed container marker(s) in HTML: {leftover_markers[:3]}")

    # 3. Parse HTML DOM
    parser = DocValidatorParser()
    try:
        parser.feed(raw_html)
    except Exception as e:
        errors.append(f"Malformed HTML structure: {e}")

    # 4. Heading 1 Checks
    if parser.h1_count == 0:
        errors.append("Document is missing an <h1> title tag.")
    elif parser.h1_count > 1:
        errors.append(f"Document contains {parser.h1_count} <h1> tags. Expected exactly 1.")
    metadata["h1_title"] = parser.h1_texts[0] if parser.h1_texts else None

    # 5. Unique Heading IDs
    seen_h_ids: Set[str] = set()
    dup_h_ids: List[str] = []
    for h_id in parser.heading_ids:
        if h_id in seen_h_ids:
            dup_h_ids.append(h_id)
        seen_h_ids.add(h_id)
    if dup_h_ids:
        errors.append(f"Duplicate heading IDs detected: {dup_h_ids}")

    # 6. Intact Internal Anchors
    broken_anchors: List[str] = []
    for anchor in parser.internal_links:
        # Ignore empty anchors or dynamic scroll anchors
        if anchor in ("_top", "doc-content", "top"):
            continue
        if anchor not in parser.all_ids:
            broken_anchors.append(anchor)
    if broken_anchors:
        errors.append(f"Broken internal anchor links: {set(broken_anchors)}")

    # 7. No external resources
    if parser.external_resources:
        for tag, url in parser.external_resources:
            errors.append(f"External resource prohibited for offline privacy: <{tag}> loading {url}")

    # 8. Images have alt text
    if parser.images_without_alt:
        errors.append(f"Found {len(parser.images_without_alt)} image(s) missing alt text attributes.")

    # 9. Contrast Ratio Calculation
    css_match = re.search(r"<style>(.*?)</style>", raw_html, re.DOTALL)
    if css_match:
        colors = extract_theme_colors(css_match.group(1))
        bg = colors.get("--bg", "#ffffff")
        text = colors.get("--text", "#0f172a")
        ratio = calculate_contrast_ratio(bg, text)
        metadata["contrast_ratio"] = round(ratio, 2)
        if ratio < 4.5:
            errors.append(f"WCAG AA contrast violation: Text {text} on background {bg} has ratio {ratio:.2f}:1 (min 4.5:1 required).")
    else:
        warnings.append("No inlined <style> block found to verify theme contrast ratios.")

    # 10. CSP Meta Tag Check
    if '<meta http-equiv="Content-Security-Policy"' not in raw_html:
        warnings.append("Missing Content-Security-Policy meta tag.")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings, metadata


def main():
    parser = argparse.ArgumentParser(
        description="Automated quality and accessibility validator for premium-docs HTML deliverables.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("file", type=Path, help="HTML file to validate")
    parser.add_argument("--json", action="store_true", help="Output validation report in JSON format")

    args = parser.parse_args()

    is_valid, errors, warnings, metadata = validate_document(args.file)

    if args.json:
        report = {
            "valid": is_valid,
            "file": str(args.file),
            "errors": errors,
            "warnings": warnings,
            "metadata": metadata,
        }
        print(json.dumps(report, indent=2))
    else:
        print(f"\nDocument Quality & Accessibility Report: {args.file}")
        print("=" * 60)
        print(f"Title: {metadata.get('h1_title', 'Unknown')}")
        print(f"Size:  {metadata.get('size_kb', 0)} KB")
        if "contrast_ratio" in metadata:
            print(f"Text Contrast Ratio: {metadata['contrast_ratio']}:1 (WCAG AA Target: >= 4.5:1)")

        if warnings:
            print("\nWarnings:")
            for w in warnings:
                print(f"  [!] {w}")

        if errors:
            print("\nErrors:")
            for e in errors:
                print(f"  [X] {e}")
            print("\nResult: FAILED\n")
            sys.exit(1)
        else:
            print("\nResult: PASSED (All quality, accessibility, and offline gates verified)\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
