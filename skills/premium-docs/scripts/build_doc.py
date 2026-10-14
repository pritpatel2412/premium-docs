#!/usr/bin/env python3
"""build_doc.py - Standalone HTML compiler for premium-docs.

Converts Lean Markdown + YAML frontmatter + Docusaurus-style container blocks
into a single, self-contained, publication-grade HTML document with zero external dependencies.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Dependency check: markdown
try:
    import markdown
except ImportError:
    print(
        "Error: 'markdown' package is required for Markdown parsing.\n"
        "Install it with: pip install markdown",
        file=sys.stderr,
    )
    sys.exit(1)

# Optional dependency: Pygments
try:
    import pygments
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.formatters import HtmlFormatter
    HAS_PYGMENTS = True
except ImportError:
    HAS_PYGMENTS = False

# Optional dependency: PyYAML
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def find_assets_dir() -> Path:
    """Find the assets directory relative to this script or installed skill."""
    script_dir = Path(__file__).resolve().parent
    # Standard location: skills/premium-docs/assets/
    candidate1 = script_dir.parent / "assets"
    if candidate1.is_dir():
        return candidate1
    # Fallback: check workspace or parent directory
    candidate2 = script_dir / "assets"
    if candidate2.is_dir():
        return candidate2
    candidate3 = Path.cwd() / "skills" / "premium-docs" / "assets"
    if candidate3.is_dir():
        return candidate3
    raise FileNotFoundError(f"Could not locate 'assets' directory. Checked: {candidate1}, {candidate2}, {candidate3}")


# --- YAML Frontmatter Parser ---
def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    """Parse YAML frontmatter at the beginning of the file."""
    if not text.startswith("---"):
        return {}, text

    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text

    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx == -1:
        return {}, text

    fm_text = "".join(lines[1:end_idx])
    body_text = "".join(lines[end_idx + 1:])

    data: Dict[str, Any] = {}
    if HAS_YAML:
        try:
            loaded = yaml.safe_load(fm_text)
            if isinstance(loaded, dict):
                data = loaded
        except Exception as e:
            print(f"Warning: Failed to parse YAML frontmatter: {e}", file=sys.stderr)
    else:
        # Simple stdlib regex fallback for key: value
        for line in fm_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if v.lower() == "true":
                    data[k] = True
                elif v.lower() == "false":
                    data[k] = False
                elif v.startswith("[") and v.endswith("]"):
                    items = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
                    data[k] = items
                else:
                    data[k] = v

    return data, body_text


# --- Color Utilities for Accent Derivation ---
def hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    hex_code = hex_code.lstrip("#")
    if len(hex_code) == 3:
        hex_code = "".join(c * 2 for c in hex_code)
    if len(hex_code) != 6:
        return (99, 102, 241)  # Default indigo
    return (int(hex_code[0:2], 16), int(hex_code[2:4], 16), int(hex_code[4:6], 16))


def derive_accent_css(accent_hex: str) -> str:
    """Generate dynamic CSS variable overrides from a custom hex accent."""
    r, g, b = hex_to_rgb(accent_hex)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    fg_color = "#000000" if luminance > 0.6 else "#ffffff"

    # Hover color: slightly darker or lighter
    hover_r = max(0, int(r * 0.85))
    hover_g = max(0, int(g * 0.85))
    hover_b = max(0, int(b * 0.85))
    hover_hex = f"#{hover_r:02x}{hover_g:02x}{hover_b:02x}"

    return f"""
