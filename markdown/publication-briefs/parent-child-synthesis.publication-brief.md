---
brief_id: "PB-PARENT-CHILD-SYNTHESIS"
subject: "Parent-Child Parallel Synthesis"
reader: "Maintainer, future agent, or reviewer trying to understand the internal perspective-synthesis mode for physics AgentJobs."
reader_job: "Understand parent_child_parallel_synthesis as one outer AgentJob with internal perspectives, inherited authority, conflict review, and one fused output."
document_type: "concept_explainer"
reading_experience: "A concept guide built around the one-job invariant, a parent/child lane explanation, a conflict-resolution rule, and a warning against child-output authority inflation."
narrative_structure:
  - "Open with the invariant: parent-child synthesis is internal decomposition, not additional AgentJobs."
  - "Explain the parent and child perspectives as analytical units that inherit the same execution-role record."
  - "Clarify inherited allowlists, source restrictions, claim boundaries, validators, and stop conditions."
  - "Explain how conflicts block PASS completion until resolved or recorded as blocked."
  - "Close with safe and unsafe summaries for future routing."
visual_strategy: "state_model"
source_basis:
  - "README.md"
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/AGENTS.md"
  - ".agents/schemas/AGENT_JOB_SCHEMA.md"
  - ".agents/schemas/EXECUTION_ROLE_SCHEMA.md"
  - "registries/AGENT_JOB_REGISTRY.csv"
authority_boundaries:
  - "The page may explain parent-child synthesis, but it cannot change the one-job rule, AgentJob schema, execution-role schema, validators, routing behavior, or physics claim status."
  - "Child outputs remain supporting draft/control artifacts and do not become independent AgentJobs, independent execution roles, or separate authority surfaces."
output_surfaces:
  - "github-facing/parent-child-synthesis-explainer.md"
  - "html/parent-child-synthesis-explainer.html"
acceptance_criteria:
  - "States one Director decision, one outer AgentJob, one execution-role record, one completion record, and one fused output."
  - "Explains inherited authority, allowlists, source restrictions, claim boundaries, validators, and stop conditions."
  - "States that child outputs are supporting draft/control artifacts."
  - "Explains that unresolved blocking conflicts prevent PASS completion."
  - "Includes page-specific before/after review and desktop/mobile screenshot evidence."
forbidden_patterns:
  - "Route around one bounded AgentJob per invocation."
  - "Child output treated as independent authority."
  - "Child execution unit described as a separate AgentJob or separate execution-role record."
  - "Claim that all future non-physics work uses this mode."
  - "Schema, validator, routing, role-authority, or physics-claim change."
migration_status: "reviewed"
---

# Publication Brief: Parent-Child Parallel Synthesis

This Phase 3B page explains the internal parent-child perspective mode used by
future physics AgentJobs. It is an explanatory publication surface, not a
schema change, role expansion, routing change, or physics claim.
