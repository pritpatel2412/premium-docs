#!/usr/bin/env python3
"""
premium-docs Installer & Adapter Manager
Installs the premium-docs agent skill, workflows, and rule adapters across 8 major AI agent ecosystems.

Supported Targets:
  - antigravity: Google Antigravity (.agents/skills, .agents/workflows, .agents/rules)
  - claude:      Claude Code (.claude/skills, CLAUDE.md)
  - cursor:      Cursor (.cursor/skills, .cursor/rules/premium-docs.mdc)
  - gemini:      Gemini CLI (.gemini/skills, GEMINI.md)
  - agents:      AGENTS.md / Codex / OpenHands (skills/, AGENTS.md)
  - copilot:     GitHub Copilot (.github/skills, .github/copilot-instructions.md)
  - windsurf:    Codeium Windsurf (.windsurf/skills, .windsurfrules)
  - cline:       Cline / Roo-Code (.cline/skills, .clinerules)
  - all:         All 8 supported platforms

Usage:
  python install.py --target antigravity
  python install.py --target claude,cursor --scope project
  python install.py --target all --dry-run
  python install.py --target antigravity --uninstall
"""

import argparse
import os
import platform
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

VERSION = "0.1.0"
SNIPPET_START = "<!-- BEGIN PREMIUM-DOCS -->"
SNIPPET_END = "<!-- END PREMIUM-DOCS -->"

# Color helpers for terminal
USE_COLOR = sys.stdout.isatty() and platform.system() != "Windows" or os.environ.get("ANSICON") or os.environ.get("WT_SESSION")


def color(text: str, code: str) -> str:
    if not USE_COLOR:
        return text
    return f"\033[{code}m{text}\033[0m"


def bold(text: str) -> str:
    return color(text, "1")


def green(text: str) -> str:
    return color(text, "32")


def cyan(text: str) -> str:
    return color(text, "36")


def yellow(text: str) -> str:
    return color(text, "33")


def red(text: str) -> str:
    return color(text, "31")


def dim(text: str) -> str:
    return color(text, "90")


class TargetConfig:
    def __init__(
        self,
        name: str,
        display_name: str,
        project_skill_rel: Optional[str],
        project_rules: List[Tuple[str, str, bool]],  # (rel_dest, adapter_src, is_snippet)
        global_skill_rel: Optional[str],
        global_rules: List[Tuple[str, str, bool]],
    ):
        self.name = name
        self.display_name = display_name
        self.project_skill_rel = project_skill_rel
        self.project_rules = project_rules
        self.global_skill_rel = global_skill_rel
        self.global_rules = global_rules


# Repository paths
REPO_ROOT = Path(__file__).resolve().parent
SKILL_SRC = REPO_ROOT / "skills" / "premium-docs"
ADAPTERS_SRC = REPO_ROOT / "adapters"

