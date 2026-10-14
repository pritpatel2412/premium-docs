# Changelog

All notable changes to the `premium-docs` project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-10-14

### Added
- **Design System & Shell**:
  - Inlined base typography, elevation shadows, fluid spacing, and responsive layout foundations.
  - Three curated WCAG AA themes: `aurora` (modern gradient tech), `slate` (clean corporate engineering), and `paper` (warm editorial serif).
  - Client engine (`app.js`) featuring safe storage theme switcher, TOC scroll-spy, mobile drawer, accessible keyboard tabs, and code copy buttons.
  - Inlined Lucide SVG icon set with zero runtime CDN dependencies.
- **AST Compiler Pipeline (`build_doc.py`)**:
  - Docusaurus-style container AST stack parser with precise line-accurate syntax error reporting.
  - Support for `:::tldr`, `:::stats`, `:::cards`, `:::callouts`, `:::steps`, `:::tabs`, `:::compare`, `:::timeline`, `:::faq`, `:::filetree`, `:::kv`, and `:::progress`.
  - Pygments syntax highlighting on code blocks with filename badges.
  - Auto-generated unique heading IDs, interactive anchor links, and responsive table wrappers.
  - Mode A (full standalone document) and Mode B (`--fragment` HTML wrapper).
- **Document Quality Validator (`validate_doc.py`)**:
  - Verification gates for single `<h1>`, unique IDs, intact local `#anchors`, and image `alt` tags.
  - Mathematical WCAG 2.1 AA text-to-canvas contrast ratio verification (≥ 4.5:1).
  - Strict offline enforcement prohibiting external URLs in `<script>`, `<link>`, or `<img>`.
  - Checks for unparsed leftover `:::` container markers.
- **Agent Skill & Progressive Disclosure**:
  - `skills/premium-docs/SKILL.md` (< 500 lines) with a 7-step progressive disclosure workflow.
  - References: `design-principles.md`, `components.md`, `doc-recipes.md` (13 archetypes), `markdown-syntax.md`, and `accessibility-print.md`.
- **Dogfooding Showcase Deliverables**:
  - 4 production examples: `technical-report.html`, `prd-feature-spec.html`, `project-guide.html`, and `incident-postmortem.html`.
  - Multi-viewport visual QA across 1440px (desktop), 768px (tablet), and 375px (mobile) in light and dark modes.
- **Installer & Platform Adapters (`install.py`)**:
  - Universal zero-dependency Python installer with `--target`, `--scope`, `--with-rule`, `--dry-run`, and `--uninstall`.
  - Ready-to-use adapter configurations for Google Antigravity, Claude Code, Cursor, Gemini CLI, Codex/AGENTS.md, GitHub Copilot, Codeium Windsurf, and Cline.
  - Non-destructive snippet merging with `<!-- BEGIN PREMIUM-DOCS -->` markers.
- **Quality Assurance & CI/CD**:
  - 41 automated pytest unit and integration tests across converters, validators, installers, and contrast ratios.
  - Multi-OS GitHub Actions CI workflow (Ubuntu, Windows, macOS on Python 3.9 & 3.12).
  - GitHub Pages deployment workflow with static showcase gallery (`site/`).
