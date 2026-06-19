---
brief_id: "PB-ROLE-ROUTING"
subject: "Role Routing And Execution Contracts"
reader: "Maintainer, reviewer, or future agent deciding how registered roles, task overlays, provisional roles, and execution-role records constrain a job."
reader_job: "Know how to inspect role templates and task-local execution-role records without mistaking a role name for current write permission or claim authority."
document_type: "reference_catalog"
reading_experience: "A compact reference catalog with role categories, execution-contract rules, routing decisions, and protected-authority warnings."
narrative_structure:
  - "Open by distinguishing registered role templates from the one-job execution-role record."
  - "Catalog active physics and research-ops roles by authority level, output form, validators, and gate status."
  - "Explain registered_role, task_overlay, and one_job_provisional_role decisions."
  - "Explain why role presence never expands an AgentJob allowlist by itself."
  - "Close with inspection steps and anti-patterns."
visual_strategy: "role_matrix"
source_basis:
  - "research_control/README.md"
  - "registries/AGENT_ROLE_REGISTRY.csv"
  - "registries/ROLE_EXECUTION_REGISTRY.csv"
  - ".agents/schemas/ROLE_SCHEMA.md"
  - ".agents/schemas/EXECUTION_ROLE_SCHEMA.md"
  - ".agents/roles/"
authority_boundaries:
  - "The page may explain role routing and execution contracts, but it cannot register roles, expand permissions, change role authority, change schemas, or alter routing behavior."
  - "Gate Chair remains human-gated; role routing documentation cannot promote claims or authorize Gate Chair execution."
output_surfaces:
  - "github-facing/role-routing-explainer.md"
  - "html/role-routing-explainer.html"
acceptance_criteria:
  - "Distinguishes registered role, task overlay, and one-job provisional role."
  - "Lists active physics and active research-ops role categories with gate status."
  - "Explains role authority level, may/may-not fields, and execution-role records."
  - "Explains recurring provisional-role review as a project-system signal."
  - "States that role presence does not expand a current AgentJob allowlist."
  - "Includes page-specific before/after review and desktop/mobile screenshot evidence."
forbidden_patterns:
  - "Role registration change."
  - "Role authority expansion."
  - "Omission of human-gated Gate Chair status."
  - "Template-by-convention promotion of a provisional role."
  - "Treating a role contract as current write permission without the AgentJob allowlist."
migration_status: "reviewed"
---

# Publication Brief: Role Routing And Execution Contracts

This Phase 3B page explains how role templates and task-local execution-role
records constrain work. It is a reference catalog, not a role-registration
packet or permission expansion.
