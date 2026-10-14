<!-- BEGIN PREMIUM-DOCS -->
## Premium HTML Documentation (premium-docs)

When asked to create reports, specs, PRDs, architecture guides, runbooks, post-mortems, or visual documentation:
- Refer to the `premium-docs` skill at `.claude/skills/premium-docs/` (or `skills/premium-docs/`).
- Structure documents in Markdown with full YAML frontmatter (`title`, `subtitle`, `date`, `version`, `theme: aurora|slate|paper`, `mode: auto|light|dark`).
- Use rich visual container blocks instead of plain text:
  - `:::tldr` for executive summary
  - `:::stats` with `[stat: number, label, delta]`
  - `:::card-grid` with `:::card`
  - `:::badge [variant]` (primary, success, warning, danger, neutral)
  - `:::timeline` with `:::timeline-item`
  - `:::callout [info|success|warning|danger|tip]`
  - `:::steps` with `:::step`
  - `:::table-wrap` for responsive tables
  - `:::tabs` with `:::tab [Title]`
- Compile to standalone HTML:
  `python <path_to_skill>/scripts/build_doc.py <document.md> -o <document.html>`
- Validate output:
  `python <path_to_skill>/scripts/validate_doc.py <document.html>`
- All generated HTML files are 100% self-contained and offline-ready with zero external CDN dependencies.
<!-- END PREMIUM-DOCS -->
