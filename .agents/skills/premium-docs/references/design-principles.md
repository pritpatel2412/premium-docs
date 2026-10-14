# Design Principles for premium-docs

The `premium-docs` visual language is engineered to feel **calm, confident, and editorial**. It draws inspiration from premier technical publications and modern product engineering documentation. It avoids flashy, gimmick-laden layouts or generic CSS framework appearances.

---

## 1. Core Aesthetic Principles

### A. Restraint Over Decoration
- **Whitespace Over Borders**: Use comfortable padding (`--space-6` to `--space-8`) and whitespace to group related concepts instead of wrapping everything in heavy borders.
- **Maximum 2 Accent Hues**: Restrict each document to the primary theme accent plus semantic feedback colors (`success`, `warning`, `danger`, `info`). Avoid rainbow styling.
- **No Emoji Clutter**: Never use raw emojis in titles or section headers. Use the curated inline SVG icons (`<svg><use href="#icon-..."></use></svg>`) for consistent stroke weight and rendering across operating systems.
- **One Visual Idea Per Section**: Avoid stacking multiple heavy containers (e.g. stats grid immediately followed by cards and tabs). Let prose breathe between structured components.

### B. Typographic Hierarchy & Measure
- **Comfortable Measure**: The prose reading measure is capped at `~72ch` (`--measure`). Reading lines that span full widescreen monitors cause visual fatigue.
- **System Font Stacks**: Zero external font dependencies (no Google Fonts network calls). Uses optimized native system stacks:
  - Sans: Apple SF Pro / Segoe UI / Roboto
  - Serif: Charter / Cambria / Georgia (in `paper` theme)
  - Mono: SF Mono / Cascadia Code / Menlo / Consolas
- **Tight Headings, Relaxed Body**: Headings have tight letter-spacing (`-0.02em`) and snug line-height (`1.25`); body text has relaxed line-height (`1.65` to `1.7`) for maximum legibility.

### C. Contrast & Accessibility (WCAG AA)
- Every theme and mode guarantees text contrast of at least **4.5:1** for normal text and **3.0:1** for large headings and UI controls.
- Color is never the sole conveyor of information (icons, labels, and text accompany status badges and delta metrics).
- High-visibility keyboard focus rings (`outline: 2px solid var(--accent); outline-offset: 3px`) are maintained across all interactive elements.

### D. Offline & Privacy Sovereignty
- Output is strictly **one self-contained HTML file**.
- No external CDNs, tracking pixels, or third-party web fonts.
- Guarded by default with a strict Content Security Policy meta header:
  ```html
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:; script-src 'unsafe-inline';">
  ```

---

## 2. Component Placement Rules

| Component | Recommended Usage | Avoid |
| :--- | :--- | :--- |
| **`:::tldr`** | Immediate opening under document header. Summarizes core findings, objectives, or actions. | Placing inside middle or ending sections. |
| **`:::stats`** | Executive dashboards, SLA metrics, benchmark comparisons, performance summaries. | Using for qualitative or subjective lists. |
| **`:::cards`** | Architectural subsystems, feature highlights, modular concepts (3 columns max). | Storing full paragraphs of dense text. |
| **`:::steps`** | Sequential runbooks, procedural onboarding, release pipelines. | Non-linear or unordered points. |
| **`:::tabs`** | Multi-language code samples (Python/Go/TypeScript), platform setups (Linux/macOS/Windows). | Long sequential reading material that gets hidden. |
| **`:::compare`** | Architecture decision trade-offs, Pros vs Cons, Old vs New comparisons. | Generic two-column text without contrasting intent. |
| **`:::filetree`** | Directory structure overviews, repository maps. | File listings exceeding 35 lines. |
| **`:::faq`** | Troubleshooting, common edge cases, onboarding questions. | Essential primary documentation that must be seen upfront. |

---

## 3. Theme Selection Guidance

- **`aurora`** *(Default)*: Modern indigo-violet tech gradient. Best for software architecture, developer guides, PRDs, and modern technical specifications.
- **`slate`**: Monochromatic, neutral, calm charcoal aesthetic. Best for enterprise reports, security audits, compliance reviews, and formal post-mortems.
- **`paper`**: Warm editorial serif with ivory/espresso paper-tinted background. Best for whitepapers, strategy proposals, research summaries, and long-form narrative readouts.