/* Custom Accent Override */
:root {{
  --accent: {accent_hex};
  --accent-hover: {hover_hex};
  --accent-soft: rgba({r}, {g}, {b}, 0.08);
  --accent-border: rgba({r}, {g}, {b}, 0.25);
  --accent-fg: {fg_color};
  --hero-gradient: linear-gradient(135deg, rgba({r}, {g}, {b}, 0.08) 0%, rgba({r}, {g}, {b}, 0.02) 100%);
  --hero-border: rgba({r}, {g}, {b}, 0.2);
}}
"""


# --- Container Parser (AST Stack) ---
class ContainerNode:
    def __init__(self, c_type: str, title: str, start_line: int):
        self.c_type = c_type.lower()
        self.title = title
        self.start_line = start_line
        self.lines: List[str] = []

    def add_line(self, line: str):
        self.lines.append(line)


def parse_containers(text: str) -> str:
    """Preprocess Docusaurus-style container blocks `:::type [Title]` ... `:::` with nesting support."""
    lines = text.splitlines()
    output_lines: List[str] = []

    # Stack holds tuples of (ContainerNode, child_lines)
    stack: List[ContainerNode] = []

    open_pattern = re.compile(r"^\s*:::([a-zA-Z0-9_-]+)(?:\s+(.*))?$")
    close_pattern = re.compile(r"^\s*:::\s*$")

    for line_num, line in enumerate(lines, start=1):
        # Check for open container
        m_open = open_pattern.match(line)
        # Check for close container
        m_close = close_pattern.match(line)

        if m_close and not m_open:
            if not stack:
                raise SyntaxError(f"Line {line_num}: Unexpected closing ':::' with no matching opening container.")
            closed_node = stack.pop()
            rendered = render_container(closed_node)
            if stack:
                stack[-1].lines.append(rendered)
            else:
                output_lines.append(rendered)
            continue

        if m_open:
            c_type = m_open.group(1)
            c_title = m_open.group(2) or ""
            node = ContainerNode(c_type, c_title, line_num)
            stack.append(node)
            continue

        if stack:
            stack[-1].add_line(line)
        else:
            output_lines.append(line)

    if stack:
        unclosed = stack[-1]
        raise SyntaxError(
            f"Line {unclosed.start_line}: Unclosed container ':::{unclosed.c_type}' "
            f"(opened with title '{unclosed.title}'). Missing closing ':::'."
        )

    return "\n".join(output_lines)


def render_container(node: ContainerNode) -> str:
    """Render a container node to clean, accessible HTML."""
    c_type = node.c_type
    raw_content = "\n".join(node.lines)
    # Recursively resolve any child containers that might be nested
    parsed_inner = parse_containers(raw_content)

    # 1. Standard Callouts (note, tip, info, success, warning, danger)
    if c_type in ("note", "tip", "info", "success", "warning", "danger"):
        icons = {
            "note": "file-text",
            "tip": "lightbulb",
            "info": "info",
            "success": "check-circle",
            "warning": "alert-triangle",
            "danger": "x-circle",
        }
        icon_name = icons.get(c_type, "info")
        title = node.title.strip() or c_type.capitalize()
        # Convert inner markdown to HTML
        inner_html = markdown.markdown(parsed_inner, extensions=["tables", "fenced_code"])
        return f"""
<div class="callout callout-{c_type}" role="region" aria-label="{html.escape(title)}">
  <div class="callout-header">
    <svg class="callout-icon" aria-hidden="true"><use href="#icon-{icon_name}"></use></svg>
    <span class="callout-title">{html.escape(title)}</span>
  </div>
  <div class="callout-body">
    {inner_html}
  </div>
</div>
"""

    # 2. TL;DR (Executive Summary)
    if c_type == "tldr":
        title = node.title.strip() or "Executive Summary"
        inner_html = markdown.markdown(parsed_inner, extensions=["tables", "fenced_code"])
        return f"""
<div class="tldr-box" role="region" aria-label="{html.escape(title)}">
  <div class="tldr-header">
    <svg class="tldr-icon" aria-hidden="true"><use href="#icon-zap"></use></svg>
    <span>{html.escape(title)}</span>
  </div>
  <div class="tldr-body">
    {inner_html}
  </div>
</div>
"""

    # 3. Cards Grid (children separated by ---)
    if c_type == "cards":
        card_chunks = re.split(r"\n\s*---\s*\n", parsed_inner)
        cards_html: List[str] = []
        for chunk in card_chunks:
            chunk = chunk.strip()
            if not chunk:
                continue
            card_title = ""
            # Check for leading ### Title
            m_title = re.match(r"^###\s+(.*?)(?:\n|$)", chunk)
            if m_title:
                card_title = m_title.group(1).strip()
                chunk = chunk[m_title.end():].strip()

            body_html = markdown.markdown(chunk, extensions=["tables", "fenced_code"])
            title_html = f'<div class="card-title">{html.escape(card_title)}</div>' if card_title else ""
            cards_html.append(f"""
<div class="card-item">
  {title_html}
  <div class="card-body">
    {body_html}
  </div>
