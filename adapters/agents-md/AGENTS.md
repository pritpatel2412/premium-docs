<!-- BEGIN PREMIUM-DOCS -->
## Documentation Generation (premium-docs)

When generating reports, PRDs, technical specifications, guides, runbooks, or post-mortems:
- Use `skills/premium-docs/SKILL.md` for styling guidelines, component syntax, and document recipes.
- Author Markdown with YAML frontmatter (`title`, `subtitle`, `date`, `version`, `theme: aurora|slate|paper`, `mode: auto|light|dark`).
- Format content using semantic containers (`:::tldr`, `:::stats`, `:::card-grid`, `:::badge`, `:::timeline`, `:::callout`, `:::steps`, `:::table-wrap`, `:::tabs`).
- Compile via:
  `python skills/premium-docs/scripts/build_doc.py <input.md> -o <output.html>`
- Validate via:
  `python skills/premium-docs/scripts/validate_doc.py <output.html>`
- Output is a standalone, offline single-file HTML document.
<!-- END PREMIUM-DOCS -->