TARGET_REGISTRY: Dict[str, TargetConfig] = {
    "antigravity": TargetConfig(
        name="antigravity",
        display_name="Google Antigravity",
        project_skill_rel=".agents/skills/premium-docs",
        project_rules=[
            (".agents/workflows/premium-doc.md", "antigravity/workflows/premium-doc.md", False),
            (".agents/rules/premium-docs.md", "antigravity/rules/premium-docs.md", False),
        ],
        global_skill_rel=".gemini/config/skills/premium-docs",
        global_rules=[
            (".gemini/config/workflows/premium-doc.md", "antigravity/workflows/premium-doc.md", False),
            (".gemini/config/rules/premium-docs.md", "antigravity/rules/premium-docs.md", False),
        ],
    ),
    "claude": TargetConfig(
        name="claude",
        display_name="Claude Code",
        project_skill_rel=".claude/skills/premium-docs",
        project_rules=[
            ("CLAUDE.md", "claude-code/CLAUDE.md", True),
        ],
        global_skill_rel=".claude/skills/premium-docs",
        global_rules=[
            (".claude/CLAUDE.md", "claude-code/CLAUDE.md", True),
        ],
    ),
    "cursor": TargetConfig(
        name="cursor",
        display_name="Cursor",
        project_skill_rel=".cursor/skills/premium-docs",
        project_rules=[
            (".cursor/rules/premium-docs.mdc", "cursor/premium-docs.mdc", False),
        ],
        global_skill_rel=".cursor/skills/premium-docs",
        global_rules=[
            (".cursor/rules/premium-docs.mdc", "cursor/premium-docs.mdc", False),
        ],
    ),
    "gemini": TargetConfig(
        name="gemini",
        display_name="Gemini CLI",
        project_skill_rel=".gemini/skills/premium-docs",
        project_rules=[
            ("GEMINI.md", "gemini-cli/GEMINI.md", True),
        ],
        global_skill_rel=".gemini/skills/premium-docs",
        global_rules=[
            (".gemini/GEMINI.md", "gemini-cli/GEMINI.md", True),
        ],
    ),
    "agents": TargetConfig(
        name="agents",
        display_name="Codex / AGENTS.md / OpenHands",
        project_skill_rel="skills/premium-docs",
        project_rules=[
            ("AGENTS.md", "agents-md/AGENTS.md", True),
        ],
        global_skill_rel=".agents/skills/premium-docs",
        global_rules=[
            (".agents/AGENTS.md", "agents-md/AGENTS.md", True),
        ],
    ),
    "copilot": TargetConfig(
        name="copilot",
        display_name="GitHub Copilot",
        project_skill_rel=".github/skills/premium-docs",
        project_rules=[
            (".github/copilot-instructions.md", "copilot/copilot-instructions.md", True),
        ],
        global_skill_rel=".config/github-copilot/skills/premium-docs",
        global_rules=[
            (".config/github-copilot/copilot-instructions.md", "copilot/copilot-instructions.md", True),
        ],
    ),
    "windsurf": TargetConfig(
        name="windsurf",
        display_name="Codeium Windsurf",
        project_skill_rel=".windsurf/skills/premium-docs",
        project_rules=[
            (".windsurfrules", "windsurf/.windsurfrules", True),
        ],
        global_skill_rel=".codeium/windsurf/skills/premium-docs",
        global_rules=[
            (".windsurfrules", "windsurf/.windsurfrules", True),
        ],
    ),
    "cline": TargetConfig(
        name="cline",
        display_name="Cline / Roo-Code",
        project_skill_rel=".cline/skills/premium-docs",
        project_rules=[
            (".clinerules", "cline/.clinerules", True),
        ],
        global_skill_rel=".cline/skills/premium-docs",
        global_rules=[
            (".clinerules", "cline/.clinerules", True),
        ],
    ),
}


