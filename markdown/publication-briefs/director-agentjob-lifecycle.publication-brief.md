---
brief_id: "PB-DIRECTOR-AGENTJOB-LIFECYCLE"
subject: "Director Decisions And AgentJob Lifecycle"
reader: "Maintainer, reviewer, future agent, or technical reader who needs to inspect the research-control record chain."
reader_job: "Know how Director Decision Records, AgentJobs, execution roles, completions, handoffs, and registries fit together, and know when superseding is required instead of editing."
document_type: "decision_or_lifecycle_guide"
reading_experience: "A lifecycle guide with a record chain, state model, record-type matrix, immutable-record boundary, allowlist checklist, and operator mistake table."
narrative_structure:
  - "Open with the record chain from task to decision, job, execution role, completion, handoff, and registry rows."
  - "Explain lifecycle states and the immutable-after-creation rule."
  - "Separate allowed transaction evidence from broad proof or authority expansion."
  - "Explain allowlists, validators, claim boundaries, and stop conditions."
  - "Name common operator mistakes and the safe corrective action."
visual_strategy: "state_model"
source_basis:
  - "research_control/README.md"
  - "research_control/AGENTS.md"
  - ".agents/schemas/DIRECTOR_DECISION_SCHEMA.md"
  - ".agents/schemas/AGENT_JOB_SCHEMA.md"
  - ".agents/schemas/EXECUTION_ROLE_SCHEMA.md"
  - "registries/DIRECTOR_DECISION_REGISTRY.csv"
  - "registries/AGENT_JOB_REGISTRY.csv"
  - "registries/ROLE_EXECUTION_REGISTRY.csv"
authority_boundaries:
  - "The page may explain lifecycle records and operator discipline, but it cannot edit schemas, change task behavior, alter routing, or authorize mutation of historical control records."
  - "Completion records are evidence for their bounded transaction only; they do not prove broader physics, promote role authority, or authorize generated-output authority."
output_surfaces:
  - "github-facing/director-agentjob-lifecycle-explainer.md"
  - "html/director-agentjob-lifecycle-explainer.html"
acceptance_criteria:
  - "Explains task, DDR, AgentJob, execution-role record, completion, handoff, and registry relationship."
  - "States that activated or created DDRs, AgentJobs, completions, approvals, and handoffs are superseded rather than rewritten."
  - "Explains allowlists, validators, claim boundaries, and stop conditions."
  - "States that completion evidence is transaction evidence, not broad proof."
  - "Names common operator mistakes and safe corrective actions."
  - "Includes page-specific before/after review and desktop/mobile screenshot evidence."
forbidden_patterns:
  - "Schema or task-behavior edit during page migration."
  - "Implied permission to mutate historical control records."
  - "Completion record treated as broad proof."
  - "Allowlists treated as reusable general permissions."
  - "Role registration or authority expansion."
migration_status: "reviewed"
---

# Publication Brief: Director Decisions And AgentJob Lifecycle

This Phase 3A page explains the durable control-record chain used by the
research-agent workflow. It helps operators inspect and maintain task state
without mutating historical records or widening authority.