</div>
""")
        return f'<div class="cards-grid">{"".join(cards_html)}</div>'

    # 4. Stats Tiles (lines: value | label | delta)
    if c_type == "stats":
        tiles_html: List[str] = []
        for line in parsed_inner.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if not parts:
                continue
            value = parts[0]
            label = parts[1] if len(parts) > 1 else ""
            delta = parts[2] if len(parts) > 2 else ""

            delta_html = ""
            if delta:
                delta_cls = "neutral"
                delta_icon = "activity"
                if delta.startswith("+") or "up" in delta.lower():
                    delta_cls = "positive"
                    delta_icon = "trending-up"
                elif delta.startswith("-") or "down" in delta.lower():
                    delta_cls = "negative"
                    delta_icon = "trending-down"
                delta_html = f"""
<div class="stat-delta {delta_cls}">
  <svg aria-hidden="true"><use href="#icon-{delta_icon}"></use></svg>
  <span>{html.escape(delta)}</span>
</div>"""

            tiles_html.append(f"""
<div class="stat-tile">
  <div class="stat-value">{html.escape(value)}</div>
  <div class="stat-label">{html.escape(label)}</div>
  {delta_html}
</div>
""")
        return f'<div class="stats-grid">{"".join(tiles_html)}</div>'

    # 5. Steps Process
    if c_type == "steps":
        step_chunks = re.split(r"\n(?=###|\d+\.)", parsed_inner)
        steps_html: List[str] = []
        step_num = 1
        for chunk in step_chunks:
            chunk = chunk.strip()
            if not chunk:
                continue
            step_title = ""
            m = re.match(r"^(?:###\s+|\d+\.\s+)(.*?)(?:\n|$)", chunk)
            if m:
                step_title = m.group(1).strip()
                chunk = chunk[m.end():].strip()
            else:
                step_title = f"Step {step_num}"

            body_html = markdown.markdown(chunk, extensions=["tables", "fenced_code"])
            steps_html.append(f"""
<div class="step-item">
  <div class="step-badge">{step_num}</div>
  <div class="step-content">
    <div class="step-title">{html.escape(step_title)}</div>
    <div class="step-body">{body_html}</div>
  </div>
</div>
""")
            step_num += 1
        return f'<div class="steps-container">{"".join(steps_html)}</div>'

    # 6. Accessible Tabs (@tab Tab Name)
    if c_type == "tabs":
        tab_chunks = re.split(r"\n(?=@tab\s+)", "\n" + parsed_inner)
        tab_buttons: List[str] = []
        tab_panels: List[str] = []
        idx = 0
        for chunk in tab_chunks:
            chunk = chunk.strip()
            if not chunk or not chunk.startswith("@tab"):
                continue
            m = re.match(r"^@tab\s+(.*?)(?:\n|$)", chunk)
            tab_name = m.group(1).strip() if m else f"Tab {idx + 1}"
            tab_content = chunk[m.end():].strip() if m else ""

            is_first = (idx == 0)
            aria_selected = "true" if is_first else "false"
            hidden_attr = "" if is_first else "hidden"
            tab_id = f"tab-btn-{idx + 1}"
            panel_id = f"tab-panel-{idx + 1}"

            tab_buttons.append(
                f'<button class="tab-button" role="tab" id="{tab_id}" aria-controls="{panel_id}" '
                f'aria-selected="{aria_selected}" tabindex="{0 if is_first else -1}">{html.escape(tab_name)}</button>'
            )
            body_html = markdown.markdown(tab_content, extensions=["tables", "fenced_code"])
            tab_panels.append(
                f'<div class="tab-panel" role="tabpanel" id="{panel_id}" aria-labelledby="{tab_id}" {hidden_attr}>'
                f"{body_html}</div>"
            )
            idx += 1

        return f"""
<div class="tabs-container">
  <div class="tab-list" role="tablist">{"".join(tab_buttons)}</div>
  {"".join(tab_panels)}
