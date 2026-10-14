"""
WCAG AA Contrast Ratio mathematical test suite for premium-docs themes.
Verifies that all themes (aurora, slate, paper) in both light and dark modes meet
the WCAG 2.1 AA requirement of at least 4.5:1 for body text against the canvas.
"""

import re
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
THEMES_DIR = REPO_ROOT / "skills" / "premium-docs" / "assets" / "themes"


def hex_to_rgb(hex_str: str):
    hex_str = hex_str.strip().lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join(c * 2 for c in hex_str)
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


def relative_luminance(rgb):
    def channel_linear(c):
        c_norm = c / 255.0
        if c_norm <= 0.04045:
            return c_norm / 12.92
        else:
            return ((c_norm + 0.055) / 1.055) ** 2.4

    r, g, b = (channel_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(color1_hex: str, color2_hex: str) -> float:
    l1 = relative_luminance(hex_to_rgb(color1_hex))
    l2 = relative_luminance(hex_to_rgb(color2_hex))
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def extract_colors_from_css(css_text: str):
    """
    Extracts light mode and dark mode bg-canvas and text-primary colors.
    """
    # Find :root (light mode)
    light_match = re.search(r":root\s*\{([^}]+)\}", css_text)
    dark_match = re.search(r'(:root\[data-mode="dark"\]|@media\s*\([^\)]+dark[^\)]*\))\s*\{([^}]+)\}', css_text)

    def extract_vars(block: str):
        bg = re.search(r"--bg-canvas\s*:\s*([^;]+);", block)
        text = re.search(r"--text-primary\s*:\s*([^;]+);", block)
        text_sec = re.search(r"--text-secondary\s*:\s*([^;]+);", block)
        return {
            "bg": bg.group(1).strip() if bg else "#ffffff",
            "text": text.group(1).strip() if text else "#000000",
            "text_sec": text_sec.group(1).strip() if text_sec else "#333333",
        }

    light_vars = extract_vars(light_match.group(1)) if light_match else {"bg": "#ffffff", "text": "#000000"}
    dark_vars = extract_vars(dark_match.group(2)) if dark_match else {"bg": "#0b0f19", "text": "#f1f5f9"}
    return light_vars, dark_vars


class TestThemeContrastRatios:
    @pytest.mark.parametrize("theme_name", ["aurora.css", "slate.css", "paper.css"])
    def test_wcag_aa_contrast(self, theme_name):
        theme_path = THEMES_DIR / theme_name
        assert theme_path.exists(), f"Theme {theme_name} must exist"
        css_content = theme_path.read_text(encoding="utf-8")
        light_vars, dark_vars = extract_colors_from_css(css_content)

        # Light mode test
        light_ratio = contrast_ratio(light_vars["text"], light_vars["bg"])
        print(f"\n{theme_name} (Light): text {light_vars['text']} vs bg {light_vars['bg']} -> {light_ratio:.2f}:1")
        assert light_ratio >= 4.5, f"{theme_name} light mode contrast {light_ratio:.2f}:1 fails WCAG AA (≥ 4.5:1)"

        # Dark mode test
        dark_ratio = contrast_ratio(dark_vars["text"], dark_vars["bg"])
        print(f"{theme_name} (Dark):  text {dark_vars['text']} vs bg {dark_vars['bg']} -> {dark_ratio:.2f}:1")
        assert dark_ratio >= 4.5, f"{theme_name} dark mode contrast {dark_ratio:.2f}:1 fails WCAG AA (≥ 4.5:1)"
