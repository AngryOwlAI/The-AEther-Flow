---
description: Generate a local visual explainer for the Æther-Flow research project with strict claim boundaries
---
Load the visual-explainer skill, then generate a self-contained HTML explainer
for `The-AEther-Flow` research project.

Use Æther-Flow Project Mode from `.codex/skills/visual-explainer/SKILL.md`.
Read sources in this order before generating claims:

1. `AGENTS.md`
2. `README.md`
3. `ontology/aether-and-aether-flow.md`
4. `ontology/tex/*.tex` and `ontology/pdfs/*.pdf` when present
5. `manuscripts/`
6. `git status` and recent commit history

The page must explain:

- the two-track project identity: physics research and AI research-agent
  development
- the physics track as exact-GR benchmark adoption with an open derivation
  burden
- the AI track as human-scaffolded research-agent workflow, not autonomous proof
- the ontology vocabulary: Æther, Æther-flow, observed space, S-time, observed
  expansion, and mass-shaped reorganization
- the source-law burden and why "not yet derived" remains a live constraint
- the repository map and which artifacts are source authority versus local or
  generated explanatory output

Claim discipline:

- Do not present speculative ontology as established physics.
- Distinguish adopted GR structure from derived substrate law.
- Preserve negative-result and "not yet derived" status clearly.
- Mark any inference from repository structure as inference.
- Use APA 7 style when citing documents or external material in the generated
  page.

Recommended page structure:

1. Executive orientation
2. Two-track system map
3. Ontology-to-benchmark flow diagram
4. Derivation burden and open gates
5. Research-agent workflow map
6. Repository artifact map
7. What is established, open, speculative, or generated
8. Logical next steps

Write the file to `.local/html_wikis/visual-explainer/` with a descriptive
filename such as `aether-flow-project-explainer.html`. Open the result in the
browser when possible and report the local path. Do not publish or deploy the
page without a separate explicit user request.

$@
