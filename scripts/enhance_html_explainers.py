#!/usr/bin/env python3
"""Enhance standalone Æther-Flow HTML explainers without touching diagrams.

This script injects a small CSS/JavaScript reading layer into generated HTML
files under `html/`.

It is intended as a renderer-layer prototype or local preview tool. In the
tracked repository workflow, generated HTML should be produced from Markdown
source specs, not manually edited as the source of truth.

Usage:
    python scripts/enhance_html_explainers.py --root . --suffix .enhanced
    python scripts/enhance_html_explainers.py --root . --in-place
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
from typing import Iterable

STYLE_ID = "aether-docs-enhancement"
SCRIPT_ID = "aether-docs-enhancement-js"

ENHANCEMENT_CSS = f"""
<style id="{STYLE_ID}">
  :root {{
    --doc-bg: #f8f5ee;
    --doc-ink: #18201b;
    --doc-muted: #5f6b60;
    --doc-line: rgba(33, 49, 40, .18);
    --doc-panel: rgba(255, 255, 255, .92);
    --doc-wash: #f1eadc;
    --doc-authority: #1e3a5f;
    --doc-physics: #2f6f54;
    --doc-workflow: #8b5a20;
    --doc-warning: #a34f12;
    --doc-validation: #0f766e;
    --doc-shadow: 0 18px 50px rgba(27, 33, 28, .10);
    --doc-radius: 8px;
  }}

  html {{ scroll-behavior: smooth; }}
  body {{
    background:
      linear-gradient(180deg, #fffcf7 0%, var(--doc-bg) 42%, #efe8dc 100%);
    color: var(--doc-ink);
  }}

  body::before {{
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: .28;
    background-image:
      linear-gradient(rgba(30,58,95,.07) 1px, transparent 1px),
      linear-gradient(90deg, rgba(30,58,95,.06) 1px, transparent 1px);
    background-size: 44px 44px;
    mask-image: linear-gradient(180deg, black, transparent 75%);
  }}

  .page-shell {{
    max-width: 1220px;
    padding-top: 26px;
    position: relative;
  }}

  .hero,
  .panel,
  .atlas-link,
  .content-block,
  .capsule,
  .block-subgroup,
  .source-list li,
  details {{
    border-radius: var(--doc-radius);
  }}

  .hero {{
    position: relative;
    overflow: hidden;
    box-shadow: var(--doc-shadow);
    border-color: rgba(30,58,95,.22);
    background:
      linear-gradient(135deg, rgba(255,255,255,.96), rgba(223,232,242,.78)),
      linear-gradient(90deg, rgba(47,111,84,.12), rgba(139,90,32,.10));
  }}

  .hero > * {{ position: relative; z-index: 1; }}

  h1 {{
    letter-spacing: 0;
    text-wrap: balance;
  }}

  h2, h3 {{ text-wrap: balance; }}

  p, li, dd {{
    font-size: 1.01rem;
    line-height: 1.72;
  }}

  .hero-copy {{
    font-size: clamp(1.02rem, 2vw, 1.22rem);
    max-width: 70ch;
  }}

  .meta-chip,
  .source-chip,
  .control-marker {{
    border-radius: 999px;
  }}

  .meta-chip {{
    box-shadow: 0 10px 28px rgba(30,58,95,.08);
  }}

  .nav {{
    top: 8px;
    border-radius: 999px;
    padding: 10px;
    background: rgba(248,245,238,.72);
    border: 1px solid rgba(33,49,40,.10);
    box-shadow: 0 12px 36px rgba(27,33,28,.08);
  }}

  .nav a {{
    border-radius: 999px;
    transition: transform .18s ease, background .18s ease, border-color .18s ease;
  }}

  .nav a:hover,
  .nav a.is-active {{
    transform: translateY(-1px);
    background: var(--doc-ink);
    color: #fffaf1;
    border-color: var(--doc-ink);
  }}

  .panel {{
    box-shadow: 0 14px 44px rgba(27,33,28,.075);
    border-color: rgba(33,49,40,.16);
  }}

  .section-heading {{
    border-bottom: 1px solid rgba(33,49,40,.10);
    padding-bottom: 12px;
  }}

  .subject-summary .content-block {{
    border-left: 7px solid var(--doc-authority);
    background:
      linear-gradient(90deg, rgba(30,58,95,.07), transparent 30%),
      var(--doc-panel);
  }}

  .content-grid {{
    grid-template-columns: 1fr;
  }}

  .content-block {{
    position: relative;
    padding: clamp(18px, 2vw, 26px);
    border-left: 7px solid rgba(30,58,95,.28);
    background: var(--doc-panel);
    box-shadow: 0 8px 28px rgba(27,33,28,.055);
  }}

  .content-block[data-content-block*="ontology"],
  .content-block[data-content-block*="physics"],
  .content-block[data-content-block*="claim"],
  .content-block[data-content-block*="benchmark"],
  .content-block[data-content-block*="derivation"] {{
    border-left-color: var(--doc-physics);
  }}

  .content-block[data-content-block*="workflow"],
  .content-block[data-content-block*="agent"],
  .content-block[data-content-block*="role"],
  .content-block[data-content-block*="director"] {{
    border-left-color: var(--doc-workflow);
  }}

  .content-block[data-content-block*="validation"],
  .content-block[data-content-block*="memory"],
  .content-block[data-content-block*="authority"],
  .content-block[data-content-block*="source"] {{
    border-left-color: var(--doc-validation);
  }}

  .content-block::before {{
    content: attr(data-content-block);
    display: inline-block;
    margin: 0 0 10px;
    padding: 4px 9px;
    border-radius: 999px;
    background: rgba(30,58,95,.08);
    color: var(--doc-authority);
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .04em;
    text-transform: uppercase;
  }}

  .block-head {{
    padding-bottom: 10px;
    border-bottom: 1px dashed rgba(33,49,40,.14);
  }}

  .atlas-link {{
    transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
  }}

  .atlas-link:hover {{
    transform: translateY(-2px);
    box-shadow: 0 14px 34px rgba(27,33,28,.10);
    border-color: rgba(30,58,95,.38);
  }}

  .reader-toolbar {{
    position: sticky;
    top: 68px;
    z-index: 4;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    margin: 10px 0 18px;
    padding: 10px;
    border: 1px solid rgba(33,49,40,.14);
    border-radius: 999px;
    background: rgba(255,255,255,.82);
    backdrop-filter: blur(14px);
    box-shadow: 0 10px 30px rgba(27,33,28,.08);
  }}

  .reader-toolbar input[type="search"] {{
    flex: 1 1 230px;
    min-width: 160px;
    border: 1px solid rgba(33,49,40,.16);
    border-radius: 999px;
    padding: 10px 13px;
    color: var(--doc-ink);
    background: #fff;
    font: inherit;
  }}

  .reader-toolbar button {{
    border: 1px solid rgba(33,49,40,.16);
    border-radius: 999px;
    padding: 9px 12px;
    color: var(--doc-ink);
    background: #fff;
    font: inherit;
    font-weight: 800;
    cursor: pointer;
  }}

  .reader-toolbar button[aria-pressed="true"] {{
    background: var(--doc-ink);
    color: #fffaf1;
  }}

  .reading-progress {{
    position: fixed;
    z-index: 10;
    top: 0;
    left: 0;
    width: var(--reading-progress, 0%);
    height: 4px;
    background: linear-gradient(90deg, var(--doc-authority), var(--doc-physics), var(--doc-warning));
    box-shadow: 0 0 18px rgba(47,111,84,.35);
  }}

  .source-chip,
  .source-list li {{
    cursor: copy;
  }}

  .source-chip.was-copied,
  .source-list li.was-copied {{
    outline: 2px solid rgba(15,118,110,.35);
    background: rgba(15,118,110,.10);
  }}

  mark.search-hit {{
    background: rgba(248,232,199,.9);
    color: inherit;
    padding: 0 .15em;
    border-radius: .25em;
  }}

  [hidden] {{ display: none !important; }}

  body[data-reader-mode="simple"] details.source-fold,
  body[data-reader-mode="simple"] pre {{
    display: none;
  }}

  body[data-reader-mode="simple"] .capsule dd {{
    color: var(--doc-ink);
  }}

  body[data-reader-mode="simple"] p,
  body[data-reader-mode="simple"] li,
  body[data-reader-mode="simple"] dd {{
    font-size: 1.06rem;
    line-height: 1.78;
  }}

  body[data-reader-mode="technical"] .source-chip,
  body[data-reader-mode="technical"] code {{
    font-size: .95em;
  }}

  .diagram-shell {{
    background:
      linear-gradient(180deg, rgba(255,255,255,.96), rgba(248,245,238,.96));
  }}

  .diagram-shell .section-heading::after {{
    content: "Diagram preserved from source spec";
    display: inline-block;
    margin-top: 8px;
    color: var(--doc-muted);
    font-size: .84rem;
  }}

  .zoom-controls button {{
    border-radius: 999px;
    box-shadow: 0 8px 20px rgba(27,33,28,.10);
  }}

  .source-list li {{
    transition: transform .15s ease, background .15s ease;
  }}

  .source-list li:hover {{
    transform: translateY(-1px);
    background: rgba(223,232,242,.58);
  }}

  .capsule {{
    box-shadow: 0 8px 28px rgba(27,33,28,.055);
  }}

  .capsule-row {{
    padding: 10px 0;
    border-top: 1px dashed rgba(33,49,40,.12);
  }}

  .capsule-row:first-child {{
    border-top: 0;
  }}

  @media (max-width: 860px) {{
    .reader-toolbar {{
      position: static;
      border-radius: var(--doc-radius);
    }}

    .nav {{
      border-radius: var(--doc-radius);
    }}

    .hero, .panel {{ border-radius: var(--doc-radius); }}
  }}
</style>
"""

ENHANCEMENT_JS = f"""
<script id="{SCRIPT_ID}">
  (() => {{
    if (window.__aetherDocsEnhancementLoaded) return;
    window.__aetherDocsEnhancementLoaded = true;

    const body = document.body;
    const storageKey = `aether-doc-mode:${{location.pathname}}`;
    const savedMode = localStorage.getItem(storageKey) || 'technical';
    body.dataset.readerMode = savedMode;

    const progress = document.createElement('div');
    progress.className = 'reading-progress';
    progress.setAttribute('aria-hidden', 'true');
    document.body.prepend(progress);

    const nav = document.querySelector('[data-explainer-control="section_toc"]');
    const toolbar = document.createElement('div');
    toolbar.className = 'reader-toolbar';
    toolbar.setAttribute('aria-label', 'Reader controls');
    toolbar.innerHTML = `
      <input type="search" placeholder="Search this explainer" aria-label="Search this explainer">
      <button type="button" data-action="expand">Expand notes</button>
      <button type="button" data-action="collapse">Collapse notes</button>
      <button type="button" data-mode="simple">Simple view</button>
      <button type="button" data-mode="technical">Technical view</button>
    `;
    if (nav) nav.insertAdjacentElement('afterend', toolbar);

    const updateModeButtons = () => {{
      toolbar.querySelectorAll('[data-mode]').forEach((button) => {{
        button.setAttribute('aria-pressed', String(button.dataset.mode === body.dataset.readerMode));
      }});
    }};
    updateModeButtons();

    toolbar.addEventListener('click', (event) => {{
      const button = event.target.closest('button');
      if (!button) return;
      if (button.dataset.action === 'expand') {{
        document.querySelectorAll('details').forEach((details) => {{ details.open = true; }});
      }}
      if (button.dataset.action === 'collapse') {{
        document.querySelectorAll('details').forEach((details) => {{ details.open = false; }});
      }}
      if (button.dataset.mode) {{
        body.dataset.readerMode = button.dataset.mode;
        localStorage.setItem(storageKey, button.dataset.mode);
        updateModeButtons();
      }}
    }});

    const searchable = Array.from(document.querySelectorAll(
      '[data-content-block], [data-analysis-capsule], .source-list li, .atlas-link'
    ));

    const clearMarks = (node) => {{
      node.querySelectorAll('mark.search-hit').forEach((mark) => {{
        mark.replaceWith(document.createTextNode(mark.textContent || ''));
      }});
      node.normalize();
    }};

    const markText = (node, query) => {{
      if (!query || node.matches('script, style, svg, pre, code')) return;
      for (const child of Array.from(node.childNodes)) {{
        if (child.nodeType === Node.TEXT_NODE) {{
          const text = child.nodeValue || '';
          const index = text.toLowerCase().indexOf(query);
          if (index >= 0) {{
            const range = document.createRange();
            range.setStart(child, index);
            range.setEnd(child, index + query.length);
            const mark = document.createElement('mark');
            mark.className = 'search-hit';
            range.surroundContents(mark);
          }}
        }} else if (child.nodeType === Node.ELEMENT_NODE) {{
          markText(child, query);
        }}
      }}
    }};

    const searchInput = toolbar.querySelector('input[type="search"]');
    searchInput?.addEventListener('input', () => {{
      const raw = searchInput.value.trim();
      const query = raw.toLowerCase();
      searchable.forEach((node) => {{
        clearMarks(node);
        const matches = !query || node.textContent.toLowerCase().includes(query);
        node.hidden = !matches;
        if (matches && query) markText(node, query);
      }});
    }});

    const sourceNodes = document.querySelectorAll('[data-source-path], .source-list li');
    sourceNodes.forEach((node) => {{
      node.addEventListener('click', async () => {{
        const text = node.getAttribute('data-source-path') || node.textContent.trim();
        if (!text) return;
        try {{
          await navigator.clipboard.writeText(text);
          node.classList.add('was-copied');
          setTimeout(() => node.classList.remove('was-copied'), 850);
        }} catch (_) {{
          // Clipboard may be unavailable for local file URLs. No-op.
        }}
      }});
    }});

    const updateProgress = () => {{
      const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
      const pct = Math.min(100, Math.max(0, (window.scrollY / max) * 100));
      document.documentElement.style.setProperty('--reading-progress', `${{pct}}%`);
    }};
    updateProgress();
    addEventListener('scroll', updateProgress, {{ passive: true }});
    addEventListener('resize', updateProgress);

    const navLinks = Array.from(document.querySelectorAll('.nav a[href^="#"]'));
    const sections = navLinks
      .map((link) => document.querySelector(link.getAttribute('href')))
      .filter(Boolean);
    if ('IntersectionObserver' in window && sections.length) {{
      const observer = new IntersectionObserver((entries) => {{
        entries.forEach((entry) => {{
          if (!entry.isIntersecting) return;
          const id = `#${{entry.target.id}}`;
          navLinks.forEach((link) => link.classList.toggle('is-active', link.getAttribute('href') === id));
        }});
      }}, {{ rootMargin: '-28% 0px -62% 0px', threshold: 0.01 }});
      sections.forEach((section) => observer.observe(section));
    }}
  }})();
</script>
"""

def already_enhanced(text: str) -> bool:
    return STYLE_ID in text or SCRIPT_ID in text

def inject(text: str) -> str:
    if already_enhanced(text):
        return text

    if "</head>" not in text or "</body>" not in text:
        raise ValueError("not a complete HTML document")

    text = text.replace("</head>", ENHANCEMENT_CSS + "\n</head>", 1)
    text = text.replace("</body>", ENHANCEMENT_JS + "\n</body>", 1)
    return text

def iter_html(root: Path) -> Iterable[Path]:
    html_dir = root / "html"
    if not html_dir.exists():
        return []
    return sorted(html_dir.glob("*-explainer.html"))

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--in-place", action="store_true")
    parser.add_argument("--suffix", default=".enhanced", help="suffix before .html when not using --in-place")
    args = parser.parse_args()

    files = list(iter_html(args.root))
    if not files:
        print("No explainer HTML files found under html/")
        return 1

    changed = 0
    for path in files:
        original = path.read_text(encoding="utf-8")
        try:
            updated = inject(original)
        except ValueError as exc:
            print(f"SKIP {path}: {exc}")
            continue

        if updated == original:
            print(f"UNCHANGED {path}")
            continue

        if args.in_place:
            target = path
        else:
            target = path.with_name(path.stem + args.suffix + path.suffix)
        target.write_text(updated, encoding="utf-8")
        changed += 1
        print(f"WROTE {target}")

    print(f"Enhanced {changed} file(s).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
