# Markdown Syntax & Container Specification

Complete syntax specification with copy-paste templates for all containers, frontmatter attributes, and markdown extensions in `premium-docs`.

---

## 1. YAML Front Matter

Placed at the very beginning of the document between `---` fences:

```yaml
---
title: Engineering Architecture Report
subtitle: High-throughput ingestion and cache invalidation
author: Staff Engineering Team
date: October 2026
status: final          # draft | review | final
tags: [Architecture, Performance, Distributed-Systems]
theme: aurora          # aurora | slate | paper
accent: "#6366f1"      # optional custom hex override
toc: true              # true | false
cover: false           # true | false
mode: auto             # auto | light | dark
---
```

---

## 2. Docusaurus-Style Containers (`:::type [Title]`)

All containers begin with `:::type Optional Title` and terminate with `:::`. Arbitrary nesting of containers and markdown is supported.

### A. Callouts (note, tip, info, success, warning, danger)
```markdown
:::info Informational Notice
Standard informational callout for important contextual notes.
:::

:::tip Performance Recommendation
Enable persistent connection pooling to reduce handshake overhead by 40%.
:::

:::warning Deprecation Alert
Legacy authentication tokens will be decommissioned in Q4 2026.
:::

:::danger Critical Security Warning
Do not expose internal cluster ports to the public gateway without mTLS.
:::
```

### B. TL;DR (Executive Summary)
```markdown
:::tldr Executive Summary
The distributed cache invalidation system achieves a 99.995% delivery rate with global propagation under 250 milliseconds.
:::
```

### C. Cards Grid
Delimit cards with `---`. An optional `### Title` at the beginning of a card is styled as a header:
```markdown
:::cards
### Ingest Gateway
Validates incoming signatures and deduplicates event payloads.
---
### Streaming Cluster
Maintains partition logs across multi-availability zones.
---
### Local Daemon
Applies real-time evictions to local cache memory pools.
:::
```

### D. Stats Tiles
Lines formatted as `value | label | delta` (delta is optional; `+` or `-` sets color):
```markdown
:::stats
99.995% | Uptime SLA | +0.05% vs Q1
14.2ms | p99 Latency | -3.8ms improvement
4.2M | Req / Sec | Peak throughput
0.001% | Error Rate | Stable
:::
```

### E. Steps Process
Sequential workflow where each step begins with `### Step Title` or `1. ...`:
```markdown
:::steps
### Configure IAM Permissions
Grant the edge worker service account read access to the invalidation topic.
### Deploy Worker Daemon
Apply the daemonset configuration across all edge clusters.
### Verify Local Probe
Ensure health checks respond with HTTP 200 on port 9090.
:::
```

### F. Accessible Tabs
Child panels delimited with `@tab Tab Name`:
```markdown
:::tabs
@tab Python Client
```python title="client.py"
from invalidation import Invalidator
client = Invalidator(endpoint="https://cache.internal")
client.evict("user:1234")
```
@tab Go Client
```go title="client.go"
client, err := invalidation.NewClient("https://cache.internal")
client.Evict(ctx, "user:1234")
```
:::
```

### G. Compare Grid
Side-by-side comparison columns delimited by `---`:
```markdown
:::compare
### Pro: Pub/Sub Model
- Sub-second global propagation
- Zero cache stampede on updates
- Predictable database loads
---
### Con: Passive TTL
- Significant data staleness window
- Stampede spikes when popular keys expire
- Unnecessary database load
:::
```

### H. FAQ Accordion
Collapsible questions where each question begins with `### Question`:
```markdown
:::faq
### Does this document work completely offline?
Yes. All CSS, JS, Lucide SVG icons, and fonts are inlined directly into a single self-contained HTML file.

### How do I print to PDF?
Click the print icon in the top header or press Ctrl+P / Cmd+P. The print stylesheet automatically expands tabs, hides chrome, and optimizes layout.
:::
```

### I. File Tree
Directory structure representation with folder and file icons:
```markdown
:::filetree
premium-docs/
├── skills/premium-docs/     # The primary agent skill
│   ├── SKILL.md             # Progressive disclosure entrypoint
│   ├── assets/              # Inlined CSS, JS, icons
│   └── scripts/             # build_doc.py & validate_doc.py
├── adapters/                # Platform adapters (Antigravity, Claude, Cursor)
└── install.py               # Cross-platform installer
:::
```

### J. Key-Value Grid
Two-column metadata grid where each line is `Key | Value`:
```markdown
:::kv
Engine Version    | v0.1.0
Target Platform   | Cross-platform (Windows, macOS, Linux)
Memory Footprint  | Under 35 MB
License           | MIT License
:::
```

### K. Progress Bars
Progress bars where each line is `Label | Percentage%`:
```markdown
:::progress
Architecture Specification | 100%
Compiler Pipeline          | 100%
Agent Skills & Recipes     | 100%
Visual QA Across Viewports | 100%
:::
```

### L. Timeline
Sequential milestones or post-mortem incident chronology:
```markdown
:::timeline
14:02 UTC | Alarm Triggered | Automated alert fired for elevated error rate on API gateway.
14:08 UTC | On-Call Engaged | Primary engineer initiated diagnostic runbook and identified node deadlock.
14:15 UTC | Rollback Executed | Reverted to previous release candidate; error rates normalized within 90 seconds.
:::
```

---

## 3. Standard Markdown Enhancements

### A. Code Blocks with Titles & Copy Buttons
Use the `title="filename.ext"` attribute to add an elevated filename header bar with an instant copy button:
````markdown
```python title="scripts/worker.py"
def process_task():
    return True
```
````

### B. Responsive Tables
Tables automatically receive responsive horizontal scrolling containers with sticky headers:
```markdown
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `theme` | string | `aurora` | Theme palette (`aurora`, `slate`, `paper`) |
| `toc` | boolean | `true` | Enables sticky Table of Contents |
| `accent` | hex | `None` | Custom accent override |
```

### C. Task Lists
```markdown
- [x] Phase 1 completed
- [x] Phase 2 completed
- [ ] Phase 3 in progress
```

### D. Footnotes
```markdown
This architectural decision[^1] was ratified by the committee.

[^1]: See RFC-2026 for complete benchmark data and telemetry.
```