class Installer:
    def __init__(
        self,
        dest_root: Path,
        scope: str = "project",
        dry_run: bool = False,
        with_rule: bool = True,
        use_symlink: bool = False,
        force: bool = False,
    ):
        self.dest_root = dest_root.resolve()
        self.scope = scope
        self.dry_run = dry_run
        self.with_rule = with_rule
        self.use_symlink = use_symlink
        self.force = force

    def _copy_or_link_dir(self, src: Path, dst: Path) -> str:
        """Copies or links directory from src to dst. Returns action string."""
        if dst.resolve() == src.resolve():
            return "same directory (in-place repo, skipped)"

        if self.dry_run:
            return f"would install directory to {dst}"

        # Clean destination if exists
        if dst.exists() or dst.is_symlink():
            if dst.is_symlink() or dst.is_file():
                dst.unlink()
            else:
                shutil.rmtree(dst)

        dst.parent.mkdir(parents=True, exist_ok=True)

        if self.use_symlink:
            try:
                dst.symlink_to(src, target_is_directory=True)
                return f"symlinked to {dst}"
            except (OSError, NotImplementedError):
                # Fallback on systems without symlink privileges (e.g. non-dev Windows)
                shutil.copytree(src, dst)
                return f"copied to {dst} (symlink unavailable, copied instead)"
        else:
            shutil.copytree(src, dst)
            return f"copied to {dst}"

    def _install_rule_file(self, src_file: Path, dst_file: Path, is_snippet: bool) -> str:
        """Installs or updates a rule file or snippet. Returns action description."""
        if not src_file.exists():
            return f"source adapter missing ({src_file})"

        content = src_file.read_text(encoding="utf-8")

        if self.dry_run:
            if is_snippet and dst_file.exists():
                return f"would update snippet in {dst_file}"
            return f"would write {dst_file}"

        dst_file.parent.mkdir(parents=True, exist_ok=True)

        if not is_snippet:
            # Standalone file: copy directly
            shutil.copy2(src_file, dst_file)
            return f"created {dst_file}"

        # Snippet file: merge or append
        if dst_file.exists():
            existing = dst_file.read_text(encoding="utf-8")
            if SNIPPET_START in existing and SNIPPET_END in existing:
                pattern = re.compile(
                    re.escape(SNIPPET_START) + r".*?" + re.escape(SNIPPET_END),
                    re.DOTALL,
                )
                updated = pattern.sub(content.strip(), existing)
                dst_file.write_text(updated, encoding="utf-8")
                return f"updated snippet in {dst_file}"
            else:
                sep = "\n\n" if existing.strip() else ""
                dst_file.write_text(existing.rstrip() + sep + content.strip() + "\n", encoding="utf-8")
                return f"appended snippet to {dst_file}"
        else:
            dst_file.write_text(content.strip() + "\n", encoding="utf-8")
            return f"created {dst_file}"

    def _uninstall_rule_file(self, dst_file: Path, is_snippet: bool) -> Optional[str]:
        """Removes or cleans a rule file. Returns action description if modified."""
        if not dst_file.exists():
            return None

        if self.dry_run:
            return f"would remove/clean {dst_file}"

        if not is_snippet:
            dst_file.unlink()
            # Clean parent if empty
            try:
                dst_file.parent.rmdir()
            except OSError:
                pass
            return f"removed {dst_file}"

        # Snippet removal
        existing = dst_file.read_text(encoding="utf-8")
        if SNIPPET_START in existing and SNIPPET_END in existing:
            pattern = re.compile(
                r"\n*" + re.escape(SNIPPET_START) + r".*?" + re.escape(SNIPPET_END) + r"\n*",
                re.DOTALL,
            )
            cleaned = pattern.sub("\n", existing).strip()
            if not cleaned:
                dst_file.unlink()
                return f"removed empty {dst_file}"
            else:
                dst_file.write_text(cleaned + "\n", encoding="utf-8")
                return f"removed snippet from {dst_file}"
        return None

    def install_target(self, target: TargetConfig) -> List[str]:
        """Installs the skill and adapters for a given target. Returns log messages."""
        logs = []
        skill_rel = target.project_skill_rel if self.scope == "project" else target.global_skill_rel
        rule_defs = target.project_rules if self.scope == "project" else target.global_rules

        # 1. Install Skill Directory
        if skill_rel and SKILL_SRC.exists():
            dst_skill = self.dest_root / skill_rel
            action = self._copy_or_link_dir(SKILL_SRC, dst_skill)
            logs.append(f"  {green('+')} Skill: {action}")
        elif not SKILL_SRC.exists():
            logs.append(f"  {red('x')} Error: Skill source not found at {SKILL_SRC}")

        # 2. Install Rule Adapters
        if self.with_rule:
            for rel_dest, adapter_src_rel, is_snippet in rule_defs:
                src_file = ADAPTERS_SRC / adapter_src_rel
                dst_file = self.dest_root / rel_dest
                action = self._install_rule_file(src_file, dst_file, is_snippet)
                logs.append(f"  {green('+')} Rule:  {action}")

        return logs

    def uninstall_target(self, target: TargetConfig) -> List[str]:
        """Uninstalls skill and rule adapters for a given target. Returns log messages."""
        logs = []
        skill_rel = target.project_skill_rel if self.scope == "project" else target.global_skill_rel
        rule_defs = target.project_rules if self.scope == "project" else target.global_rules

        # 1. Remove Skill Directory
        if skill_rel:
            dst_skill = self.dest_root / skill_rel
            if dst_skill.exists() or dst_skill.is_symlink():
                if dst_skill.resolve() == SKILL_SRC.resolve():
                    logs.append(f"  {yellow('!')} Skipped source repository skill directory at {dst_skill}")
                elif self.dry_run:
                    logs.append(f"  {cyan('~')} Would remove skill directory {dst_skill}")
                else:
                    if dst_skill.is_symlink() or dst_skill.is_file():
                        dst_skill.unlink()
                    else:
                        shutil.rmtree(dst_skill)
                    logs.append(f"  {red('-')} Removed skill directory {dst_skill}")

        # 2. Remove / Clean Rules
        for rel_dest, _, is_snippet in rule_defs:
            dst_file = self.dest_root / rel_dest
            res = self._uninstall_rule_file(dst_file, is_snippet)
            if res:
                logs.append(f"  {red('-')} {res}")

        return logs


