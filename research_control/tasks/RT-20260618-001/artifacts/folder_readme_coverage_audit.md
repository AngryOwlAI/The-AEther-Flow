<!-- authority: explanatory -->

# Folder README Coverage Audit

Task: `RT-20260618-001`

## Objective

Implement the full folder README coverage plan for ordinary project
documentation. The goal is local reader orientation, not GitHub-facing
documentation, HTML generation, generated wiki authoring, physics claim
promotion, or control-contract revision.

## Implemented README Targets

### Agent And Skill Orientation

- `.agents/roles/README.md`
- `.agents/schemas/README.md`
- `.codex/agents/README.md`
- `.codex/prompts/README.md`
- `.codex/skills/README.md`

### Source Documentation And Registry Orientation

- `markdown/README.md`
- `markdown/html-explainer-specs/README.md`
- `markdown/teaching-packets/README.md`
- `registries/README.md`

### Physics-Adjacent Source Boundary Orientation

- `ontology/README.md`
- `ontology/tex/README.md`
- `tex_shared/README.md`

### Research-Control Orientation

- `research_control/design/README.md`
- `research_control/handoffs/README.md`
- `research_control/tasks/README.md`
- `research_control/templates/README.md`

### Tooling And Test Orientation

- `scripts/README.md`
- `scripts/project_control/README.md`
- `scripts/research_control/README.md`
- `tests/README.md`

### Asset Orientation

- `assets/README.md`

## Registration Decision

The memory bootstrap now has an explicit `FOLDER_README_FILES` allowlist for
the planned folder README set. Those README files are registered as:

- role: `folder_readme_documentation`
- authority status: `explanatory_noncanonical`
- owner skill: `documentation-curator`
- audience: `humans_and_agents`

The explicit allowlist avoids promoting ignored, generated, dependency, or
reserved folders into registered documentation by accident.

## Boundary Check

This packet did not edit:

- `github-facing/`
- `html/`
- canonical ontology TeX files
- generated wiki files by hand
- role contracts
- schema contracts
- skill contracts
- validator requirements
- routing behavior
- checkpoint gates

Generated registry and wiki changes were produced by bootstrap from registered
source changes.

