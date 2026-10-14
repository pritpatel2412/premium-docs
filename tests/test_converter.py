"""
Unit and integration tests for build_doc.py (AST Container Parser and HTML Compiler).
"""

import sys
import subprocess
import tempfile
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_SCRIPT = REPO_ROOT / "skills" / "premium-docs" / "scripts" / "build_doc.py"


def run_build(md_content: str, extra_args=None) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = Path(tmpdir) / "doc.md"
        output_path = Path(tmpdir) / "doc.html"
        input_path.write_text(md_content, encoding="utf-8")
        cmd = [sys.executable, str(BUILD_SCRIPT), str(input_path), "-o", str(output_path)]
        if extra_args:
            cmd.extend(extra_args)
        res = subprocess.run(cmd, capture_output=True, text=True)
        html = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
        return res, html


class TestFrontmatterAndMetadata:
    def test_frontmatter_parsing(self):
        md = """---
title: "System Architecture & Design"
subtitle: "High-performance microservices architecture"
date: "2026-10-14"
version: "2.1.0"
author: "Engineering Team"
theme: "aurora"
mode: "dark"
toc: true
---

# Overview
This is a test document.
"""
        res, html = run_build(md)
        assert res.returncode == 0
        assert "<title>System Architecture &amp; Design</title>" in html
        assert "System Architecture &amp; Design" in html
        assert "High-performance microservices architecture" in html
        assert "2026-10-14" in html
        assert "v2.1.0" in html
        assert "Engineering Team" in html
        assert 'data-theme="aurora"' in html
        assert 'data-mode="dark"' in html

    def test_default_metadata_fallback(self):
        md = "# Untitled Document\n\nBody content."
        res, html = run_build(md)
        assert res.returncode == 0
        assert 'data-theme="aurora"' in html
        assert 'data-mode="auto"' in html


class TestContainerParsing:
    def test_tldr_container(self):
        md = """# Sample
:::tldr Executive Summary
Key takeaways go here in bold.
:::
"""
        res, html = run_build(md)
        assert res.returncode == 0
        assert 'class="tldr-box"' in html
        assert "Executive Summary" in html
        assert "Key takeaways go here in bold." in html

    def test_stats_container(self):
        md = """# Sample
:::stats
99.99% | Uptime SLA | +0.05%
12ms | Latency P99 | -4ms
:::
"""
        res, html = run_build(md)
        assert res.returncode == 0
        assert 'class="stats-grid"' in html
        assert '<div class="stat-value">99.99%</div>' in html
        assert '<div class="stat-label">Uptime SLA</div>' in html
        assert 'class="stat-delta positive"' in html
        assert '<div class="stat-value">12ms</div>' in html
        assert 'class="stat-delta negative"' in html

    def test_cards_grid(self):
        md = """# Sample
:::cards
### Cloud Storage
Scalable object storage for binary artifacts.
---
### CDN Distribution
Low-latency edge caching across 200+ PoPs.
:::
"""
        res, html = run_build(md)
        assert res.returncode == 0
        assert 'class="cards-grid"' in html
        assert 'class="card-item"' in html
        assert "Cloud Storage" in html
        assert "Scalable object storage" in html

    def test_callouts_variants(self):
        for variant in ["note", "tip", "info", "success", "warning", "danger"]:
            md = f"""# Sample
:::{variant}
This is a {variant} notice.
:::
"""
            res, html = run_build(md)
            assert res.returncode == 0
            assert f'class="callout callout-{variant}"' in html
            assert f"This is a {variant} notice." in html

    def test_steps_container(self):
        md = """# Installation Steps
:::steps
### Prepare Environment
Install Python 3.9+ and git.
### Clone Repository
Clone the repository locally.
:::
"""
        res, html = run_build(md)
        assert res.returncode == 0
        assert 'class="steps-container"' in html
        assert 'class="step-item"' in html
        assert '<div class="step-badge">1</div>' in html
        assert '<div class="step-badge">2</div>' in html
        assert "Prepare Environment" in html

    def test_timeline_container(self):
        md = """# Timeline
:::timeline
14:00 UTC | Alert Triggered | High latency detected on ingress nodes.
14:15 UTC | Traffic Rerouted | Traffic shifted to standby datacenter.
:::
"""
        res, html = run_build(md)
        assert res.returncode == 0
        assert 'class="timeline-container"' in html
        assert 'class="timeline-item"' in html
        assert '<div class="timeline-time">14:00 UTC</div>' in html
        assert "Alert Triggered" in html

    def test_badges(self):
        md = """# Badges
:::badge success Production Ready
:::
:::badge danger Deprecated
:::
"""
        res, html = run_build(md)
        assert res.returncode == 0
        assert '<span class="badge badge-success">Production Ready</span>' in html
        assert '<span class="badge badge-danger">Deprecated</span>' in html

    def test_tabs_container(self):
        md = """# Tabs
:::tabs
@tab Python
```python
print("Hello Python")
```
@tab JavaScript
```javascript
console.log("Hello JS");
```
:::
"""
        res, html = run_build(md)
        assert res.returncode == 0
        assert 'class="tabs-container"' in html
        assert 'class="tab-list"' in html
        assert 'class="tab-button"' in html
        assert "Python" in html
        assert "JavaScript" in html
        assert 'class="tab-panel"' in html

    def test_table_wrap(self):
        md = """# Table
:::table-wrap
| Feature | Supported | Notes |
| :--- | :--- | :--- |
| Offline | Yes | 100% self-contained |
:::
"""
        res, html = run_build(md)
        assert res.returncode == 0
        assert 'class="table-wrapper"' in html
        assert '<table>' in html

    def test_filetree(self):
        md = """# Project Structure
:::filetree
src/
├── core/
│   └── engine.py
└── main.py
:::
"""
        res, html = run_build(md)
        assert res.returncode == 0
        assert 'class="filetree-container"' in html
        assert "engine.py" in html


class TestSyntaxErrorHandling:
    def test_unclosed_container_line_error(self):
        md = """# Unclosed Container Test
Line 2
:::cards Unclosed Card
Content without closing tag.
"""
        res, _ = run_build(md)
        assert res.returncode != 0
        assert "Line 3: Unclosed container ':::cards'" in res.stderr

    def test_unexpected_closing_tag(self):
        md = """# Unexpected Closing
Line 2
:::
"""
        res, _ = run_build(md)
        assert res.returncode != 0
        assert "Line 3: Unexpected closing ':::'" in res.stderr


class TestCodeHighlightingAndFragment:
    def test_pygments_highlighting(self):
        md = """# Code Test
```python
def add(a: int, b: int) -> int:
    return a + b
```
"""
        res, html = run_build(md)
        assert res.returncode == 0
        assert 'class="highlight"' in html
        assert 'class="copy-button"' in html
        assert "def add" in html or "add</span>" in html

    def test_fragment_mode(self):
        fragment_input = """<h1>Fragment Title</h1>
<div class="callout callout-info"><p>Fragment body content.</p></div>
"""
        res, html = run_build(fragment_input, extra_args=["--fragment"])
        assert res.returncode == 0
        assert "<!DOCTYPE html>" in html
        assert 'class="callout callout-info"' in html
        assert "Fragment body content." in html


class TestTocDoubleEscaping:
    def test_heading_ampersand_unescaped_in_toc(self):
        md = """# Document

## R&D & Engineering

Content under R&D.
"""
        res, html = run_build(md)
        assert res.returncode == 0
        assert "&amp;amp;" not in html
        assert "R&amp;D &amp; Engineering" in html
