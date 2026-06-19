---
brief_id: "PB-PROJECT-SYSTEM-IMPROVEMENT"
subject: "Project-System Improvement Loop"
reader: "Maintainer, reviewer, or future agent deciding how non-physics project-system drift becomes bounded work."
reader_job: "Know how documentation drift, control drift, validator gaps, memory issues, and routing ambiguity become one bounded project-system AgentJob without treating project-system documentation as physics continuation or signal closure evidence."
document_type: "workflow_guide"
reading_experience: "A practical workflow guide that separates classifier evidence, registered signals, advisory resolver output, AgentJob boundaries, documentation-impact receipts, and signal-resolution evidence."
narrative_structure:
  - "Open by separating project-system improvement from physics continuation."
  - "Explain classification before routing and the difference between current Git diff work and registered open signals."
  - "Explain how the resolver ranks open signals and why its output is advisory rather than a hard checkpoint gate."
  - "Show how one bounded AgentJob records authority, evidence, receipts, and generated-output boundaries."
  - "Close with signal-resolution evidence rules and common failure modes."
visual_strategy: "process_timeline"
source_basis:
  - "AGENTS.md"
  - "research_control/README.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - "scripts/project_control/classify_project_changes.py"
  - "scripts/project_control/resolve_project_improvement.py"
  - "registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv"
  - "registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv"
authority_boundaries:
  - "The page may explain project-system improvement routing, documentation-impact receipts, signal registries, resolver output, and evidence requirements, but it cannot create signals, resolve signals, change validators, alter routing behavior, register roles, or expand AgentJob permissions."
  - "Project-system improvement is separate from physics continuation; this page cannot promote physics claims, authorize ontology edits, make Gate Chair decisions, or treat generated documentation as authority."
output_surfaces:
  - "github-facing/project-system-improvement-explainer.md"
  - "html/project-system-improvement-explainer.html"
acceptance_criteria:
  - "Explains classification before routing."
  - "Distinguishes current Git diff work from registered open signals."
  - "States that resolver output is advisory and checkpoint blocking comes from validators or concrete authority violations."
  - "Explains signal type registry versus signal instance registry."
  - "Explains one bounded AgentJob per invocation."
  - "Explains documentation-impact receipts for state-changing project-system AgentJobs."
  - "Explains evidence required to move a signal out of open backlog."
  - "Includes page-specific before/after review and desktop/mobile screenshot evidence."
forbidden_patterns:
  - "Physics continuation or claim-promotion instructions."
  - "Signal resolution without completion or rejection evidence."
  - "Treating resolver output as a hard checkpoint gate by itself."
  - "Changing signal types, signal rows, validators, role authority, routing behavior, or checkpoint behavior."
  - "Treating generated documentation, wiki notes, Obsidian notes, semantic extracts, or .local caches as authority."
migration_status: "reviewed"
---

# Publication Brief: Project-System Improvement Loop

This Phase 4A page explains how project-system problems become bounded
project-control work. It is a workflow guide, not a signal-registration
packet, validator change, routing change, or physics continuation.