def parse_targets(target_arg: str) -> List[TargetConfig]:
    if target_arg.lower() == "all":
        return list(TARGET_REGISTRY.values())

    keys = [k.strip().lower() for k in target_arg.split(",") if k.strip()]
    selected = []
    for k in keys:
        if k in TARGET_REGISTRY:
            selected.append(TARGET_REGISTRY[k])
        else:
            raise ValueError(f"Unknown target '{k}'. Supported: {', '.join(TARGET_REGISTRY.keys())}, all")
    return selected


def main():
    parser = argparse.ArgumentParser(
        prog="install.py",
        description="Install premium-docs skills, workflows, and rule adapters across AI agent platforms.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python install.py --target antigravity
  python install.py --target claude,cursor --scope project
  python install.py --target all --dry-run
  python install.py --target all --uninstall
        """,
    )
    parser.add_argument(
        "--target",
        "-t",
        default="all",
        help="Target platform(s): antigravity, claude, cursor, gemini, agents, copilot, windsurf, cline, or all (default: all)",
    )
    parser.add_argument(
        "--scope",
        "-s",
        choices=["project", "global"],
        default="project",
        help="Installation scope: 'project' (current workspace) or 'global' (user home directory). Default: project",
    )
    parser.add_argument(
        "--dest",
        "-d",
        type=str,
        default=None,
        help="Custom destination directory root. Defaults to current directory for project scope, or ~ for global scope.",
    )
    parser.add_argument(
        "--with-rule",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Install rule/workflow snippets alongside the skill (default: --with-rule)",
    )
    parser.add_argument(
        "--symlink",
        action="store_true",
        help="Create symlink instead of copying skill folder (falls back to copy if unsupported)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate actions without modifying files",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Uninstall skill and clean adapter snippets for specified target(s)",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Overwrite existing files without prompting",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List all supported targets and exit",
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"premium-docs {VERSION}",
    )

    args = parser.parse_args()

    # List mode
    if args.list:
        print(bold(f"\npremium-docs v{VERSION} Supported Platforms:\n"))
        for k, v in TARGET_REGISTRY.items():
            print(f"  {cyan(k.ljust(12))} : {bold(v.display_name)}")
            print(f"                 Project Skill: {v.project_skill_rel}")
            print(f"                 Global Skill:  {v.global_skill_rel}")
        print()
        return 0

    # Determine destination root
    if args.dest:
        dest_root = Path(args.dest)
    else:
        dest_root = Path.home() if args.scope == "global" else Path.cwd()

    try:
        targets = parse_targets(args.target)
    except ValueError as e:
        print(f"{red('Error:')} {e}", file=sys.stderr)
        return 1

    mode_label = "DRY-RUN " if args.dry_run else ""
    action_label = "Uninstalling" if args.uninstall else "Installing"

    print()
    print(bold(f"=== {mode_label}premium-docs Installer v{VERSION} ==="))
    print(f"Action: {cyan(action_label)}")
    print(f"Scope:  {cyan(args.scope)} ({dest_root})")
    print(f"Target: {cyan(', '.join(t.display_name for t in targets))}")
    if args.dry_run:
        print(f"Mode:   {yellow('DRY RUN (no files modified)')}")
    print()

    installer = Installer(
        dest_root=dest_root,
        scope=args.scope,
        dry_run=args.dry_run,
        with_rule=args.with_rule,
        use_symlink=args.symlink,
        force=args.force,
    )

    total_logs = []
    for t in targets:
        print(bold(f"[{t.display_name}]"))
        if args.uninstall:
            logs = installer.uninstall_target(t)
        else:
            logs = installer.install_target(t)
        for line in logs:
            print(line)
        total_logs.extend(logs)
        print()

    status_str = "Preview complete." if args.dry_run else "Done!"
    print(green(bold(f"OK: {status_str} Successfully processed {len(targets)} target(s).")))
    if not args.uninstall and not args.dry_run:
        print("\nNext step: Try compiling a doc with:")
        print(cyan("  python skills/premium-docs/scripts/build_doc.py <input.md> -o <output.html>"))
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
