# Accessibility & Print Specifications

This document outlines the accessibility compliance standards and print media styling built into `premium-docs`.

---

## 1. Web Content Accessibility Guidelines (WCAG 2.1 AA)

All documents generated with `premium-docs` comply with **WCAG 2.1 Level AA** standards by default:

### A. Contrast Ratios
- **Body & Prose Text**: Minimum contrast ratio of **4.5:1** against underlying surfaces.
- **Large Text & Headings** (≥ 18pt / 24px): Minimum contrast ratio of **3.0:1**.
- **Interactive UI & Focus States**: Minimum contrast ratio of **3.0:1** for borders, focus rings, and active tab indicators.
- Verified mathematically via `validate_doc.py` for both Light and Dark modes across all themes (`aurora`, `slate`, `paper`).

### B. Heading Structure & Landmarks
- Exactly **one `<h1>`** per document (the document title), ensuring screen readers have an unambiguous root landmark.
- Hierarchical subheadings (`<h2>`, `<h3>`, `<h4>`) without level-skipping.
- Semantic HTML5 landmarks:
  - `<header role="banner">` (top navigation and action bar)
  - `<main role="main">` (prose reading content)
  - `<aside aria-label="Table of contents">` (document sidebar navigation)
  - `<footer role="contentinfo">` (document metadata)
  - `<div role="region" aria-label="...">` on callouts and TL;DR panels.

### C. Keyboard Accessibility
- **Skip Link**: Hidden top link (`Skip to content`) appears on first Tab press, allowing keyboard users to bypass navigation directly to the primary prose.
- **Focus Rings**: High-contrast, non-obtrusive focus indicators (`outline: 2px solid var(--accent); outline-offset: 3px`) on all interactive buttons, links, and form elements.
- **ARIA Tabs**: Keyboard-navigable tab panels following W3C patterns (ArrowLeft/ArrowRight cycle tabs; Home/End jump to first/last; Enter/Space activates).
- **Collapsible FAQ**: Native `<details><summary>` elements accessible via standard Space/Enter keyboard triggers.

### D. Reduced Motion
- Respects `prefers-reduced-motion: reduce`. Disables CSS transitions, animations, and smooth scrolling for users sensitive to vestibular motion.

---

## 2. Print & PDF Styling (`@media print`)

When a user prints the document (via header print icon or Ctrl+P / Cmd+P) or exports to PDF:

1. **Chrome Elimination**:
   - The desktop TOC, mobile drawer, reading progress bar, action buttons, theme toggles, code copy buttons, and back-to-top links are automatically hidden.
2. **Expansion of Hidden Content**:
   - All tab panels are expanded and rendered sequentially.
   - All `<details>` accordions are forced open so no critical content is hidden from paper output.
3. **Page-Break Optimization**:
   - `break-inside: avoid` and `page-break-inside: avoid` are applied to cards, tables, callouts, and code blocks to prevent awkward mid-element page tears.
4. **Link Citations**:
   - External hyperlinks print their target URL in parentheses following the anchor text:
     ```css
     a[href^="http"]::after {
       content: " (" attr(href) ")";
       font-size: 0.85em;
       color: #666;
     }
     ```
5. **Ink-Friendly Palette**:
   - Background colors are stripped to pure white (`#ffffff`) and text is rendered in deep black (`#000000`), minimizing toner consumption while maximizing readability.
