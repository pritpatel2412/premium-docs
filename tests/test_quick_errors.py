import subprocess
import sys
from pathlib import Path

def test_errors():
    fixtures_dir = Path("tests/fixtures")
    fixtures_dir.mkdir(parents=True, exist_ok=True)

    # Test 1: Unclosed container
    bad_md = fixtures_dir / "bad-unclosed.md"
    bad_md.write_text("# Title\n\n:::note Unclosed\nSome content without closing\n", encoding="utf-8")
    res1 = subprocess.run(
        [sys.executable, "skills/premium-docs/scripts/build_doc.py", str(bad_md)],
        capture_output=True,
        text=True,
    )
    print("Test 1 (Unclosed container) exit code:", res1.returncode)
    print("Test 1 stderr snippet:", res1.stderr.strip()[:200])
    assert res1.returncode != 0
    assert "Line 3: Unclosed container ':::note'" in res1.stderr

    # Test 2: Broken anchor validation
    bad_html = fixtures_dir / "bad-anchor.html"
    bad_html.write_text("<h1>Title</h1><a href=\"#missing-section\">Broken</a>", encoding="utf-8")
    res2 = subprocess.run(
        [sys.executable, "skills/premium-docs/scripts/validate_doc.py", str(bad_html)],
        capture_output=True,
        text=True,
    )
    print("Test 2 (Broken anchor) exit code:", res2.returncode)
    print("Test 2 errors:", [l for l in res2.stdout.splitlines() if "[X]" in l])
    assert res2.returncode != 0
    assert any("missing-section" in l for l in res2.stdout.splitlines())

    print("\nAll error tests passed successfully!")

if __name__ == "__main__":
    test_errors()
