# premium-docs

> **Publication-Grade, Self-Contained HTML Documents for AI Coding Agents.**  
> Turn plain Markdown reports, PRDs, guides, specs, runbooks, and post-mortems into stunning, zero-dependency HTML deliverables that work 100% offline.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-brightgreen.svg)](https://www.python.org/)
[![Offline: 0 CDN Requests](https://img.shields.io/badge/Offline-Zero%20CDN%20Requests-success.svg)](#offline--privacy-guarantee)
[![Accessibility: WCAG AA](https://img.shields.io/badge/Accessibility-WCAG%20AA%20Certified-indigo.svg)](#accessibility--contrast)
[![Platforms: 8 Supported](https://img.shields.io/badge/Platforms-8%20Agent%20Ecosystems-blueviolet.svg)](#supported-platforms)

---

## Why premium-docs?

Paid AI tools (Claude Code, Cursor, and enterprise platforms) often turn technical discussions into polished HTML documents with color, visual hierarchy, stats, and interactive components. Developers on open and free tools (Google Antigravity, Gemini CLI, OpenHands, Cline) often get plain `.md` files that are difficult to scan and share with leadership.

**premium-docs closes that gap.**

In under 60 seconds, install the skill into your coding agent. Then simply prompt:
> *"Produce a technical architecture report on our new caching service"*

Your agent authors rich, structured Markdown with semantic container blocks, and compiles a single, self-contained HTML file. Open it in any browser or print it to PDF—no local server, build tool, or internet connection required.

---

## Key Features

- 🌐 **100% Offline & Self-Contained**: Inlines all CSS, lightweight JS, and Lucide SVG icons directly into one single `.html` file. Zero runtime CDN requests.
- 🎨 **3 Curated Design Systems**:
  - **`aurora`**: Modern tech gradient (indigo/violet/sky) for architecture reports, feature specs, and engineering roadmaps.
  - **`slate`**: Clean corporate engineering theme (slate blue/teal) for incident post-mortems, RFCs, and enterprise documentation.
  - **`paper`**: Warm editorial serif theme (warm amber/ink) for long-form handbooks, guides, and technical books.
- 🌓 **Automatic Dark & Light Modes**: System preference auto-detection (`prefers-color-scheme`) with an interactive header toggle and persistence.
- ♿ **WCAG AA Certified**: Mathematical contrast ratio verification (≥ 4.5:1 text-to-canvas contrast across all themes).
- 📱 **Responsive Multi-Viewport Layout**: Desktop sticky table-of-contents with scroll-spy, tablet reflow, and mobile slide-out drawer menu.
- ⚡ **Interactive Components**: Accessible keyboard-navigable tabs, copy-to-clipboard code blocks with Pygments syntax highlighting, collapsible FAQ accordions, and print-to-PDF styles.
- 🤖 **Universal Multi-Agent Support**: Ready-to-use workflows and adapters for 8 major AI agent ecosystems.

---

## Supported Platforms

| Platform | Project Scope Location | Global Scope Location | Adapter Rule File |
| :--- | :--- | :--- | :--- |
| **Google Antigravity** | `.agents/skills/premium-docs/` | `~/.gemini/config/skills/premium-docs/` | `.agents/workflows/premium-doc.md`, `.agents/rules/` |
| **Claude Code** | `.claude/skills/premium-docs/` | `~/.claude/skills/premium-docs/` | `CLAUDE.md` |
| **Cursor** | `.cursor/skills/premium-docs/` | `~/.cursor/skills/premium-docs/` | `.cursor/rules/premium-docs.mdc` |
| **Gemini CLI** | `.gemini/skills/premium-docs/` | `~/.gemini/skills/premium-docs/` | `GEMINI.md` |
| **AGENTS.md / Codex** | `skills/premium-docs/` | `~/.agents/skills/premium-docs/` | `AGENTS.md` |
| **GitHub Copilot** | `.github/skills/premium-docs/` | `~/.config/github-copilot/skills/` | `.github/copilot-instructions.md` |
| **Codeium Windsurf** | `.windsurf/skills/premium-docs/` | `~/.codeium/windsurf/skills/` | `.windsurfrules` |
| **Cline / Roo-Code** | `.cline/skills/premium-docs/` | `~/.cline/skills/premium-docs/` | `.clinerules` |

---

## 60-Second Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/pritpatel2412/premium-docs.git
cd premium-docs
```

### Step 2: Run Universal Installer
Install across all 8 agent platforms simultaneously:
```bash
python install.py --target all
```

Or install specifically for your active tool:
```bash
# Google Antigravity
python install.py --target antigravity

# Claude Code
python install.py --target claude

# Cursor
python install.py --target cursor

# Gemini CLI
python install.py --target gemini
```

### Installer Options
```bash
# Preview actions without modifying any files
python install.py --target all --dry-run

# Install globally to user home directory
python install.py --target claude --scope global

# Cleanly uninstall skill and remove injected config snippets
python install.py --target all --uninstall

# List all platform destination paths
python install.py --list
```

---

## Live Document Showcase

Four real-world production examples are pre-compiled and included:

| Archetype | Theme | Deliverable Size | Description |
| :--- | :--- | :--- | :--- |
| **Technical Architecture Report** | `aurora` | 76.9 KB | Distributed cache invalidation with stats, compare grid, and code snippets. |
| **Product Requirements (PRD)** | `slate` | 77.7 KB | Autonomous agent telemetry engine with accessible tabs and implementation steps. |
| **Developer Handbook & Guide** | `paper` | 75.1 KB | Development environment setup with interactive directory filetree and copy buttons. |
| **Incident Post-Mortem** | `slate` | 69.7 KB | High-severity authentication gateway outage with chronological timeline and metrics. |

All compiled HTML files are located under `skills/premium-docs/examples/`.

---

## Container Syntax Reference

`premium-docs` extends standard Markdown with clean Docusaurus-style container blocks (`:::type [Title]` ... `:::`).

### Executive Summary (`:::tldr`)
```markdown
:::tldr Executive Summary
The new cache invalidation engine delivers 99.995% reliability with global propagation under 250ms.
:::
```

### Metrics & Stats Tiles (`:::stats`)
```markdown
:::stats
99.995% | Uptime SLA | +0.05% vs Q1
14.2ms | p99 Latency | -3.8ms improvement
4.2M | Req / Sec | Peak throughput
0.001% | Error Rate | Stable
:::
```

### Callouts (`:::info`, `:::tip`, `:::warning`, `:::danger`, `:::note`, `:::success`)
```markdown
:::tip Performance Recommendation
Enable persistent HTTP/2 connection pooling to reduce SSL handshake overhead by 40%.
:::

:::warning Deprecation Alert
Legacy API tokens will be decommissioned in Q4 2026.
:::
```

### Cards Grid (`:::cards`)
```markdown
:::cards
### Ingestion Gateway
Validates incoming payload signatures and deduplicates events.
---
### Streaming Cluster
Maintains partitioned commit logs across multi-region availability zones.
---
### Local Daemon
Applies real-time memory pool evictions with zero GC pauses.
:::
```

### Sequential Steps (`:::steps`)
```markdown
:::steps
### Configure IAM Permissions
Grant the edge daemon read access to the cluster invalidation topic.
### Deploy DaemonSet
Apply Kubernetes daemonset manifests across all edge compute nodes.
### Run Verification Probe
Verify synthetic traffic probes respond with HTTP 200 on port 9090.
:::
```

### Accessible Tabs (`:::tabs`)
```markdown
:::tabs
@tab Python Client
```python title="client.py"
from cache import Invalidator
client = Invalidator(endpoint="https://cache.internal")
client.evict("user:1024")
```
@tab Go Client
```go title="client.go"
client, err := cache.NewClient("https://cache.internal")
client.Evict(ctx, "user:1024")
```
:::
```

### Comparison Grid (`:::compare`)
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

### Chronological Timeline (`:::timeline`)
```markdown
:::timeline
14:00 UTC | Alert Triggered | Automated monitor detected ingress latency spike.
14:08 UTC | Traffic Rerouted | Incident commander shifted traffic to standby cluster.
14:25 UTC | Hotfix Deployed | Memory pool exhaustion patched and verified.
:::
```

### Directory Structure (`:::filetree`)
```markdown
:::filetree
my-project/
├── src/
│   ├── core/
│   │   └── engine.py        # Core processing pipeline
│   └── main.py
└── pyproject.toml
:::
```

---

## CLI Tools

### 1. Document Compiler (`build_doc.py`)
Compile any Markdown file into standalone HTML:
```bash
python skills/premium-docs/scripts/build_doc.py input.md -o output.html
```

Options:
- `--theme aurora|slate|paper`: Override visual theme.
- `--mode auto|light|dark`: Set default color appearance.
- `--accent "#6366f1"`: Apply a custom brand hex accent color.
- `--no-toc`: Disable Table of Contents generation.
- `--fragment`: Treat input as an HTML fragment (Mode B).
- `--json`: Output build telemetry in JSON format.

### 2. Quality & Accessibility Validator (`validate_doc.py`)
Verify HTML deliverables meet all quality and privacy standards:
```bash
python skills/premium-docs/scripts/validate_doc.py output.html
```

Verification Gates:
- ✅ Single `<h1>` title check.
- ✅ Heading uniqueness and intact local `#anchor` links.
- ✅ Zero external URLs in `<script>`, `<link>`, or `<img>` (100% offline).
- ✅ Image `alt` accessibility tags.
- ✅ Mathematical WCAG AA contrast ratio verification (≥ 4.5:1).
- ✅ Leftover unparsed `:::` container detection.
- ✅ Deliverable file-size budget check (< 1MB).

---

## Offline & Privacy Guarantee

`premium-docs` adheres to a strict offline-first design:
- All CSS design systems, client scripts, and SVG icon sets are embedded directly into each file.
- The default output includes a strict Content Security Policy meta tag:
  ```html
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:; script-src 'unsafe-inline';">
  ```
- No analytics, tracking pixels, or third-party web fonts are ever loaded.

---

## Contributing

We welcome community contributions, custom themes, and new agent adapters!  
See [CONTRIBUTING.md](CONTRIBUTING.md) for local development setup and test guidelines.

---

## License & Attribution

- **Source Code**: Released under the [MIT License](LICENSE).
- **Icons**: Lucide icons are used under the [ISC License](THIRD_PARTY_NOTICES.md) courtesy of the Lucide Project contributors.
