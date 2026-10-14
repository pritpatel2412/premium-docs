"""
Unit and integration tests for validate_doc.py document quality and compliance validator.
"""

import sys
import subprocess
import tempfile
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
VALIDATE_SCRIPT = REPO_ROOT / "skills" / "premium-docs" / "scripts" / "validate_doc.py"
EXAMPLES_DIR = REPO_ROOT / "skills" / "premium-docs" / "examples"


def run_validator(html_content: str, extra_args=None) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmpdir:
        doc_path = Path(tmpdir) / "test.html"
        doc_path.write_text(html_content, encoding="utf-8")
        cmd = [sys.executable, str(VALIDATE_SCRIPT), str(doc_path)]
        if extra_args:
            cmd.extend(extra_args)
        return subprocess.run(cmd, capture_output=True, text=True)


class TestExamplesValidation:
    @pytest.mark.parametrize("example_name", [
        "technical-report.html",
        "prd-feature-spec.html",
        "project-guide.html",
        "incident-postmortem.html",
    ])
    def test_official_examples_pass(self, example_name):
        doc_path = EXAMPLES_DIR / example_name
        assert doc_path.exists(), f"Example {example_name} must exist"
        cmd = [sys.executable, str(VALIDATE_SCRIPT), str(doc_path)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        assert res.returncode == 0, f"Validator failed on {example_name}:\n{res.stdout}"
        assert "Result: PASSED" in res.stdout


class TestValidatorRules:
    def test_missing_h1_fails(self):
        html = """<!DOCTYPE html><html><body><h2>Subheading Only</h2></body></html>"""
        res = run_validator(html)
        assert res.returncode != 0
        assert any("missing an <h1>" in l for l in res.stdout.splitlines())

    def test_multiple_h1_fails(self):
        html = """<!DOCTYPE html><html><body><h1>First</h1><h1>Second</h1></body></html>"""
        res = run_validator(html)
        assert res.returncode != 0
        assert any("contains 2 <h1>" in l for l in res.stdout.splitlines())

    def test_duplicate_heading_ids_fails(self):
        html = """<!DOCTYPE html><html><body><h1 id="title">Title</h1><h2 id="intro">Section 1</h2><h2 id="intro">Section 2</h2></body></html>"""
        res = run_validator(html)
        assert res.returncode != 0
        assert any("Duplicate heading IDs" in l for l in res.stdout.splitlines())

    def test_broken_local_anchor_fails(self):
        html = """<!DOCTYPE html><html><body><h1 id="title">Title</h1><a href="#non-existent">Link</a></body></html>"""
        res = run_validator(html)
        assert res.returncode != 0
        assert any("Broken internal anchor links" in l for l in res.stdout.splitlines())

    def test_valid_local_anchor_passes(self):
        html = """<!DOCTYPE html><html><head><meta http-equiv="Content-Security-Policy" content="default-src 'none';"><style>:root { --bg: #ffffff; --text: #000000; }</style></head><body><h1 id="title">Title</h1><a href="#title">Back to Top</a></body></html>"""
        res = run_validator(html)
        assert res.returncode == 0

    def test_external_script_fails(self):
        html = """<!DOCTYPE html><html><head><script src="https://cdn.example.com/app.js"></script></head><body><h1>Title</h1></body></html>"""
        res = run_validator(html)
        assert res.returncode != 0
        assert any("External resource prohibited" in l for l in res.stdout.splitlines())

    def test_external_stylesheet_fails(self):
        html = """<!DOCTYPE html><html><head><link rel="stylesheet" href="https://cdn.example.com/base.css"></head><body><h1>Title</h1></body></html>"""
        res = run_validator(html)
        assert res.returncode != 0
        assert any("External resource prohibited" in l for l in res.stdout.splitlines())

    def test_external_hyperlink_allowed(self):
        html = """<!DOCTYPE html><html><head><meta http-equiv="Content-Security-Policy" content="default-src 'none';"><style>:root { --bg: #ffffff; --text: #000000; }</style></head><body><h1 id="title">Title</h1><a href="https://github.com/pritpatel2412/premium-docs">Repo</a></body></html>"""
        res = run_validator(html)
        assert res.returncode == 0

    def test_unparsed_container_marker_fails(self):
        html = """<!DOCTYPE html><html><body><h1 id="title">Title</h1>\n:::tldr\nUnparsed\n:::\n</body></html>"""
        res = run_validator(html)
        assert res.returncode != 0
        assert any("unparsed container marker" in l for l in res.stdout.splitlines())

    def test_missing_image_alt_fails(self):
        html = """<!DOCTYPE html><html><body><h1 id="title">Title</h1><img src="data:image/png;base64,iVBORw0KGgo="></body></html>"""
        res = run_validator(html)
        assert res.returncode != 0
        assert any("missing alt text" in l for l in res.stdout.splitlines())

    def test_size_budget_enforcement(self):
        large_body = "A" * (1_100_000)
        html = f"""<!DOCTYPE html><html><body><h1 id="title">Title</h1><p>{large_body}</p></body></html>"""
        res = run_validator(html)
        assert res.returncode != 0
        assert any("exceeds 1MB budget" in l for l in res.stdout.splitlines())
