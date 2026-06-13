#!/usr/bin/env python3
"""Enhance standalone Æther-Flow HTML explainers without touching diagrams.

This script injects or refreshes a small CSS/JavaScript reading layer into
generated HTML files under `html/`.

It is intended as a renderer-layer prototype or local preview tool. In the
tracked repository workflow, generated HTML should be produced from Markdown
source specs, not manually edited as the source of truth.

Usage:
    python scripts/enhance_html_explainers.py --root . --suffix .enhanced
    python scripts/enhance_html_explainers.py --root . --in-place
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path
import re
from typing import Iterable

STYLE_ID = "aether-docs-enhancement"
SCRIPT_ID = "aether-docs-enhancement-js"
OUTPUT_PATH_RE = re.compile(r"^output_path:\s*[\"']?([^\"'\n]+)[\"']?\s*$", re.MULTILINE)

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

  .hero {{
    grid-template-columns: minmax(0, 1fr);
    align-items: start;
  }}

  .hero > div {{
    max-width: 78ch;
  }}

  p, li, dd {{
    font-size: 1.01rem;
    line-height: 1.72;
  }}

  .hero-copy {{
    font-size: clamp(1.02rem, 2vw, 1.22rem);
    max-width: 70ch;
  }}

  .source-chip,
  .control-marker {{
    border-radius: 999px;
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

    const progress = document.createElement('div');
    progress.className = 'reading-progress';
    progress.setAttribute('aria-hidden', 'true');
    document.body.prepend(progress);

    const nav = document.querySelector('[data-explainer-control="section_toc"]');
    const toolbar = document.createElement('div');
    toolbar.className = 'reader-toolbar';
    toolbar.setAttribute('aria-label', 'Explainer search');
    toolbar.innerHTML = `
      <input type="search" placeholder="Search this explainer" aria-label="Search this explainer">
    `;
    if (nav) nav.insertAdjacentElement('afterend', toolbar);

    const searchable = Array.from(document.querySelectorAll(
      '[data-content-block], .source-list li, .atlas-link'
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
    const applySearch = () => {{
      const raw = searchInput.value.trim();
      const query = raw.toLowerCase();
      searchable.forEach((node) => {{
        clearMarks(node);
        const matches = !query || node.textContent.toLowerCase().includes(query);
        node.hidden = !matches;
        if (matches && query) markText(node, query);
      }});
    }};
    searchInput?.addEventListener('input', applySearch);
    searchInput?.addEventListener('search', applySearch);

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

def replace_tag_by_id(text: str, tag: str, element_id: str, replacement: str) -> str:
    pattern = re.compile(
        rf"<{tag}\b[^>]*\bid=[\"']{re.escape(element_id)}[\"'][^>]*>.*?</{tag}>",
        re.IGNORECASE | re.DOTALL,
    )
    updated, count = pattern.subn(replacement, text, count=1)
    return updated if count else text

def remove_visible_file_metadata(text: str) -> str:
    return re.sub(
        r"\n\s*<aside\s+class=[\"']meta-stack[\"']\s+aria-label=[\"']Page metadata[\"']>.*?</aside>",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

def remove_analysis_capsule_layer(text: str) -> str:
    text = re.sub(
        r"<a\s+href=[\"']#analysis[\"']>Analysis</a>",
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\n\s*<section\s+id=[\"']analysis[\"'][^>]*>.*?</section>",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(
        r"<p>The legitimate claim is explanatory:.*?</p>",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = text.replace(".hub-grid, .capsule-grid, .source-grid", ".hub-grid, .source-grid")
    text = text.replace(".atlas-link, .content-block, .capsule, .block-subgroup", ".atlas-link, .content-block, .block-subgroup")
    text = re.sub(
        r"\n\s*\.capsule(?:-row)?\b[^{}]*\{[^{}]*\}",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    return text

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_basis_by_output(root: Path) -> dict[Path, tuple[str, str]]:
    registry = root / "registries" / "MARKDOWN_SOURCE_REGISTRY.csv"
    if not registry.exists():
        return {}
    by_output: dict[Path, tuple[str, str]] = {}
    with registry.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("role") != "html_explainer_source_spec":
                continue
            spec_path = root / row.get("path", "")
            if not spec_path.exists():
                continue
            match = OUTPUT_PATH_RE.search(spec_path.read_text(encoding="utf-8"))
            if not match:
                continue
            by_output[(root / match.group(1).strip()).resolve()] = (
                row.get("object_id", ""),
                sha256_file(spec_path),
            )
    return by_output


def upsert_meta(text: str, name: str, content: str) -> str:
    pattern = re.compile(
        rf"(<meta\s+name=[\"']{re.escape(name)}[\"']\s+content=[\"'])([^\"']*)([\"'][^>]*>)",
        re.IGNORECASE,
    )
    updated, count = pattern.subn(rf"\g<1>{content}\g<3>", text, count=1)
    if count:
        return updated
    return updated.replace(
        "</head>", f'  <meta name="{name}" content="{content}">\n</head>', 1
    )


def refresh_source_basis_metadata(text: str, source_basis: tuple[str, str] | None) -> str:
    if not source_basis:
        return text
    object_id, source_hash = source_basis
    if not object_id or not source_hash:
        return text
    text = upsert_meta(text, "aether-flow-source-basis", object_id)
    return upsert_meta(text, "aether-flow-source-basis-hash", source_hash)


def inject(text: str, source_basis: tuple[str, str] | None = None) -> str:
    if "</head>" not in text or "</body>" not in text:
        raise ValueError("not a complete HTML document")

    text = refresh_source_basis_metadata(text, source_basis)
    text = remove_visible_file_metadata(text)
    text = remove_analysis_capsule_layer(text)
    if STYLE_ID in text:
        text = replace_tag_by_id(text, "style", STYLE_ID, ENHANCEMENT_CSS)
    else:
        text = text.replace("</head>", ENHANCEMENT_CSS + "\n</head>", 1)
    if SCRIPT_ID in text:
        text = replace_tag_by_id(text, "script", SCRIPT_ID, ENHANCEMENT_JS)
    else:
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

    root = args.root.resolve()
    files = list(iter_html(root))
    if not files:
        print("No explainer HTML files found under html/")
        return 1

    basis_by_output = source_basis_by_output(root)
    changed = 0
    for path in files:
        original = path.read_text(encoding="utf-8")
        try:
            updated = inject(original, basis_by_output.get(path.resolve()))
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
