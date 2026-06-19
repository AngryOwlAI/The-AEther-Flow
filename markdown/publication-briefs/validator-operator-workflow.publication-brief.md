---
brief_id: "PB-VALIDATOR-OPERATOR-WORKFLOW"
subject: "Validator And Operator Workflow"
reader: "Maintainer, reviewer, or future agent deciding which repository checks to run for documentation, memory, project-control, and research-control work."
reader_job: "Run the correct command chain for the change type, understand bootstrap versus validate-only, know when documentation-impact and research-control checks are required, capture screenshot evidence for tracked HTML, and avoid treating validator PASS as scientific truth or publication taste."
document_type: "contributor_operator_guide"
reading_experience: "A practical operator guide with a command matrix, decision path, troubleshooting notes, evidence checklist, and boundary notes for what each PASS result does and does not mean."
narrative_structure:
  - "Open with the operator problem: choose checks by change type rather than by habit."
  - "Present the core command matrix for memory bootstrap, publication checks, documentation-impact receipts, research-control checks, unit tests, and screenshot QA."
  - "Explain bootstrap versus validate-only and why generated derivatives are refreshed by the bootstrap path."
  - "Explain when project-system documentation impact, research-control validation, diff validation, unit tests, and screenshots are required."
  - "Close with common failures, final evidence expectations, and limits of validator PASS."
visual_strategy: "annotated_table"
source_basis:
  - "README.md"
  - "AGENTS.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - "scripts/README.md"
  - "tests/README.md"
  - "scripts/validate_publication_process.py"
  - "scripts/project_control/validate_documentation_impact.py"
  - "scripts/research_control/validate_research_control.py"
authority_boundaries:
  - "The page may explain existing operator command selection, bootstrap behavior, publication checks, documentation-impact checks, research-control checks, unit-test triggers, screenshot evidence, and PASS-result limits."
  - "The page may not change validator behavior, command semantics, routing behavior, documentation-impact requirements, research-control requirements, role authority, schemas, checkpoint gates, generated-output authority, or physics claim status."
  - "Validator PASS is evidence that deterministic checks passed; it is not proof of scientific truth, editorial quality, ontology adoption, benchmark promotion, or completed derivation."
output_surfaces:
  - "github-facing/validator-operator-workflow-explainer.md"
  - "html/validator-operator-workflow-explainer.html"
acceptance_criteria:
  - "Explains validation by change type."
  - "Explains bootstrap versus validate-only."
  - "Explains publication-process checks."
  - "Explains documentation-impact validation."
  - "Explains research-control validation and --check-diff."
  - "Explains unit-test trigger conditions."
  - "Explains screenshot evidence for tracked HTML pages."
  - "Explains what validator PASS does and does not mean."
  - "Includes page-specific before/after review and desktop/mobile screenshot evidence."
forbidden_patterns:
  - "New validator behavior or command semantics."
  - "Obsolete validator commands from the retired Visual Atlas flow."
  - "Claiming validators certify scientific truth, ontology adoption, benchmark promotion, completed derivation, or publication taste."
  - "Treating generated HTML, GitHub Markdown, wiki notes, Obsidian notes, semantic extracts, or .local caches as authority."
  - "Changing role authority, schemas, routing, checkpoint gates, or physics claim status."
migration_status: "reviewed"
---

# Publication Brief: Validator And Operator Workflow

This Phase 4C page explains how AEther-Flow operators choose and run the
existing check chain for documentation, memory, project-control, and
research-control work. It is a contributor/operator guide, not a validator
implementation packet, command semantics change, role change, routing change,
or physics continuation.
