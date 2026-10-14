"""
Unit and integration tests for install.py installer and platform adapters.
"""

import subprocess
import sys
import tempfile
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALLER = REPO_ROOT / "install.py"


class TestInstallerCLI:
    def test_installer_list(self):
        res = subprocess.run([sys.executable, str(INSTALLER), "--list"], capture_output=True, text=True)
        assert res.returncode == 0
        assert "Google Antigravity" in res.stdout
        assert "Claude Code" in res.stdout
        assert "Cursor" in res.stdout
        assert "Gemini CLI" in res.stdout
        assert "GitHub Copilot" in res.stdout
        assert "Codeium Windsurf" in res.stdout
        assert "Cline / Roo-Code" in res.stdout

    def test_installer_version(self):
        res = subprocess.run([sys.executable, str(INSTALLER), "--version"], capture_output=True, text=True)
        assert res.returncode == 0
        assert "0.1.0" in res.stdout

    def test_dry_run_leaves_directory_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir)
            res = subprocess.run(
                [sys.executable, str(INSTALLER), "--target", "all", "--dest", str(dest), "--dry-run"],
                capture_output=True,
                text=True,
            )
            assert res.returncode == 0
            assert "DRY RUN" in res.stdout
            assert len(list(dest.iterdir())) == 0, "Dry run must not create any files or folders"


class TestInstallerOperations:
    def test_install_all_targets(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir)
            res = subprocess.run(
                [sys.executable, str(INSTALLER), "--target", "all", "--dest", str(dest)],
                capture_output=True,
                text=True,
            )
            assert res.returncode == 0, f"Install failed:\n{res.stderr}"

            # Check skills
            assert (dest / ".agents" / "skills" / "premium-docs" / "SKILL.md").exists()
            assert (dest / ".claude" / "skills" / "premium-docs" / "SKILL.md").exists()
            assert (dest / ".cursor" / "skills" / "premium-docs" / "SKILL.md").exists()
            assert (dest / ".gemini" / "skills" / "premium-docs" / "SKILL.md").exists()
            assert (dest / "skills" / "premium-docs" / "SKILL.md").exists()
            assert (dest / ".github" / "skills" / "premium-docs" / "SKILL.md").exists()
            assert (dest / ".windsurf" / "skills" / "premium-docs" / "SKILL.md").exists()
            assert (dest / ".cline" / "skills" / "premium-docs" / "SKILL.md").exists()

            # Check rules & workflows
            assert (dest / ".agents" / "workflows" / "premium-doc.md").exists()
            assert (dest / ".agents" / "rules" / "premium-docs.md").exists()
            assert (dest / "CLAUDE.md").exists()
            assert (dest / ".cursor" / "rules" / "premium-docs.mdc").exists()
            assert (dest / "GEMINI.md").exists()
            assert (dest / "AGENTS.md").exists()
            assert (dest / ".github" / "copilot-instructions.md").exists()
            assert (dest / ".windsurfrules").exists()
            assert (dest / ".clinerules").exists()

    def test_idempotent_install(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir)
            # Run 1
            res1 = subprocess.run(
                [sys.executable, str(INSTALLER), "--target", "claude,gemini", "--dest", str(dest)],
                capture_output=True,
                text=True,
            )
            assert res1.returncode == 0

            # Run 2
            res2 = subprocess.run(
                [sys.executable, str(INSTALLER), "--target", "claude,gemini", "--dest", str(dest)],
                capture_output=True,
                text=True,
            )
            assert res2.returncode == 0

            claude_text = (dest / "CLAUDE.md").read_text(encoding="utf-8")
            gemini_text = (dest / "GEMINI.md").read_text(encoding="utf-8")
            assert claude_text.count("<!-- BEGIN PREMIUM-DOCS -->") == 1
            assert gemini_text.count("<!-- BEGIN PREMIUM-DOCS -->") == 1

    def test_snippet_preservation_and_uninstall(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dest = Path(tmpdir)
            claude_file = dest / "CLAUDE.md"
            claude_file.write_text("# My Existing Claude Instructions\nImportant rule here.\n", encoding="utf-8")

            # Install
            res_in = subprocess.run(
                [sys.executable, str(INSTALLER), "--target", "claude", "--dest", str(dest)],
                capture_output=True,
                text=True,
            )
            assert res_in.returncode == 0
            text_after_install = claude_file.read_text(encoding="utf-8")
            assert "Important rule here." in text_after_install
            assert "<!-- BEGIN PREMIUM-DOCS -->" in text_after_install

            # Uninstall
            res_un = subprocess.run(
                [sys.executable, str(INSTALLER), "--target", "claude", "--dest", str(dest), "--uninstall"],
                capture_output=True,
                text=True,
            )
            assert res_un.returncode == 0
            text_after_uninstall = claude_file.read_text(encoding="utf-8")
            assert "Important rule here." in text_after_uninstall
            assert "<!-- BEGIN PREMIUM-DOCS -->" not in text_after_uninstall
            assert not (dest / ".claude" / "skills" / "premium-docs").exists()
