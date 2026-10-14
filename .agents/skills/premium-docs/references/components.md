# Component Reference Catalog

This guide provides the functional purpose and design parameters for each container and UI element in the `premium-docs` design system.

---

## 1. Callouts (`:::note`, `:::tip`, `:::info`, `:::success`, `:::warning`, `:::danger`)
- **Purpose**: Highlight non-linear editorial notes, warnings, best practices, and alerts.
- **Visual Presentation**: Soft background tint, distinct 4px colored indicator border on the left, Lucide SVG icon, and semantic header text.
- **Usage**:
  ```markdown
  :::note Important Context
  Background explanation or context for the reader.
  :::
  ```

---

## 2. TL;DR (`:::tldr`)
- **Purpose**: Executive overview placed at the very top of a document.
- **Visual Presentation**: Prominent card elevation, top accent gradient bar, lightning badge, and slightly larger body text.
- **Usage**:
  ```markdown
  :::tldr Executive Summary
  Key decisions, impact metrics, and high-level takeaways.
  :::
  ```

---

## 3. Cards Grid (`:::cards`)
- **Purpose**: Modular display of discrete concepts, modules, or feature sets.
- **Visual Presentation**: Responsive CSS grid (280px minimum column width), subtle border, soft shadow, and hover lift elevation.
- **Usage**: Separate cards with `---`. Optional `### Title` at the start of each card:
  ```markdown
  :::cards
  ### Ingestion Pipeline
  Handles incoming webhook events with rate-limiting and validation.
  ---
  ### Processing Worker
  Consumes partition queues and persists normalized records.
  :::
  ```

---

## 4. Stats Tiles (`:::stats`)
- **Purpose**: Display numerical KPIs, SLAs, benchmarks, or impact numbers.
- **Visual Presentation**: Extra-bold large metric text (`2.25rem`), uppercase muted label, and trend delta pill (`positive`, `negative`, or `neutral`).
- **Usage**: Each line formatted as `value | label | delta`:
  ```markdown
  :::stats
  99.99% | Availability SLA | +0.05% vs Q1
  14.2ms | p99 Latency | -3.1ms improvement
  4.2M | Req / Sec | Peak throughput
  :::
  ```

---

## 5. Steps Process (`:::steps`)
- **Purpose**: Sequential workflows, runbook procedures, and deployment stages.
- **Visual Presentation**: Numbered circular accent badges connected by a vertical timeline guide line.
- **Usage**:
  ```markdown
  :::steps
  ### Configure Environment
  Set up secrets and environment variables.
  ### Execute Database Migration
  Run the idempotent schema update.
  ### Deploy Application
  Deploy the new container image to the cluster.
  :::
  ```

---

## 6. Accessible Tabs (`:::tabs`)
- **Purpose**: Alternative configurations, programming languages, or operating system instructions.
- **Visual Presentation**: Horizontal tab bar with active indicator border and keyboard ARIA navigation (Arrow keys, Home, End).
- **Usage**: Delimit tabs with `@tab Tab Name`:
  ```markdown
  :::tabs
  @tab Python
  ```python
  client = APIClient()
  ```
  @tab TypeScript
  ```typescript
  const client = new APIClient();
  ```
  :::
  ```

---

## 7. Compare Grid (`:::compare`)
- **Purpose**: Trade-off evaluation, Pros vs Cons, or Option A vs Option B.
- **Visual Presentation**: Side-by-side columns with green (pro) and red (con) top borders and matching SVG badges.
- **Usage**:
  ```markdown
  :::compare
  ### Pro: Distributed Cache
  - Sub-millisecond reads
  - Resilient to primary database restarts
  ---
  ### Con: Operational Complexity
  - Cache invalidation race conditions
  - Memory capacity planning required
  :::
  ```

---

## 8. FAQ Accordion (`:::faq`)
- **Purpose**: Secondary questions, edge case clarifications, and troubleshooting steps.
- **Visual Presentation**: Collapsible `<details><summary>` cards with smooth rotating chevron indicator.
- **Usage**:
  ```markdown
  :::faq
  ### What happens during network partitions?
  Workers buffer events locally and replay on reconnection.
  ### Is authentication required?
  Yes, mutual TLS is enforced across all node endpoints.
  :::
  ```

---

## 9. File Tree (`:::filetree`)
- **Purpose**: Visual representation of repository directories and project layout.
- **Visual Presentation**: Monospaced font, folder and file SVG icons, indentation spacing, and styled comments.
- **Usage**:
  ```markdown
  :::filetree
  my-project/
  ├── src/
  │   ├── app.py          # Primary application entrypoint
  │   └── utils.py        # Shared helpers
  └── config.yaml         # Service configuration
  :::
  ```

---

## 10. Key-Value Grid (`:::kv`)
- **Purpose**: Metadata summaries, server specifications, or environment configurations.
- **Visual Presentation**: Clean 2-column or grid card with uppercase muted label and prominent value text.
- **Usage**:
  ```markdown
  :::kv
  Runtime Version | Python 3.12
  Memory Allocation | 4 GB
  Timeout Limit | 30 seconds
  :::
  ```

---

## 11. Progress Bars (`:::progress`)
- **Purpose**: Roadmap milestone tracking, migration completion, or capacity utilization.
- **Visual Presentation**: Label with percentage and animated rounded accent progress track.
- **Usage**:
  ```markdown
  :::progress
  Phase 1: Architecture | 100%
  Phase 2: Core Engine | 75%
  Phase 3: Integration Tests | 30%
  :::
  ```

---

## 12. Code Blocks with Filenames
- **Purpose**: Source code snippets with language badges, copy buttons, and syntax highlighting.
- **Usage**:
  ````markdown
  ```python title="service/worker.py"
  def start_worker():
      print("Worker running...")
  ```
  ````