</div>
"""

    # 7. Compare Grid (Pros/Cons or A vs B)
    if c_type == "compare":
        cols = re.split(r"\n\s*---\s*\n", parsed_inner)
        cols_html: List[str] = []
        for chunk in cols:
            chunk = chunk.strip()
            if not chunk:
                continue
            col_class = "compare-col-neutral"
            col_icon = "layers"
            title = ""

            m_title = re.match(r"^###\s+(.*?)(?:\n|$)", chunk)
            if m_title:
                title = m_title.group(1).strip()
                chunk = chunk[m_title.end():].strip()

            lower_title = title.lower()
            if any(w in lower_title for w in ("pro", "advantage", "strength", "good", "recommended")):
                col_class = "compare-col-pro"
                col_icon = "check-circle"
            elif any(w in lower_title for w in ("con", "disadvantage", "drawback", "limitation", "bad")):
                col_class = "compare-col-con"
                col_icon = "x-circle"

            body_html = markdown.markdown(chunk, extensions=["tables", "fenced_code"])
            cols_html.append(f"""
<div class="compare-col {col_class}">
  <div class="compare-title">
    <svg style="width:18px;height:18px;" aria-hidden="true"><use href="#icon-{col_icon}"></use></svg>
    <span>{html.escape(title)}</span>
  </div>
  <div class="compare-body">
    {body_html}
  </div>
</div>
""")
        return f'<div class="compare-grid">{"".join(cols_html)}</div>'

    # 8. FAQ Accordion
    if c_type == "faq":
        items = re.split(r"\n(?=###\s+)", parsed_inner)
        faq_html: List[str] = []
        for item in items:
            item = item.strip()
            if not item:
                continue
            m = re.match(r"^###\s+(.*?)(?:\n|$)", item)
            question = m.group(1).strip() if m else "Question"
            answer_text = item[m.end():].strip() if m else item
            answer_html = markdown.markdown(answer_text, extensions=["tables", "fenced_code"])
            faq_html.append(f"""
<details class="faq-item">
  <summary class="faq-summary">
    <span>{html.escape(question)}</span>
    <svg class="faq-chevron" aria-hidden="true"><use href="#icon-chevron-right"></use></svg>
  </summary>
  <div class="faq-content">
    {answer_html}
  </div>
</details>
""")
        return f'<div class="faq-list">{"".join(faq_html)}</div>'

    # 9. File Tree
    if c_type == "filetree":
        tree_lines: List[str] = []
        for line in parsed_inner.splitlines():
            if not line.strip():
                continue
            indent_count = len(line) - len(line.lstrip(" "))
            indent_spaces = "&nbsp;" * indent_count
            trimmed = line.strip()

            comment = ""
            if "#" in trimmed:
                parts = trimmed.split("#", 1)
                trimmed = parts[0].strip()
                comment = f'<span class="filetree-comment"># {html.escape(parts[1].strip())}</span>'

            is_folder = trimmed.endswith("/") or trimmed.endswith("\\")
            icon = "folder" if is_folder else "file"
            line_cls = "folder" if is_folder else "file"

            tree_lines.append(
                f'<div class="filetree-line {line_cls}">{indent_spaces}<svg aria-hidden="true">'
                f'<use href="#icon-{icon}"></use></svg> {html.escape(trimmed)} {comment}</div>'
            )
        return f'<div class="filetree-container">{"".join(tree_lines)}</div>'

    # 10. Key-Value Grid (lines: Key | Value)
    if c_type == "kv":
        kv_items: List[str] = []
        for line in parsed_inner.splitlines():
            line = line.strip()
            if not line or "|" not in line:
                continue
            k, v = [p.strip() for p in line.split("|", 1)]
            kv_items.append(
                f'<div class="kv-item"><span class="kv-key">{html.escape(k)}</span>'
                f'<span class="kv-value">{html.escape(v)}</span></div>'
            )
        return f'<div class="kv-grid">{"".join(kv_items)}</div>'

    # 11. Progress Bars (lines: Label | 75%)
    if c_type == "progress":
        prog_items: List[str] = []
        for line in parsed_inner.splitlines():
            line = line.strip()
            if not line or "|" not in line:
                continue
            label, val_str = [p.strip() for p in line.split("|", 1)]
            val_clean = re.sub(r"[^\d.]", "", val_str)
            percentage = float(val_clean) if val_clean else 0.0
            prog_items.append(f"""
<div class="progress-item">
  <div class="progress-header">
    <span>{html.escape(label)}</span>
    <span>{html.escape(val_str)}</span>
  </div>
  <div class="progress-track" role="progressbar" aria-valuenow="{percentage}" aria-valuemin="0" aria-valuemax="100">
    <div class="progress-fill" style="width: {percentage}%;"></div>
  </div>
