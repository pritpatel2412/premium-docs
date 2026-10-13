"""Helper script to assemble a comprehensive design system showcase HTML."""
import pathlib

def build_showcase(theme="aurora", mode="auto", out_file="docs/showcase.html"):
    assets_dir = pathlib.Path("skills/premium-docs/assets")
    shell = (assets_dir / "shell.html").read_text(encoding="utf-8")
    base_css = (assets_dir / "base.css").read_text(encoding="utf-8")
    comp_css = (assets_dir / "components.css").read_text(encoding="utf-8")
    theme_css = (assets_dir / f"themes/{theme}.css").read_text(encoding="utf-8")
    icons_svg = (assets_dir / "icons.svg").read_text(encoding="utf-8")
    app_js = (assets_dir / "app.js").read_text(encoding="utf-8")

    content_html = """
    <div class="tldr-box">
      <div class="tldr-header">
        <svg class="tldr-icon"><use href="#icon-zap"></use></svg>
        <span>Executive Summary</span>
      </div>
      <div class="tldr-body">
        <p><strong>premium-docs</strong> gives AI coding agents the capability to produce visually refined, self-contained HTML documents with zero external dependencies, total offline privacy, and WCAG AA compliance across desktop and mobile form factors.</p>
      </div>
    </div>

    <h2 id="key-metrics">Key Performance Metrics</h2>
    <p>Operational health across regional distributed storage clusters over the past 30 days:</p>
    <div class="stats-grid">
      <div class="stat-tile">
        <div class="stat-value">99.995%</div>
        <div class="stat-label">Availability SLA</div>
        <div class="stat-delta positive">
          <svg><use href="#icon-trending-up"></use></svg>
          <span>+0.04% vs Q1</span>
        </div>
      </div>
      <div class="stat-tile">
        <div class="stat-value">14.2ms</div>
        <div class="stat-label">p99 Latency</div>
        <div class="stat-delta positive">
          <svg><use href="#icon-trending-up"></use></svg>
          <span>-3.8ms improvement</span>
        </div>
      </div>
      <div class="stat-tile">
        <div class="stat-value">4.2M</div>
        <div class="stat-label">Req / Sec</div>
        <div class="stat-delta neutral">
          <svg><use href="#icon-activity"></use></svg>
          <span>Peak throughput</span>
        </div>
      </div>
      <div class="stat-tile">
        <div class="stat-value">0.001%</div>
        <div class="stat-label">Error Rate</div>
        <div class="stat-delta positive">
          <svg><use href="#icon-trending-up"></use></svg>
          <span>Under error budget</span>
        </div>
      </div>
    </div>

    <h2 id="feature-architecture">Architecture Components</h2>
    <p>The system is structured into four decoupled layers for resilient execution:</p>
    <div class="cards-grid">
      <div class="card-item">
        <div class="card-title">1. Content Authoring (Lean MD)</div>
        <div class="card-body">Agents author standard Markdown with YAML front matter and Docusaurus-style container blocks. Zero style pollution in prompt context.</div>
      </div>
      <div class="card-item">
        <div class="card-title">2. In-Memory Converter</div>
        <div class="card-body">A deterministic single-pass AST preprocessor that parses nested containers and inlines syntax tokens via Pygments.</div>
      </div>
      <div class="card-item">
        <div class="card-title">3. Self-Contained Shell</div>
        <div class="card-body">Embeds CSS custom properties, SVG symbols, and client JS directly into one standalone HTML file with strict CSP headers.</div>
      </div>
    </div>

    <h2 id="callouts-feedback">Semantic Callouts</h2>
    <div class="callout callout-info">
      <div class="callout-header">
        <svg class="callout-icon"><use href="#icon-info"></use></svg>
        <span class="callout-title">System Information</span>
      </div>
      <div class="callout-body">All stylesheets and assets are bundled directly into the output file. No runtime CDN requests or external tracker beacons are executed.</div>
    </div>

    <div class="callout callout-tip">
      <div class="callout-header">
        <svg class="callout-icon"><use href="#icon-lightbulb"></use></svg>
        <span class="callout-title">Optimization Tip</span>
      </div>
      <div class="callout-body">Enable the sticky TOC for documents longer than 1,000 words to provide readers effortless keyboard and scroll navigation.</div>
    </div>

    <div class="callout callout-warning">
      <div class="callout-header">
        <svg class="callout-icon"><use href="#icon-alert-triangle"></use></svg>
        <span class="callout-title">Deprecation Notice</span>
      </div>
      <div class="callout-body">The legacy single-file `.agent/` configuration will be retired in v0.3. Use the standardized `.agents/skills/` directory tree.</div>
    </div>

    <h2 id="interactive-tabs">Implementation Profiles</h2>
    <div class="tabs-container">
      <div class="tab-list" role="tablist">
        <button class="tab-button" role="tab" aria-selected="true" id="tab-1">Python Engine</button>
        <button class="tab-button" role="tab" aria-selected="false" id="tab-2">Agent Skill</button>
        <button class="tab-button" role="tab" aria-selected="false" id="tab-3">CLI Installer</button>
      </div>
      <div class="tab-panel" role="tabpanel" id="panel-1">
        <p>The build engine runs on Python 3.9+ using standard libraries and Python-Markdown. It handles recursive container trees and strict line-level error reporting.</p>
      </div>
      <div class="tab-panel" role="tabpanel" id="panel-2" hidden>
        <p>The Agent Skill is packaged under <code>skills/premium-docs/</code> with a concise <code>SKILL.md</code> under 500 lines adhering to progressive disclosure guidelines.</p>
      </div>
      <div class="tab-panel" role="tabpanel" id="panel-3" hidden>
        <p>The cross-platform installer <code>install.py</code> sets up symlinks or directory copies for Antigravity, Claude Code, Cursor, Gemini CLI, and other agent platforms.</p>
      </div>
    </div>

    <h2 id="comparison">Architectural Comparison</h2>
    <div class="compare-grid">
      <div class="compare-col compare-col-pro">
        <div class="compare-title">
          <svg style="width:18px;height:18px;"><use href="#icon-check-circle"></use></svg>
          <span>premium-docs Approach</span>
        </div>
        <div class="compare-body">
          <ul>
            <li>Single self-contained HTML file</li>
            <li>Zero external dependencies or CDNs</li>
            <li>Strict Content Security Policy</li>
            <li>WCAG AA contrast in light & dark modes</li>
            <li>Print-ready stylesheets</li>
          </ul>
        </div>
      </div>
      <div class="compare-col compare-col-con">
        <div class="compare-title">
          <svg style="width:18px;height:18px;"><use href="#icon-x-circle"></use></svg>
          <span>Traditional Doc Generators</span>
        </div>
        <div class="compare-body">
          <ul>
            <li>Heavy Node/Vite build toolchain required</li>
            <li>Fragile multi-file asset folders</li>
            <li>External Google Fonts and CDN scripts</li>
            <li>Broken mobile & print formatting</li>
            <li>Slow compile and complex setup</li>
          </ul>
        </div>
      </div>
    </div>

    <h2 id="code-sample">Code Demonstration</h2>
    <div class="code-block-wrapper">
      <div class="code-header">
        <div class="code-title">
          <svg><use href="#icon-file"></use></svg>
          <span>scripts/build_doc.py</span>
        </div>
        <div class="code-actions">
          <button class="copy-button" type="button" aria-label="Copy code">
            <svg><use href="#icon-copy"></use></svg>
            <span>Copy</span>
          </button>
        </div>
      </div>
      <pre><code><span class="highlight"><span class="k">from</span> <span class="nn">pathlib</span> <span class="k">import</span> <span class="n">Path</span>
<span class="k">import</span> <span class="nn">sys</span>

<span class="k">def</span> <span class="nf">build</span><span class="p">(</span><span class="n">input_path</span><span class="p">:</span> <span class="n">Path</span><span class="p">,</span> <span class="n">output_path</span><span class="p">:</span> <span class="n">Path</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
    <span class="c1"># Read markdown with YAML frontmatter</span>
    <span class="n">raw_text</span> <span class="o">=</span> <span class="n">input_path</span><span class="o">.</span><span class="n">read_text</span><span class="p">(</span><span class="n">encoding</span><span class="o">=</span><span class="s2">"utf-8"</span><span class="p">)</span>
    <span class="n">doc</span> <span class="o">=</span> <span class="n">parse_document</span><span class="p">(</span><span class="n">raw_text</span><span class="p">)</span>
    <span class="n">output_path</span><span class="o">.</span><span class="n">write_text</span><span class="p">(</span><span class="n">doc</span><span class="o">.</span><span class="n">to_html</span><span class="p">(),</span> <span class="n">encoding</span><span class="o">=</span><span class="s2">"utf-8"</span><span class="p">)</span>
    <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">"Built self-contained doc: </span><span class="si">{</span><span class="n">output_path</span><span class="si">}</span><span class="s2">"</span><span class="p">)</span>
</span></code></pre>
    </div>

    <h2 id="file-structure">Repository Structure</h2>
    <div class="filetree-container">
      <div class="filetree-line folder"><svg><use href="#icon-folder"></use></svg> premium-docs/</div>
      <div class="filetree-line folder">&nbsp;&nbsp;├── <svg><use href="#icon-folder"></use></svg> skills/premium-docs/ <span class="filetree-comment"># The agent skill</span></div>
      <div class="filetree-line file">&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── <svg><use href="#icon-file"></use></svg> SKILL.md</div>
      <div class="filetree-line folder">&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── <svg><use href="#icon-folder"></use></svg> assets/ <span class="filetree-comment"># Inlined CSS, JS, SVG</span></div>
      <div class="filetree-line folder">&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;├── <svg><use href="#icon-folder"></use></svg> scripts/ <span class="filetree-comment"># build_doc.py & validate_doc.py</span></div>
      <div class="filetree-line folder">&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;└── <svg><use href="#icon-folder"></use></svg> references/ <span class="filetree-comment"># Progressive disclosure guides</span></div>
      <div class="filetree-line folder">&nbsp;&nbsp;├── <svg><use href="#icon-folder"></use></svg> adapters/ <span class="filetree-comment"># Antigravity, Claude, Cursor, Gemini</span></div>
      <div class="filetree-line file">&nbsp;&nbsp;└── <svg><use href="#icon-file"></use></svg> install.py <span class="filetree-comment"># Cross-platform installer</span></div>
    </div>

    <h2 id="faq">Frequently Asked Questions</h2>
    <div class="faq-list">
      <details class="faq-item">
        <summary class="faq-summary">
          <span>Does this document require internet access to view?</span>
          <svg class="faq-chevron"><use href="#icon-chevron-right"></use></svg>
        </summary>
        <div class="faq-content">
          <p>No. All styling, SVG icons, fonts, and client scripts are directly embedded into the single HTML file. You can open it offline, attach it to emails, or host it on any static server.</p>
        </div>
      </details>
      <details class="faq-item">
        <summary class="faq-summary">
          <span>How does dark mode persist across reloads?</span>
          <svg class="faq-chevron"><use href="#icon-chevron-right"></use></svg>
        </summary>
        <div class="faq-content">
          <p>The mode setting is stored in local storage inside a safe try-catch wrapper. If local storage is disabled (e.g. in high-security iframe sandboxes), it gracefully defaults to the operating system's prefers-color-scheme.</p>
        </div>
      </details>
    </div>
    """

    toc_html = """
    <ul class="toc-list">
      <li class="toc-item level-2"><a href="#key-metrics" class="toc-link">Key Performance Metrics</a></li>
      <li class="toc-item level-2"><a href="#feature-architecture" class="toc-link">Architecture Components</a></li>
      <li class="toc-item level-2"><a href="#callouts-feedback" class="toc-link">Semantic Callouts</a></li>
      <li class="toc-item level-2"><a href="#interactive-tabs" class="toc-link">Implementation Profiles</a></li>
      <li class="toc-item level-2"><a href="#comparison" class="toc-link">Architectural Comparison</a></li>
      <li class="toc-item level-2"><a href="#code-sample" class="toc-link">Code Demonstration</a></li>
      <li class="toc-item level-2"><a href="#file-structure" class="toc-link">Repository Structure</a></li>
      <li class="toc-item level-2"><a href="#faq" class="toc-link">Frequently Asked Questions</a></li>
    </ul>
    """

    replacements = {
        "{{THEME}}": theme,
        "{{MODE}}": mode,
        "{{CSP_META}}": '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; img-src \'self\' data:; script-src \'unsafe-inline\';">',
        "{{TITLE}}": "Design System Showcase & Architecture Report",
        "{{THEME_CSS}}": theme_css,
        "{{BASE_CSS}}": base_css,
        "{{COMPONENTS_CSS}}": comp_css,
        "{{ACCENT_CSS}}": "",
        "{{ICONS_SVG}}": icons_svg,
        "{{APP_JS}}": app_js,
        "{{TYPE_LABEL}}": "Architecture Report",
        "{{MOBILE_TOC_BUTTON}}": '<button id="mobile-toc-toggle" class="icon-btn mobile-toc-btn" type="button" aria-label="Table of Contents" title="Table of Contents"><svg><use href="#icon-menu"></use></svg></button>',
        "{{STATUS_BADGE}}": '<span class="badge badge-final">Final Specification</span>',
        "{{TAGS_CHIPS}}": '<span class="tag-chip"><svg><use href="#icon-tag"></use></svg>Architecture</span><span class="tag-chip"><svg><use href="#icon-tag"></use></svg>Design System</span>',
        "{{SUBTITLE_HTML}}": '<p class="doc-subtitle">A comprehensive demonstration of the visual hierarchy, component taxonomy, responsive grid, and typography tokens across the premium-docs design system.</p>',
        "{{AUTHOR_HTML}}": '<div class="hero-meta-item"><svg><use href="#icon-user"></use></svg><span>Staff Engineering Team</span></div>',
        "{{DATE_HTML}}": '<div class="hero-meta-item"><svg><use href="#icon-calendar"></use></svg><span>October 2026</span></div>',
        "{{READING_TIME_HTML}}": '<div class="hero-meta-item"><svg><use href="#icon-clock"></use></svg><span>4 min read</span></div>',
        "{{GRID_CLASS}}": "",
        "{{SIDEBAR_TOC_HTML}}": f'<aside class="doc-sidebar" aria-label="Table of contents"><div class="toc-heading"><svg><use href="#icon-layers"></use></svg><span>Contents</span></div>{toc_html}</aside>',
        "{{MOBILE_TOC_DRAWER_HTML}}": f'<div id="mobile-toc-overlay" class="mobile-toc-overlay"></div><div id="mobile-toc-drawer" class="mobile-toc-drawer"><div class="mobile-toc-header"><strong>Contents</strong><button id="mobile-toc-close" class="icon-btn" type="button" aria-label="Close Table of Contents"><svg><use href="#icon-x"></use></svg></button></div>{toc_html}</div>',
        "{{CONTENT_HTML}}": content_html,
    }

    output = shell
    for k, v in replacements.items():
        output = output.replace(k, v)

    out_p = pathlib.Path(out_file)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_text(output, encoding="utf-8")
    print(f"Generated {out_file} ({len(output)} bytes)")

if __name__ == "__main__":
    build_showcase(theme="aurora", mode="light", out_file="docs/showcase-aurora-light.html")
    build_showcase(theme="aurora", mode="dark", out_file="docs/showcase-aurora-dark.html")
    build_showcase(theme="slate", mode="light", out_file="docs/showcase-slate-light.html")
    build_showcase(theme="paper", mode="light", out_file="docs/showcase-paper-light.html")
    build_showcase(theme="paper", mode="dark", out_file="docs/showcase-paper-dark.html")
