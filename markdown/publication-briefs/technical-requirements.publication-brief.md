---
brief_id: "PB-TECHNICAL-REQUIREMENTS"
subject: "Technical Requirements For Reproducible Operation"
reader: "Maintainer, reviewer, external AI reader, or future operator preparing to inspect the repository, run checks, refresh generated memory/wiki surfaces, review tracked HTML, or build PDFs without confusing tools with authority."
reader_job: "Identify the minimum local tool tier needed for a task, choose the repository-owned command path, and preserve the source-authority boundary before changing project knowledge."
document_type: "contributor_operator_guide"
reading_experience: "A practical operator guide with requirement tiers, command families, troubleshooting cautions, and authority boundaries. It should be concrete enough to run the project, but explicit that tool availability never grants permission or scientific status."
narrative_structure:
  - "Open with the operating rule: technical requirements make the repository reproducible, but do not create authority."
  - "Separate read-only inspection, governed Codex workflow, Python validators, memory/wiki refresh, HTML screenshot QA, and PDF derivative work."
  - "Explain .venv, requirements.txt, Makefile targets, and repository-owned command paths."
  - "Map Node, npm, Playwright, Mermaid, and PDF tooling only to the workflows that require them."
  - "Close with a tool-versus-authority boundary and source-inspection order."
visual_strategy: "annotated_table"
source_basis:
  - "README.md"
  - "AGENTS.md"
  - "research_control/README.md"
  - "requirements.txt"
  - "Makefile"
  - "scripts/README.md"
  - "tests/README.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - ".codex/skills/visual-explainer/SKILL.md"
  - ".codex/skills/pdf-derivative-build/SKILL.md"
authority_boundaries:
  - "The page may explain current local requirements, Codex app harness assumptions, Python virtual environment setup, repository-owned command families, generated-memory refresh, screenshot QA, and PDF derivative build requirements."
  - "The page may not change dependencies, validators, Makefile targets, command semantics, harness policy, role authority, routing behavior, checkpoint behavior, generated-output authority, or physics claim status."
  - "Tool availability is operational support only. Current authority still comes from registered sources, registries, task records, role or skill contracts, AgentJob allowlists, completion evidence, and validator results."
output_surfaces:
  - "github-facing/technical-requirements-explainer.md"
  - "html/technical-requirements-explainer.html"
acceptance_criteria:
  - "Explains requirement tiers for inspection, governed Codex operation, Python validators, memory/wiki refresh, HTML screenshot QA, and PDF derivative work."
  - "Covers .venv usage, requirements.txt, Makefile targets, and command-family selection without altering them."
  - "Frames Node, npm, Playwright, and Mermaid as scoped to diagram/screenshot workflows."
  - "Frames Codex app as the current governed harness, not as scientific authority or permanent lock-in."
  - "Separates local retrieval and generated surfaces from canonical authority."
  - "Includes page-specific before/after review and desktop/mobile screenshot evidence."
forbidden_patterns:
  - "Adding dependencies or implying documentation alone changed runtime requirements."
  - "Claiming permanent Codex app lock-in or unsupported future harness parity."
  - "Treating a tool, generated page, local cache, screenshot, or validator PASS as independent source authority."
  - "Changing validator behavior, command semantics, routing behavior, checkpoint gates, Makefile targets, dependencies, or role permissions."
  - "Migrating Phase 6 or the whole corpus without separate explicit approval."
migration_status: "reviewed"
---

# Publication Brief: Technical Requirements For Reproducible Operation

This Phase 5C page is a contributor/operator guide for local technical
requirements. It explains how to inspect, run, refresh, screenshot, and build
repository artifacts without turning runtime tooling into source authority.