</div>
""")
        return f'<div class="progress-container">{"".join(prog_items)}</div>'

    # 12. Timeline
    if c_type == "timeline":
        time_items = re.split(r"\n(?=###\s+|[0-9]{2}:[0-9]{2}\s*\|)", parsed_inner)
        tl_html: List[str] = []
        for item in time_items:
            item = item.strip()
            if not item:
                continue
            time_label = ""
            title = ""
            content = ""

            if "|" in item and not item.startswith("#"):
                parts = [p.strip() for p in item.split("|")]
                time_label = parts[0]
                title = parts[1] if len(parts) > 1 else ""
                content = parts[2] if len(parts) > 2 else ""
            else:
                m = re.match(r"^###\s+\[(.*?)\]\s+(.*?)(?:\n|$)", item)
                if m:
                    time_label = m.group(1).strip()
                    title = m.group(2).strip()
                    content = item[m.end():].strip()
                else:
                    m2 = re.match(r"^###\s+(.*?)(?:\n|$)", item)
                    if m2:
                        title = m2.group(1).strip()
                        content = item[m2.end():].strip()
                    else:
                        content = item

            body_html = markdown.markdown(content, extensions=["tables", "fenced_code"]) if content else ""
            time_badge = f'<div class="timeline-time">{html.escape(time_label)}</div>' if time_label else ""
            tl_html.append(f"""
<div class="timeline-item">
  {time_badge}
  <div class="timeline-title">{html.escape(title)}</div>
  <div class="timeline-content">{body_html}</div>
</div>
""")
        return f'<div class="timeline-container">{"".join(tl_html)}</div>'

    # Fallback container
    inner_html = markdown.markdown(parsed_inner, extensions=["tables", "fenced_code"])
    return f'<div class="container-{c_type}">{inner_html}</div>'


# --- Code Blocks Post-Processor & Syntax Highlighting ---
def enhance_code_blocks(md_text: str) -> str:
    """Detect fenced code blocks with title/filenames and syntax highlight with Pygments."""
    pattern = re.compile(r"```([a-zA-Z0-9_-]+)?(?:\s+title=[\"']([^\"']+)[\"'])?\n(.*?)```", re.DOTALL)

    def repl(m: re.Match) -> str:
        lang = m.group(1) or "text"
        title = m.group(2) or ""
        code = m.group(3)

        highlighted_code = ""
        if HAS_PYGMENTS:
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
            except Exception:
                lexer = guess_lexer(code) if code.strip() else get_lexer_by_name("text")
            formatter = HtmlFormatter(nowrap=True, cssclass="highlight")
            highlighted_code = pygments.highlight(code, lexer, formatter)
        else:
            highlighted_code = html.escape(code)

        title_html = ""
        if title:
            title_html = f"""
<div class="code-title">
  <svg aria-hidden="true"><use href="#icon-file"></use></svg>
  <span>{html.escape(title)}</span>
</div>
"""
        else:
            title_html = f"""
<div class="code-title">
  <svg aria-hidden="true"><use href="#icon-file"></use></svg>
  <span>{html.escape(lang)}</span>
</div>
"""

        return f"""
<div class="code-block-wrapper">
  <div class="code-header">
    {title_html}
    <div class="code-actions">
      <button class="copy-button" type="button" aria-label="Copy code">
        <svg aria-hidden="true"><use href="#icon-copy"></use></svg>
        <span>Copy</span>
      </button>
    </div>
  </div>
  <pre><code><span class="highlight">{highlighted_code}</span></code></pre>
