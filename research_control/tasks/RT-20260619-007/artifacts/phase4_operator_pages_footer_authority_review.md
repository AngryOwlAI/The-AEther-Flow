<!-- authority: control -->

# Phase 4 Operator Pages Footer Authority Review

## Scope

This review closes the Phase 4 Documentation Curator packet for the six operational page stacks named in `research_control/design/documentation_curator_post_migration_quality_plan.md`. The review checks reader orientation, footer authority placement, visual strategy, screenshot evidence, and forbidden authority overread.

## Page Review Matrix

| Page | Opening revision | Visual decision | Authority footer | Evidence |
| --- | --- | --- | --- | --- |
| `project-system-improvement` | Expanded around the page-specific operational function and its safe reader action. | Improvement-loop process map plus signal/evidence matrices. | Full generated-noncanonical paragraph moved to marked GitHub and HTML authority footer. | Desktop `research_control/tasks/RT-20260619-007/artifacts/screenshots/project-system-improvement-desktop.png`; mobile `research_control/tasks/RT-20260619-007/artifacts/screenshots/project-system-improvement-mobile.png`. |
| `documentation-curator-publication-process` | Expanded around the page-specific operational function and its safe reader action. | Publication lifecycle matrix plus brief/medium/review boundaries. | Full generated-noncanonical paragraph moved to marked GitHub and HTML authority footer. | Desktop `research_control/tasks/RT-20260619-007/artifacts/screenshots/documentation-curator-publication-process-desktop.png`; mobile `research_control/tasks/RT-20260619-007/artifacts/screenshots/documentation-curator-publication-process-mobile.png`. |
| `memory-system` | Expanded around the page-specific operational function and its safe reader action. | Authority and retrieval layer map plus query workflow matrix. | Full generated-noncanonical paragraph moved to marked GitHub and HTML authority footer. | Desktop `research_control/tasks/RT-20260619-007/artifacts/screenshots/memory-system-desktop.png`; mobile `research_control/tasks/RT-20260619-007/artifacts/screenshots/memory-system-mobile.png`. |
| `validator-operator-workflow` | Expanded around the page-specific operational function and its safe reader action. | Command decision matrix; no Mermaid required. | Full generated-noncanonical paragraph moved to marked GitHub and HTML authority footer. | Desktop `research_control/tasks/RT-20260619-007/artifacts/screenshots/validator-operator-workflow-desktop.png`; mobile `research_control/tasks/RT-20260619-007/artifacts/screenshots/validator-operator-workflow-mobile.png`. |
| `roles-and-skills` | Expanded around the page-specific operational function and its safe reader action. | Authority inspection, active role, and skill workflow matrices; no Mermaid required. | Full generated-noncanonical paragraph moved to marked GitHub and HTML authority footer. | Desktop `research_control/tasks/RT-20260619-007/artifacts/screenshots/roles-and-skills-desktop.png`; mobile `research_control/tasks/RT-20260619-007/artifacts/screenshots/roles-and-skills-mobile.png`. |
| `technical-requirements` | Expanded around the page-specific operational function and its safe reader action. | Requirement-tier, command-family, and scoped-tooling matrices; no Mermaid required. | Full generated-noncanonical paragraph moved to marked GitHub and HTML authority footer. | Desktop `research_control/tasks/RT-20260619-007/artifacts/screenshots/technical-requirements-desktop.png`; mobile `research_control/tasks/RT-20260619-007/artifacts/screenshots/technical-requirements-mobile.png`. |

## Boundary Review

- The project-system page treats classifier and resolver output as routing evidence, not correctness proof or checkpoint authority.
- The publication-process page preserves the brief-first process and keeps the retired Visual Atlas/topic-registry path outside active creation.
- The memory-system page states that registries and canonical sources carry authority while Obsidian, semantic extracts, SQLite, wiki, and `.local` mirrors remain retrieval support.
- The validator page states that PASS is bounded command evidence, not scientific truth, role authority, or generated-output authority.
- The roles-and-skills page states that catalogs are navigation aids and current authority is task-local.
- The technical-requirements page states that working tools are prerequisites, not authorization.

## Verification Plan

The required verification chain is strict publication validation, screenshot QA, bootstrap, validate-only bootstrap, documentation-surface audit, project-improvement signal validation, documentation-impact validation, research-control validation, research-control diff validation, depth lint, focused publication/depth unit tests, checkpoint validation, and `git diff --check`.

## Source Materials

AEther-Flow Project. (2026). `research_control/design/documentation_curator_post_migration_quality_plan.md` [Phase 4 scope and diagram decisions].

AEther-Flow Project. (2026). `registries/PUBLICATION_BRIEF_REGISTRY.csv` [Publication page rows and review evidence paths].

AEther-Flow Project. (2026). `research_control/design/github_facing_explainer_contract.md` [GitHub-facing source-binding and authority contract].

AEther-Flow Project. (2026). `research_control/design/html_explainer_flexible_presentation_contract.md` [Tracked HTML no-network and source-binding contract].

AEther-Flow Project. (2026). `.agents/roles/research_ops/documentation-curator.v2.0.0.md` [Documentation Curator role boundary].
