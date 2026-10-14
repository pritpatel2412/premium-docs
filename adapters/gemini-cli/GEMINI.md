<!-- BEGIN PREMIUM-DOCS -->
## Visual Documentation (premium-docs)

When asked to produce reports, specs, PRDs, guides, or post-mortems:
- Use the `premium-docs` skill at `.gemini/skills/premium-docs/` or `skills/premium-docs/`.
- Author content in Markdown using container blocks (`:::tldr`, `:::stats`, `:::card-grid`, `:::callout`, `:::steps`, `:::timeline`, `:::tabs`, `:::table-wrap`).
- Compile to standalone HTML:
  `python <path_to_skill>/scripts/build_doc.py <input.md> -o <output.html>`
- Validate output:
  `python <path_to_skill>/scripts/validate_doc.py <output.html>`
- Deliver self-contained, themeable HTML with zero external network requests.
<!-- END PREMIUM-DOCS -->
