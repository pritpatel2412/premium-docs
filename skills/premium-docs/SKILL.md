---
name: premium-docs
description: Generates visually rich, self-contained HTML documents (reports, specs, PRDs, guides, READMEs, runbooks, post-mortems, comparisons, summaries) with a polished design system: sticky table of contents, callouts, cards, stat tiles, tabs, dark mode, print-ready. Use whenever the user asks for a document, report, plan, proposal, spec, guide, walkthrough or docs as a deliverable file, or asks to make an existing .md/.txt doc look better. Do NOT use for short chat answers, code comments, or when the user explicitly wants plain Markdown.
---

# premium-docs

Transform plain-text reports, plans, specs, and guides into publication-grade, self-contained HTML documents with a modern, calm, editorial design system.

---

## 1. When to Use & When NOT to Use

### Use This Skill When:
- The user asks for a formal deliverable: report, proposal, PRD, spec, design doc, architecture decision record (ADR), post-mortem, runbook, guide, or release notes.
- The user requests to "format", "polish", or "make an existing .md/.txt document look premium/beautiful".
- The deliverable will be shared with stakeholders, clients, managers, or teams.

### Do NOT Use When:
- Short conversational chat responses, single-line answers, or quick code fixes.
- Code comments, docstrings, or inline git commit messages.
- The user explicitly asks for "plain Markdown only" or "raw text".

---

## 2. The 7-Step Workflow

Follow this procedure sequentially for every document request:

1. **Select Recipe**: Choose the matching document archetype from [doc-recipes.md](references/doc-recipes.md) (e.g., Technical Report, PRD, Post-Mortem, Architecture Doc).
2. **Draft Outline**: Outline the document sections. Every document **MUST** begin with a `:::tldr` executive summary and conclude with a **Next Steps** section.
3. **Author Lean Markdown**: Write high-clarity Markdown using container blocks (`:::cards`, `:::stats`, `:::steps`, `:::tabs`, `:::compare`, `:::callout`, `:::faq`). **Never write inline CSS or JavaScript.**
4. **Save Source File**: Save the markdown content to `docs/<slug>.md`.
5. **Compile Standalone HTML**:
   Execute the build compiler using Python:
   ```bash
   python skills/premium-docs/scripts/build_doc.py docs/<slug>.md -o docs/<slug>.html --theme <aurora|slate|paper>
   ```
   *(If running from within an installed agent directory, adjust the relative path to `scripts/build_doc.py` accordingly).*
6. **Validate Quality & Accessibility**:
   Run the automated validator to ensure compliance:
   ```bash
   python skills/premium-docs/scripts/validate_doc.py docs/<slug>.html
   ```
   If any errors are reported (e.g. broken anchor, duplicate heading ID, missing alt text), fix them in `docs/<slug>.md` and recompile.
7. **Deliver Output**:
   Present the result to the user with the file path (`docs/<slug>.html`), highlight key conclusions, and offer to open the HTML document in their default browser.

---

## 3. Theme Selection Guidance

Select the theme matching the document's domain and audience:

| Theme | Tone & Palette | Best For |
| :--- | :--- | :--- |
| **`aurora`** *(Default)* | Modern tech gradient (indigo-violet) with crisp contrast. | Technical reports, product specifications, developer guides, PRDs. |
| **`slate`** | Neutral monochromatic architectural palette (slate/charcoal). | Enterprise audits, security reviews, RFCs, blameless post-mortems. |
| **`paper`** | Warm editorial serif with ivory/espresso paper tint. | Strategy memos, executive proposals, research summaries, whitepapers. |

*To apply a custom brand hue, pass `--accent "#hex"` to `build_doc.py`.*

---

## 4. Content & Authoring Rules

- **Zero Synthetic Data**: Never invent benchmarks, customer quotes, or statistics. If real data is unknown, explicitly mark placeholders (e.g., `[TBD: Benchmarking in progress]`).
- **Whitespace Over Borders**: Let prose breathe. Avoid nesting containers deeper than 2 levels.
- **Short, Punchy Paragraphs**: Limit paragraphs to 2–4 sentences (`~72ch` measure).
- **One Visual Idea Per Section**: Alternate between narrative text and visual containers (`stats`, `cards`, `compare`). Never stack three heavy container grids consecutively.
- **No Raw Emojis in Headings**: Use semantic SVG icons rather than emojis for headings.

---

## 5. 10-Item Design Self-Review Checklist

