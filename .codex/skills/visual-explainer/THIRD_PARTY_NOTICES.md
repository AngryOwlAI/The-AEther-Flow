# Third-Party Notices

## visual-explainer

This project-local Codex skill vendors selected files from `visual-explainer`.

- Upstream repository: https://github.com/nicobailon/visual-explainer
- Upstream version: v0.7.1
- Vendored commit: 8f1d0e38ab0f265632a31d2fd032f7b730c98c15
- Copyright: Copyright (c) 2025 Nico Bailon
- License: MIT

## Mermaid

This project uses a pinned Mermaid package for build-time rendering of governed
Mermaid diagrams into sanitized inline SVG for standalone tracked HTML
explainers.

- npm package: `mermaid@11.15.0`
- Package tarball: https://registry.npmjs.org/mermaid/-/mermaid-11.15.0.tgz
- Upstream repository: https://github.com/mermaid-js/mermaid
- Retrieval method: subskill-local npm dependency install
- Retrieval date: 2026-06-11
- Local tooling path: `.codex/skills/visual-explainer/subskills/mermaid-documentation/scripts/`
- Runtime role: build-time only; tracked HTML must not import Mermaid in the browser
- License: MIT

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