</div>
"""

    return pattern.sub(repl, md_text)


# --- Heading IDs & Anchor Generation ---
def slugify(text: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug or "section"


def process_headings(html_content: str) -> Tuple[str, List[Tuple[int, str, str]]]:
    """Auto-assign unique IDs to headings, inject anchor links, and extract TOC items."""
    used_ids: Dict[str, int] = {}
    toc_items: List[Tuple[int, str, str]] = []  # (level, id, title)

    heading_pattern = re.compile(r"<h([1-6])([^>]*)>(.*?)</h\1>", re.DOTALL)

    def repl(m: re.Match) -> str:
        level = int(m.group(1))
        attrs = m.group(2)
        inner = m.group(3)

        # Strip any existing anchor or HTML tags for ID generation and clean title
        clean_text = re.sub(r"<[^>]+>", "", inner).strip()

        # Check if an id is already in attrs
        id_match = re.search(r'id=["\']([^"\']+)["\']', attrs)
        if id_match:
            h_id = id_match.group(1)
        else:
            base_slug = slugify(clean_text)
            if base_slug in used_ids:
                used_ids[base_slug] += 1
                h_id = f"{base_slug}-{used_ids[base_slug]}"
            else:
                used_ids[base_slug] = 0
                h_id = base_slug
            attrs = f'{attrs} id="{h_id}"'

        # Only add to TOC for h2 and h3
        if level in (2, 3):
            toc_items.append((level, h_id, clean_text))

        # Add heading anchor link for h2, h3, h4
        anchor_html = ""
        if level in (2, 3, 4):
            anchor_html = f'<a href="#{h_id}" class="heading-anchor" aria-hidden="true">#</a>'

        return f"<h{level}{attrs}>{anchor_html}{inner}</h{level}>"

    processed = heading_pattern.sub(repl, html_content)
    return processed, toc_items


# --- Responsive Table Wrapper ---
def wrap_tables(html_content: str) -> str:
    """Wrap <table> elements with a responsive scrolling container."""
    pattern = re.compile(r"(<table\b[^>]*>.*?</table>)", re.DOTALL)
    return pattern.sub(r'<div class="table-wrapper">\1</div>', html_content)


# --- Task List Checkboxes ---
def process_task_lists(html_content: str) -> str:
    """Enhance task list checkboxes with accessible styling."""
    html_content = re.sub(
        r"<li>\s*\[ \]\s*",
        r'<li class="task-list-item"><input type="checkbox" disabled aria-label="Task incomplete"> ',
        html_content,
    )
    html_content = re.sub(
        r"<li>\s*\[x\]\s*",
        r'<li class="task-list-item"><input type="checkbox" checked disabled aria-label="Task complete"> ',
        html_content,
    )
    return html_content


def estimate_reading_time(text: str) -> str:
    """Calculate estimated reading time at ~200 words per minute."""
    words = len(re.findall(r"\w+", text))
    mins = max(1, round(words / 200))
    return f"{mins} min read"


# --- Main Build Function ---
def build_document(
    input_file: Path,
    output_file: Optional[Path] = None,
    theme: Optional[str] = None,
    accent: Optional[str] = None,
    toc_enabled: Optional[bool] = None,
    mode: Optional[str] = None,
    is_fragment: bool = False,
    cover: bool = False,
) -> Path:
    """Compile input markdown or HTML fragment into a complete self-contained HTML document."""
    assets_dir = find_assets_dir()
    raw_text = input_file.read_text(encoding="utf-8")

    frontmatter, body_markdown = parse_frontmatter(raw_text)

    # Determine settings with precedence: CLI flag > Frontmatter > Default
    doc_theme = theme or frontmatter.get("theme", "aurora")
    doc_accent = accent or frontmatter.get("accent")
    doc_mode = mode or frontmatter.get("mode", "auto")
    doc_cover = cover or frontmatter.get("cover", False)

    if toc_enabled is not None:
        has_toc = toc_enabled
    else:
        has_toc = frontmatter.get("toc", True)

    doc_title = frontmatter.get("title", "")
    doc_subtitle = frontmatter.get("subtitle", "")
    doc_author = frontmatter.get("author", "")
    doc_date = frontmatter.get("date", "")
    doc_status = frontmatter.get("status", "")
    doc_tags = frontmatter.get("tags", [])
    if isinstance(doc_tags, str):
        doc_tags = [t.strip() for t in doc_tags.split(",") if t.strip()]

    # Load Assets
    shell_template = (assets_dir / "shell.html").read_text(encoding="utf-8")
    base_css = (assets_dir / "base.css").read_text(encoding="utf-8")
    components_css = (assets_dir / "components.css").read_text(encoding="utf-8")
    icons_svg = (assets_dir / "icons.svg").read_text(encoding="utf-8")
    app_js = (assets_dir / "app.js").read_text(encoding="utf-8")

    theme_file = assets_dir / "themes" / f"{doc_theme}.css"
    if not theme_file.exists():
        print(f"Warning: Theme '{doc_theme}' not found. Defaulting to 'aurora'.", file=sys.stderr)
        theme_file = assets_dir / "themes" / "aurora.css"
    theme_css = theme_file.read_text(encoding="utf-8")

    # Accent derivation CSS
    accent_css = derive_accent_css(doc_accent) if doc_accent else ""

    content_html = ""
    toc_items: List[Tuple[int, str, str]] = []

    if is_fragment:
        content_html = body_markdown
        content_html, toc_items = process_headings(content_html)
    else:
        # Preprocess code blocks
        preprocessed_code = enhance_code_blocks(body_markdown)
        # Preprocess containers
        preprocessed_containers = parse_containers(preprocessed_code)
        # Markdown parsing
        converted_html = markdown.markdown(
            preprocessed_containers,
            extensions=["tables", "fenced_code", "footnotes", "def_list", "attr_list"],
        )
        # Post-process tables and task lists
        wrapped = wrap_tables(converted_html)
        with_tasks = process_task_lists(wrapped)
        # Process headings
        content_html, toc_items = process_headings(with_tasks)

    # Fallback title if not provided in frontmatter
    if not doc_title:
        # Look for first H1 in markdown
        m_h1 = re.search(r"^#\s+(.+)$", body_markdown, re.MULTILINE)
        if m_h1:
            doc_title = m_h1.group(1).strip()
        else:
            doc_title = input_file.stem.replace("-", " ").replace("_", " ").title()

    reading_time = estimate_reading_time(body_markdown)

    # Generate TOC HTML
    sidebar_toc_html = ""
    mobile_toc_drawer_html = ""
    mobile_toc_button = ""

    if has_toc and toc_items:
        toc_li: List[str] = []
        for level, h_id, h_text in toc_items:
            cls = "level-2" if level == 2 else "level-3"
            toc_li.append(f'<li class="toc-item {cls}"><a href="#{h_id}" class="toc-link">{html.escape(h_text)}</a></li>')

        toc_nav = f'<ul class="toc-list">{"".join(toc_li)}</ul>'
        sidebar_toc_html = f"""
