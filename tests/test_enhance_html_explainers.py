from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "enhance_html_explainers.py"


def load_enhancer():
    spec = importlib.util.spec_from_file_location("enhance_html_explainers", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class EnhanceHtmlExplainersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.enhancer = load_enhancer()

    def test_inject_removes_visible_file_metadata_and_obsolete_buttons(self) -> None:
        html = """
<!doctype html>
<html>
<head><title>Example</title></head>
<body>
  <main>
	    <header class="hero">
	      <div><h1>Example</h1></div>
	      <aside class="meta-stack" aria-label="Page metadata">
        <div class="meta-chip"><strong>Layout intent</strong><br>Renderer metadata.</div>
        <div class="meta-chip"><strong>Authority</strong><br>Human-only generated derivative</div>
        <div class="meta-chip"><strong>Source basis</strong><br><code>MD-EXAMPLE</code></div>
      </aside>
	    </header>
	    <nav data-explainer-control="section_toc"><a href="#analysis">Analysis</a></nav>
	    <section id="content-blocks">
	      <article data-content-block="example">
	        <p>The legitimate claim is explanatory: this block may summarize source boundaries that already exist in the cited materials. It may not change project authority.</p>
	      </article>
	    </section>
	    <section id="analysis" data-explainer-control="expandable_analysis_panels">
	      <p class="eyebrow">Analysis capsules</p>
	      <h2>Claim-Aware Analysis</h2>
	      <article data-analysis-capsule="test"><div data-capsule-field="premise"></div></article>
	    </section>
	  </main>
	</body>
	</html>
"""

        updated = self.enhancer.inject(html)

        self.assertNotIn("Page metadata", updated)
        self.assertNotIn("Layout intent", updated)
        self.assertNotIn("Expand notes", updated)
        self.assertNotIn("Simple view", updated)
        self.assertNotIn("#analysis", updated)
        self.assertNotIn("Analysis capsules", updated)
        self.assertNotIn("Claim-Aware Analysis", updated)
        self.assertNotIn("data-analysis-capsule", updated)
        self.assertNotIn("The legitimate claim is explanatory", updated)
        self.assertIn("Search this explainer", updated)

    def test_inject_refreshes_existing_reader_layer(self) -> None:
        html = f"""
<!doctype html>
<html>
<head>
<style id="{self.enhancer.STYLE_ID}">body[data-reader-mode="simple"] pre {{ display: none; }}</style>
</head>
<body>
  <nav data-explainer-control="section_toc"></nav>
  <script id="{self.enhancer.SCRIPT_ID}">
    document.body.dataset.readerMode = 'technical';
    // Expand notes
  </script>
</body>
</html>
"""

        updated = self.enhancer.inject(html)

        self.assertEqual(1, updated.count(f'id="{self.enhancer.STYLE_ID}"'))
        self.assertEqual(1, updated.count(f'id="{self.enhancer.SCRIPT_ID}"'))
        self.assertNotIn("data-reader-mode", updated)
        self.assertNotIn("readerMode", updated)
        self.assertNotIn("Expand notes", updated)
        self.assertIn("Explainer search", updated)


if __name__ == "__main__":
    unittest.main()
