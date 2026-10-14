---
description: Generate publication-grade, self-contained HTML documents (reports, PRDs, architecture guides, runbooks, post-mortems)
---

# Workflow: /premium-doc

Generate a publication-grade, self-contained, responsive HTML document from markdown using the `premium-docs` design system.

## 1. Understand the Request
Determine the document archetype and reader requirements:
- **Archetype**: Technical Report, PRD/Feature Spec, Architecture Guide, Developer Setup/Runbook, Incident Post-Mortem, RFC, Executive Brief, Comparison Matrix, Release Notes, API Reference, Style Guide, Whitepaper, or Changelog.
- **Theme**:
  - `aurora`: Modern gradient tech theme (indigo/violet/sky), ideal for tech reports, specs, and modern products.
  - `slate`: Clean corporate engineer theme (slate blue/cool teal), ideal for incident post-mortems, enterprise docs, and RFCs.
  - `paper`: Warm editorial serif theme (warm amber/ink), ideal for long-form guides, whitepapers, and manuals.
- **Color Mode**: `auto` (follows OS preference, default), `dark`, or `light`.

## 2. Review Component Recipes
Check the `premium-docs` skill references:
- Check `skills/premium-docs/SKILL.md` (or `.agents/skills/premium-docs/SKILL.md`)
- Review `references/doc-recipes.md` for the chosen archetype
- Review `references/components.md` for container syntax:
  - `:::tldr` for executive summary
  - `:::stats` with `[stat: number, label, delta]`
  - `:::card-grid` with `:::card`
  - `:::badge [variant]` (primary, success, warning, danger, neutral)
  - `:::timeline` with `:::timeline-item`
  - `:::callout [info|success|warning|danger|tip]`
  - `:::steps` with `:::step`
  - `:::table-wrap` for responsive tables
  - `:::tabs` with `:::tab [Title]`
  - `:::filetree` for directory structures

## 3. Draft Markdown Content
Create the document markdown file (e.g., `docs/<topic>.md`) with full YAML frontmatter:
```yaml
---
title: "Document Title"
subtitle: "Clear, concise subtitle explaining context"
date: "YYYY-MM-DD"
version: "1.0"
author: "Author Name"
theme: "aurora" # aurora | slate | paper
mode: "auto"    # auto | light | dark
toc: true
---
```
Ensure content starts with a `:::tldr` container and concludes with actionable next steps.

## 4. Compile to Standalone HTML
Run the compiler script:
```bash
python skills/premium-docs/scripts/build_doc.py docs/<topic>.md -o docs/<topic>.html
```
*(If installed in `.agents/skills/premium-docs/`, adjust path accordingly).*

## 5. Validate Output
Run the validator:
```bash
python skills/premium-docs/scripts/validate_doc.py docs/<topic>.html
```
Ensure 0 errors: single H1, valid anchor links, WCAG AA contrast (≥ 4.5:1), and zero CDN network dependencies.

## 6. Deliver to User
Provide the user with:
- The compiled standalone HTML path: `docs/<topic>.html`
- A summary of document archetype, theme, and key sections
- Confirmation that the file is 100% self-contained and offline-ready.
