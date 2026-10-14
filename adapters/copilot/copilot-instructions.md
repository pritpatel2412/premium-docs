<!-- BEGIN PREMIUM-DOCS -->
## Documentation Authoring (premium-docs)

When asked to write documentation, reports, PRDs, architecture summaries, or post-mortems:
- Reference `skills/premium-docs/SKILL.md` for document recipes and container syntax.
- Structure content with YAML frontmatter (`title`, `subtitle`, `date`, `version`, `theme: aurora|slate|paper`, `mode: auto|light|dark`).
- Use semantic containers: `:::tldr`, `:::stats`, `:::card-grid`, `:::badge`, `:::callout`, `:::steps`, `:::timeline`, `:::tabs`, `:::table-wrap`.
- Compile to standalone HTML using:
  `python skills/premium-docs/scripts/build_doc.py <input.md> -o <output.html>`
- Validate using:
  `python skills/premium-docs/scripts/validate_doc.py <output.html>`
<!-- END PREMIUM-DOCS -->