<aside class="doc-sidebar" aria-label="Table of contents">
  <div class="toc-heading">
    <svg aria-hidden="true"><use href="#icon-layers"></use></svg>
    <span>Contents</span>
  </div>
  {toc_nav}
</aside>
"""
        mobile_toc_drawer_html = f"""
<div id="mobile-toc-overlay" class="mobile-toc-overlay"></div>
<div id="mobile-toc-drawer" class="mobile-toc-drawer" role="dialog" aria-modal="true" aria-label="Table of contents">
  <div class="mobile-toc-header">
    <strong>Contents</strong>
    <button id="mobile-toc-close" class="icon-btn" type="button" aria-label="Close Table of Contents">
      <svg aria-hidden="true"><use href="#icon-x"></use></svg>
    </button>
  </div>
  {toc_nav}
</div>
"""
        mobile_toc_button = """
<button id="mobile-toc-toggle" class="icon-btn mobile-toc-btn" type="button" aria-label="Table of Contents" title="Table of Contents">
  <svg aria-hidden="true"><use href="#icon-menu"></use></svg>
</button>
"""

    grid_class = "" if (has_toc and toc_items) else "no-toc"

    # Header Badges & Chips
    status_badge = ""
    if doc_status:
        st = doc_status.lower()
        badge_cls = f"badge-{st}" if st in ("draft", "review", "final") else "badge-draft"
        status_badge = f'<span class="badge {badge_cls}">{html.escape(doc_status.capitalize())}</span>'

    tags_html = "".join(
        f'<span class="tag-chip"><svg aria-hidden="true"><use href="#icon-tag"></use></svg>{html.escape(t)}</span>'
        for t in doc_tags
    )

    subtitle_html = f'<p class="doc-subtitle">{html.escape(doc_subtitle)}</p>' if doc_subtitle else ""
    author_html = f'<div class="hero-meta-item"><svg aria-hidden="true"><use href="#icon-user"></use></svg><span>{html.escape(doc_author)}</span></div>' if doc_author else ""
    date_html = f'<div class="hero-meta-item"><svg aria-hidden="true"><use href="#icon-calendar"></use></svg><span>{html.escape(doc_date)}</span></div>' if doc_date else ""
    read_time_html = f'<div class="hero-meta-item"><svg aria-hidden="true"><use href="#icon-clock"></use></svg><span>{reading_time}</span></div>'

    # Content Security Policy (strict offline default)
    csp_meta = '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; img-src \'self\' data:; script-src \'unsafe-inline\';">'

    replacements = {
        "{{THEME}}": doc_theme,
        "{{MODE}}": doc_mode,
        "{{CSP_META}}": csp_meta,
        "{{TITLE}}": html.escape(doc_title),
        "{{THEME_CSS}}": theme_css,
        "{{BASE_CSS}}": base_css,
        "{{COMPONENTS_CSS}}": components_css,
        "{{ACCENT_CSS}}": accent_css,
        "{{ICONS_SVG}}": icons_svg,
        "{{APP_JS}}": app_js,
        "{{TYPE_LABEL}}": "Document",
        "{{MOBILE_TOC_BUTTON}}": mobile_toc_button,
        "{{STATUS_BADGE}}": status_badge,
        "{{TAGS_CHIPS}}": tags_html,
        "{{SUBTITLE_HTML}}": subtitle_html,
        "{{AUTHOR_HTML}}": author_html,
        "{{DATE_HTML}}": date_html,
        "{{READING_TIME_HTML}}": read_time_html,
        "{{GRID_CLASS}}": grid_class,
        "{{SIDEBAR_TOC_HTML}}": sidebar_toc_html,
        "{{MOBILE_TOC_DRAWER_HTML}}": mobile_toc_drawer_html,
        "{{CONTENT_HTML}}": content_html,
    }

    assembled = shell_template
    for k, v in replacements.items():
        assembled = assembled.replace(k, v)

    # Determine output path
    if output_file is None:
        out_dir = Path("docs")
        out_dir.mkdir(parents=True, exist_ok=True)
        output_file = out_dir / f"{input_file.stem}.html"
    else:
        output_file.parent.mkdir(parents=True, exist_ok=True)

    output_file.write_text(assembled, encoding="utf-8")
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Compile Markdown + Frontmatter + Containers into standalone premium HTML documents.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input", type=Path, help="Input Markdown file (or HTML fragment if --fragment)")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output HTML destination")
    parser.add_argument("--theme", choices=["aurora", "slate", "paper"], default=None, help="Override visual theme")
    parser.add_argument("--accent", type=str, default=None, help="Custom hex accent color (e.g. '#6366f1')")
    parser.add_argument("--toc", dest="toc", action="store_true", default=None, help="Force enable Table of Contents")
    parser.add_argument("--no-toc", dest="toc", action="store_false", help="Force disable Table of Contents")
    parser.add_argument("--mode", choices=["auto", "light", "dark"], default=None, help="Theme appearance mode")
    parser.add_argument("--fragment", action="store_true", help="Treat input as an HTML body fragment (Mode B)")
    parser.add_argument("--cover", action="store_true", help="Render full cover hero layout")
    parser.add_argument("--no-source", action="store_true", help="Do not require source .md file alongside output")
    parser.add_argument("--pdf", action="store_true", help="Print instructions for PDF rendering (v0.2 preview)")
    parser.add_argument("--json", action="store_true", help="Output build results in JSON format")

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input file does not exist: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        out_path = build_document(
            input_file=args.input,
            output_file=args.output,
            theme=args.theme,
            accent=args.accent,
            toc_enabled=args.toc,
            mode=args.mode,
            is_fragment=args.fragment,
            cover=args.cover,
        )

        size_bytes = out_path.stat().st_size
        if args.json:
            result = {
                "status": "success",
                "input": str(args.input),
                "output": str(out_path),
                "size_bytes": size_bytes,
                "theme": args.theme or "aurora",
            }
            print(json.dumps(result, indent=2))
        else:
            print(f"Successfully built: {out_path} ({size_bytes:,} bytes)")

        if args.pdf:
            print("Note: PDF rendering via headless Chromium is scheduled for v0.2. You can print to PDF using the print button in the header.")

    except SyntaxError as se:
        print(f"Syntax Error: {se}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Build Failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
