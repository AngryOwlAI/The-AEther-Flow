---
brief_id: "PB-PROJECT-SYSTEM-IMPROVEMENT"
subject: "Project-System Improvement Loop"
reader: "Maintainer, reviewer, or future agent deciding how non-physics project-system drift becomes bounded work."
reader_job: "Know how documentation drift, control drift, validator gaps, memory issues, routing ambiguity, and research-improvement bridge sidecar signals become one bounded project-system AgentJob without treating project-system documentation, sidecar existence, or validator PASS as physics continuation or signal closure evidence."
document_type: "workflow_guide"
reading_experience: "A practical workflow guide that separates classifier evidence, registered signals, advisory resolver output, AgentJob boundaries, documentation-impact receipts, and signal-resolution evidence."
narrative_structure:
  - "Open by separating project-system improvement from physics continuation."
  - "Explain classification before routing and the difference between current Git diff work and registered open signals."
  - "Explain how the resolver ranks open signals and why its output is advisory rather than a hard checkpoint gate."
  - "Explain how bridge sidecars preserve the normal research handoff spine while giving /improve-project-system a separate improvement packet."
  - "Show how one bounded AgentJob records authority, evidence, receipts, and generated-output boundaries."
  - "Close with signal-resolution evidence rules, conditional checkpoint boundaries, and common failure modes."
visual_strategy: "process_timeline"
source_basis:
  - "AGENTS.md"
  - "research_control/README.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - ".agents/schemas/PROJECT_IMPROVEMENT_HANDOFF_SCHEMA.md"
  - "scripts/project_control/classify_project_changes.py"
  - "scripts/project_control/resolve_project_improvement.py"
  - "scripts/project_control/generate_project_improvement_handoff.py"
  - "scripts/project_control/project_improvement_handoff_validation.py"
  - "scripts/project_control/README.md"
  - "scripts/research_control/checkpoint_research_transaction.py"
  - "scripts/research_control/validate_research_control.py"
  - "scripts/research_control/README.md"
  - "registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv"
  - "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
  - "research_control/tasks/RT-20260622-007/artifacts/project_improvement_bridge_phase6_checkpoint_allowlist_governance.md"
authority_boundaries:
  - "The page may explain project-system improvement routing, documentation-impact receipts, signal registries, resolver output, generated project-improvement sidecars, conditional sidecar checkpoint allowlisting, and evidence requirements, but it cannot create signals, create sidecars, resolve signals, change validators, alter routing behavior, register roles, or expand AgentJob permissions."
  - "Project-system improvement is separate from physics continuation; this page cannot promote physics claims, authorize ontology edits, make Gate Chair decisions, or treat generated documentation as authority."
output_surfaces:
  - "github-facing/project-system-improvement-explainer.md"
  - "html/project-system-improvement-explainer.html"
acceptance_criteria:
  - "Explains classification before routing."
  - "Distinguishes current Git diff work from registered open signals."
  - "States that resolver output is advisory and checkpoint blocking comes from validators or concrete authority violations."
  - "Explains signal type registry versus signal instance registry."
  - "Explains that project-improvement sidecars are separate from normal research handoffs and are consumed by /improve-project-system."
  - "Explains that conditional checkpoint and --check-diff sidecar acceptance is exact-path and source-bridge based, not a global sidecar directory allowance."
  - "Explains one bounded AgentJob per invocation."
  - "Explains documentation-impact receipts for state-changing project-system AgentJobs."
  - "Explains evidence required to move a signal out of open backlog."
  - "Includes page-specific before/after review and desktop/mobile screenshot evidence."
forbidden_patterns:
  - "Physics continuation or claim-promotion instructions."
  - "Signal resolution without completion or rejection evidence."
  - "Treating resolver output as a hard checkpoint gate by itself."
  - "Changing signal types, signal rows, validators, role authority, routing behavior, or checkpoint behavior."
  - "Creating live project-improvement sidecars, replacing normal research handoffs, or implying sidecar registry integration."
  - "Treating generated documentation, wiki notes, Obsidian notes, semantic extracts, or .local caches as authority."
migration_status: "reviewed"
---

# Publication Brief: Project-System Improvement Loop

This Phase 4A page now includes the Phase 6 bridge checkpoint governance
context for project-improvement sidecars. It explains how project-system
problems become bounded project-control work, while preserving the normal
research handoff spine and keeping sidecars in the project-system lane. It is
a workflow guide, not a signal-registration packet, sidecar-creation packet,
validator change, routing change, checkpoint change, or physics continuation.