Before finalizing any document, confirm:
1. [ ] Exactly one `<h1>` title is present (derived from YAML frontmatter).
2. [ ] The document begins with an executive `:::tldr` container.
3. [ ] All numerical KPIs are grouped into a clean `:::stats` container.
4. [ ] Multi-part architectures or components use a responsive `:::cards` grid.
5. [ ] Alternative options or pros/cons are formatted using `:::compare`.
6. [ ] Code blocks specify both language and filename (e.g., ```` ```python title="app.py" ````).
7. [ ] Headings follow a strict logical hierarchy (`h2` -> `h3` -> `h4`) without skipping levels.
8. [ ] Contrast ratio is verified as WCAG AA compliant via `validate_doc.py`.
9. [ ] No unparsed leftover `:::` markers exist in the compiled output.
10. [ ] The document ends with actionable **Next Steps**.

---

## 6. Progressive Disclosure: Reference Guides

Consult the detailed references when needed:
- **[design-principles.md](references/design-principles.md)**: Visual philosophy, typography measure, restraint rules.
- **[components.md](references/components.md)**: Catalog of all 12 containers and UI components.
- **[doc-recipes.md](references/doc-recipes.md)**: Exact structural blueprints for 13 document types.
- **[markdown-syntax.md](references/markdown-syntax.md)**: Copy-paste container syntax reference.
- **[accessibility-print.md](references/accessibility-print.md)**: WCAG AA compliance and `@media print` rules.

---

## 7. Failure Handling & Troubleshooting

- **Missing `markdown` library**:
  If `build_doc.py` exits with an import error, run:
  ```bash
  pip install markdown
  ```
- **Syntax Error: Unclosed Container**:
  If `build_doc.py` reports `Line X: Unclosed container ':::type'`, check `docs/<slug>.md` around line X and verify that every opening `:::type` has a matching closing `:::`.
- **Validation Failure: Broken internal anchor**:
  If `validate_doc.py` flags broken anchors, verify that heading links match the slugified heading ID (e.g. `[Overview](#overview)` points to `## Overview`).

---

## 8. Few-Shot Authoring Examples

### Example 1: Architecture Decision Memo
```markdown
---
title: Cache Storage Engine Migration
subtitle: Transitioning from in-memory TTL to persistent log invalidation
author: Infrastructure Team
date: October 2026
status: final
theme: aurora
toc: true
---

:::tldr Executive Summary
Migrating from TTL cache expiration to persistent streaming invalidations reduces global edge latency from 15m to 250ms while cutting database load by 35%.
:::

## Key Performance Gains

:::stats
99.99% | Invalidation SLA | +0.4% vs Q1
< 250ms | Global Latency | -14.5s improvement
35% | Database Load | Net reduction
:::

## Comparison of Approaches

:::compare
### Pro: Active Invalidation
- Real-time consistency across 12 regions
- Eliminates thundering-herd database queries
---
### Con: Passive TTL Expiration
- Stale authorization state during cache windows
- Stampede spikes during peak traffic hours
:::

## Next Steps
1. Deploy invalidation daemon to staging cluster.
2. Conduct chaos-testing during synthetic AZ partition.
```

### Example 2: Product Requirements Summary
```markdown
---
title: Workspace Multi-Agent Orchestrator
subtitle: Feature specification for concurrent subagent leasing
author: Product Engineering
date: October 2026
status: review
theme: slate
toc: true
---

:::tldr Executive Summary
Enables developers to dispatch and monitor background subagents with isolated execution contexts and real-time status telemetry.
:::

## Core Capabilities

:::cards
### Parallel Task Leasing
Spawn up to 8 subagents concurrently to handle independent build, test, and lint tasks.
---
### Sandboxed Permissions
Each subagent executes inside restricted directory boundaries with granular command allowlists.
---
### Unified Event Bus
Real-time streaming telemetry and notification hooks connecting subagents to the user IDE.
:::

## Next Steps
- Finalize telemetry schema review with security leads.
- Ship alpha release to internal developer cohort.
```

### Example 3: Incident Post-Mortem
```markdown
---
title: Post-Mortem: Auth Service Outage
subtitle: Root-cause analysis and remediation for incident INC-8492
author: Reliability Engineering
date: October 2026
status: final
theme: slate
toc: true
---

:::tldr Incident Summary
A database connection pool exhaustion triggered a 7-minute auth gateway degradation affecting 1.2% of active API sessions. Zero credential data was compromised.
:::

## Incident Chronology

:::timeline
10:14 UTC | Elevated Latency | P99 latency exceeded 500ms threshold on auth gateway.
10:17 UTC | Alert Paged | On-call engineer acknowledged automated escalation.
10:21 UTC | Hotfix Applied | Pool limits dynamically expanded; error rate dropped to 0.00%.
:::

## Next Steps
- [ ] Add connection pool saturation alarms at 80% threshold.
- [ ] Implement circuit breaker pattern for database connection acquisitions.
```
