# Premium Docs Rule (Google Antigravity)

When the user asks to create, update, or compile rich documentation, reports, PRDs, architecture guides, runbooks, or post-mortems, or when producing HTML documentation:

1. **Activate the `premium-docs` skill**:
   - Skill location: `.agents/skills/premium-docs/` or `skills/premium-docs/`.
   - Read `SKILL.md` and appropriate recipes in `references/doc-recipes.md`.

2. **Structure the document**:
   - Write Markdown with YAML frontmatter (`title`, `subtitle`, `date`, `version`, `theme: aurora|slate|paper`, `mode: auto|light|dark`).
   - Use semantic container blocks (`:::tldr`, `:::stats`, `:::card-grid`, `:::badge`, `:::timeline`, `:::callout`, `:::steps`, `:::table-wrap`, `:::tabs`, `:::filetree`).
   - Never output raw inline CSS or ad-hoc HTML styling; rely strictly on container tags.

3. **Compile and Validate**:
   - Compile: `python skills/premium-docs/scripts/build_doc.py <input.md> -o <output.html>`
   - Validate: `python skills/premium-docs/scripts/validate_doc.py <output.html>`
   - Result is a publication-grade, self-contained single HTML file with zero runtime CDN requests.
