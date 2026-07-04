---
brief_id: "PB-VALIDATOR-OPERATOR-WORKFLOW"
subject: "Validator And Operator Workflow"
reader: "Maintainer, reviewer, or future agent deciding which repository checks to run for documentation, memory, project-control, and research-control work."
reader_job: "Run the correct command chain for the change type, understand bootstrap versus validate-only, know when documentation-impact and research-control checks are required, understand the conditional bridge-sidecar checkpoint rule, capture screenshot evidence for tracked HTML, and avoid treating validator PASS as scientific truth, sidecar adoption, or publication taste."
document_type: "contributor_operator_guide"
reading_experience: "A practical operator guide with a command matrix, decision path, troubleshooting notes, evidence checklist, and boundary notes for what each PASS result does and does not mean."
narrative_structure:
  - "Open with the operator problem: choose checks by change type rather than by habit."
  - "Present the core command matrix for memory bootstrap, publication checks, documentation-impact receipts, research-control checks, unit tests, and screenshot QA."
  - "Explain bootstrap versus validate-only and why generated derivatives are refreshed by the bootstrap path."
  - "Explain when project-system documentation impact, research-control validation, diff validation, conditional bridge-sidecar evidence, unit tests, and screenshots are required."
  - "Close with common failures, final evidence expectations, and limits of validator PASS."
visual_strategy: "annotated_table"
source_basis:
  - "README.md"
  - "AGENTS.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - ".agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md"
  - "scripts/README.md"
  - "scripts/project_control/README.md"
  - "scripts/research_control/README.md"
  - "tests/README.md"
  - "scripts/validate_publication_process.py"
  - "scripts/project_control/validate_documentation_impact.py"
  - "scripts/project_control/generate_project_improvement_handoff.py"
  - "scripts/project_control/project_improvement_handoff_validation.py"
  - "scripts/research_control/checkpoint_research_transaction.py"
  - "scripts/research_control/validate_research_control.py"
  - "research_control/design/public_status_exists_does_not_exist_source_spec.md"
  - "research_control/design/epistemic_category_glossary.md"
  - "research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md"
authority_boundaries:
  - "The page may explain existing operator command selection, bootstrap behavior, publication checks, documentation-impact checks, research-control checks, conditional bridge-sidecar checkpoint evidence, unit-test triggers, screenshot evidence, and PASS-result limits."
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
  - "Explains that conditional bridge-sidecar acceptance is limited to exact YAML/Markdown sidecar pairs named by changed AgentJob source-bridge metadata."
  - "Explains positive and negative controls for the conditional sidecar rule without changing validator behavior."
  - "Explains unit-test trigger conditions."
  - "Explains screenshot evidence for tracked HTML pages."
  - "Explains what validator PASS does and does not mean."
  - "Includes page-specific before/after review and desktop/mobile screenshot evidence."
forbidden_patterns:
  - "New validator behavior or command semantics."
  - "Obsolete validator commands from the retired Visual Atlas flow."
  - "Claiming validators certify scientific truth, ontology adoption, benchmark promotion, completed derivation, sidecar adoption, or publication taste."
  - "Treating conditional sidecar path acceptance as a global sidecar directory allowlist."
  - "Treating generated HTML, GitHub Markdown, wiki notes, Obsidian notes, semantic extracts, or .local caches as authority."
  - "Changing role authority, schemas, routing, checkpoint gates, or physics claim status."
migration_status: "reviewed"
---

# Publication Brief: Validator And Operator Workflow

This Phase 4C page now includes the Phase 6 bridge checkpoint governance
context. It explains how AEther-Flow operators choose and run the existing
check chain for documentation, memory, project-control, research-control, and
conditional project-improvement sidecar evidence. It is a
contributor/operator guide, not a validator implementation packet, command
semantics change, role change, routing change, checkpoint change, sidecar
adoption packet, or physics continuation.
