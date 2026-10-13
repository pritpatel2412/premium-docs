/**
 * premium-docs Client Engine (app.js)
 * Lightweight, zero-dependency, self-contained interactive features.
 */
(function () {
  'use strict';

  // --- Safe Storage Helper (handles private mode & sandboxes) ---
  const Storage = {
    get: function (key) {
      try {
        return localStorage.getItem(key);
      } catch (e) {
        return null;
      }
    },
    set: function (key, value) {
      try {
        localStorage.setItem(key, value);
      } catch (e) {}
    }
  };

  // --- 1. Theme Management (Light / Dark / Auto) ---
  const ThemeManager = {
    init: function () {
      const toggleBtn = document.getElementById('theme-toggle-btn');
      const root = document.documentElement;
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

      const authorMode = root.getAttribute('data-mode');
      const savedMode = Storage.get('premium-docs-mode');

      // Prefer user's explicit saved preference, otherwise author's baked setting, or auto
      const initialMode = savedMode || authorMode || 'auto';
      this.applyMode(initialMode);

      if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
          const current = root.getAttribute('data-mode') || 'auto';
          let next = 'dark';
          if (current === 'light') next = 'dark';
          else if (current === 'dark') next = 'auto';
          else if (current === 'auto') next = 'light';

          this.applyMode(next);
          Storage.set('premium-docs-mode', next);
        });
      }

      // Update when OS changes preference and mode is auto
      mediaQuery.addEventListener('change', () => {
        const mode = root.getAttribute('data-mode') || 'auto';
        if (mode === 'auto') {
          this.applyMode('auto');
        }
      });
    },

    applyMode: function (mode) {
      const root = document.documentElement;
      const toggleBtn = document.getElementById('theme-toggle-btn');
      const iconUse = toggleBtn ? toggleBtn.querySelector('use') : null;

      if (mode === 'auto') {
        root.removeAttribute('data-mode');
        if (toggleBtn) toggleBtn.setAttribute('title', 'Theme: Auto (System)');
        if (iconUse) iconUse.setAttribute('href', '#icon-laptop');
      } else if (mode === 'dark') {
        root.setAttribute('data-mode', 'dark');
        if (toggleBtn) toggleBtn.setAttribute('title', 'Theme: Dark');
        if (iconUse) iconUse.setAttribute('href', '#icon-moon');
      } else {
        root.setAttribute('data-mode', 'light');
        if (toggleBtn) toggleBtn.setAttribute('title', 'Theme: Light');
        if (iconUse) iconUse.setAttribute('href', '#icon-sun');
      }
    }
  };

  // --- 2. Reading Progress Bar ---
  const ProgressManager = {
    init: function () {
      const bar = document.getElementById('reading-progress');
      if (!bar) return;

      const updateProgress = () => {
        const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
        if (totalHeight <= 0) {
          bar.style.width = '0%';
          return;
        }
        const progress = Math.min(100, Math.max(0, (window.scrollY / totalHeight) * 100));
        bar.style.width = progress + '%';
      };

      window.addEventListener('scroll', updateProgress, { passive: true });
      window.addEventListener('resize', updateProgress, { passive: true });
      updateProgress();
    }
  };

  // --- 3. Table of Contents & Scroll-Spy ---
  const TocManager = {
    init: function () {
      const tocLinks = document.querySelectorAll('.toc-link');
      if (tocLinks.length === 0) return;

      const headings = [];
      tocLinks.forEach((link) => {
        const id = link.getAttribute('href');
        if (id && id.startsWith('#')) {
          const el = document.getElementById(id.substring(1));
          if (el) headings.push({ el: el, link: link });
        }
      });

      if (headings.length === 0) return;

      const setActive = () => {
        const scrollY = window.scrollY + 100;
        let current = headings[0];

        for (let i = 0; i < headings.length; i++) {
          if (headings[i].el.offsetTop <= scrollY) {
            current = headings[i];
          } else {
            break;
          }
        }

        tocLinks.forEach((l) => l.classList.remove('active'));
        if (current && current.link) {
          current.link.classList.add('active');
        }
      };

      window.addEventListener('scroll', setActive, { passive: true });
      setActive();

      // Mobile Drawer Toggle
      const openBtn = document.getElementById('mobile-toc-toggle');
      const closeBtn = document.getElementById('mobile-toc-close');
      const overlay = document.getElementById('mobile-toc-overlay');
      const drawer = document.getElementById('mobile-toc-drawer');

      const toggleDrawer = (open) => {
        if (!drawer || !overlay) return;
        if (open) {
          drawer.classList.add('open');
          overlay.classList.add('open');
          document.body.style.overflow = 'hidden';
        } else {
          drawer.classList.remove('open');
          overlay.classList.remove('open');
          document.body.style.overflow = '';
        }
      };

      if (openBtn) openBtn.addEventListener('click', () => toggleDrawer(true));
      if (closeBtn) closeBtn.addEventListener('click', () => toggleDrawer(false));
      if (overlay) overlay.addEventListener('click', () => toggleDrawer(false));

      // Close on escape
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && drawer && drawer.classList.contains('open')) {
          toggleDrawer(false);
        }
      });

      // Close drawer on clicking link inside mobile drawer
      if (drawer) {
        drawer.querySelectorAll('.toc-link').forEach((link) => {
          link.addEventListener('click', () => toggleDrawer(false));
        });
      }
    }
  };

  // --- 4. Accessible Tabs ---
  const TabsManager = {
    init: function () {
      const containers = document.querySelectorAll('.tabs-container');
      containers.forEach((container) => {
        const tabs = container.querySelectorAll('.tab-button');
        const panels = container.querySelectorAll('.tab-panel');

        tabs.forEach((tab, index) => {
          tab.addEventListener('click', () => {
            tabs.forEach((t) => {
              t.setAttribute('aria-selected', 'false');
              t.tabIndex = -1;
            });
            panels.forEach((p) => (p.hidden = true));

            tab.setAttribute('aria-selected', 'true');
            tab.tabIndex = 0;
            if (panels[index]) panels[index].hidden = false;
          });

          // W3C ARIA Keyboard navigation
          tab.addEventListener('keydown', (e) => {
            let nextIndex = null;
            if (e.key === 'ArrowRight') {
              nextIndex = (index + 1) % tabs.length;
            } else if (e.key === 'ArrowLeft') {
              nextIndex = (index - 1 + tabs.length) % tabs.length;
            } else if (e.key === 'Home') {
              nextIndex = 0;
            } else if (e.key === 'End') {
              nextIndex = tabs.length - 1;
            }

            if (nextIndex !== null) {
              e.preventDefault();
              tabs[nextIndex].focus();
              tabs[nextIndex].click();
            }
          });
        });
      });
    }
  };

  // --- 5. Code Block Copy to Clipboard ---
  const CodeManager = {
    init: function () {
      const buttons = document.querySelectorAll('.copy-button');
      buttons.forEach((btn) => {
        btn.addEventListener('click', async () => {
          const wrapper = btn.closest('.code-block-wrapper');
          if (!wrapper) return;
          const codeEl = wrapper.querySelector('pre code');
          if (!codeEl) return;

          const text = codeEl.innerText || codeEl.textContent;
          try {
            await navigator.clipboard.writeText(text);
            const originalHTML = btn.innerHTML;
            btn.classList.add('copied');
            btn.innerHTML = '<svg class="icon"><use href="#icon-check"></use></svg> Copied!';
            setTimeout(() => {
              btn.classList.remove('copied');
              btn.innerHTML = originalHTML;
            }, 2000);
          } catch (err) {
            // Fallback for restricted contexts
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();
            try {
              document.execCommand('copy');
              btn.classList.add('copied');
              btn.innerText = 'Copied!';
              setTimeout(() => {
                btn.classList.remove('copied');
                btn.innerText = 'Copy';
              }, 2000);
            } catch (e) {}
            document.body.removeChild(textarea);
          }
        });
      });
    }
  };

  // --- 6. Quick Actions (Print & Back to Top) ---
  const ActionsManager = {
    init: function () {
      const printBtn = document.getElementById('print-btn');
      if (printBtn) {
        printBtn.addEventListener('click', () => window.print());
      }

      const backToTopButtons = document.querySelectorAll('.back-to-top, #back-to-top-btn');
      backToTopButtons.forEach((btn) => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        });
      });
    }
  };

  // Initialize all managers when DOM is ready
  document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
    ProgressManager.init();
    TocManager.init();
    TabsManager.init();
    CodeManager.init();
    ActionsManager.init();
  });
})();
