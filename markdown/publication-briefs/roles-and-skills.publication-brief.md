---
brief_id: "PB-ROLES-AND-SKILLS"
subject: "Roles And Skills Catalog"
reader: "Maintainer, reviewer, or future agent trying to find active AEther-Flow role responsibilities, superseded role status, skill entry points, default validator families, and authority boundaries without treating the catalog as an execution contract."
reader_job: "Use the role and skill catalog as a navigation aid: identify the current registry row, inspect the active role contract or skill contract, then inspect the execution-role record and AgentJob before deciding current authority."
document_type: "reference_catalog"
reading_experience: "A dense but readable operator catalog with active-role grouping, superseded-role handling, skill-to-workflow mapping, validator defaults, human-gate cautions, and source-boundary reminders."
narrative_structure:
  - "Open with the rule that registries and contracts carry authority, while the public catalog is navigation."
  - "Separate active roles, superseded historical roles, and human-gated Gate Chair status."
  - "Map skill entry points to the workflows they own and what they do not own."
  - "Explain default validator families by role group."
  - "Close with a source-inspection order and forbidden overreads."
visual_strategy: "role_matrix"
source_basis:
  - "registries/AGENT_ROLE_REGISTRY.csv"
  - ".agents/roles/"
  - ".codex/skills/continue-research/SKILL.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - ".codex/skills/visual-explainer/SKILL.md"
authority_boundaries:
  - "The page may explain active and superseded role status, physics and research-ops role families, skill entry points, default validators, human-gated roles, and the source-inspection order."
  - "The page may not change role status, register a role, supersede a role, expand role authority, change skill contracts, change validator behavior, change routing behavior, change AgentJob allowlists, change checkpoint behavior, or promote physics claims."
  - "The catalog is navigation only. The current authority chain remains registry row, role or skill contract, execution-role record, AgentJob, claim boundary, completion evidence, and validation."
output_surfaces:
  - "github-facing/roles-and-skills-explainer.md"
  - "html/roles-and-skills-explainer.html"
acceptance_criteria:
  - "Explains active versus superseded role status."
  - "Separates physics roles, research-ops roles, and the human-gated Gate Chair."
  - "Maps skill entry points to owned workflow lanes."
  - "Explains default validators by role family without changing any validator."
  - "States where real authority lives."
  - "States why the page is a navigation catalog only."
  - "Includes page-specific before/after review and desktop/mobile screenshot evidence."
forbidden_patterns:
  - "Presenting the catalog as a live role contract, role registry replacement, skill contract replacement, or AgentJob allowlist."
  - "Presenting superseded roles as active."
  - "Changing or proposing role status, role authority, skill behavior, validator behavior, routing behavior, checkpoint behavior, or physics claim status."
  - "Treating Gate Chair as executable without explicit tracked human approval."
  - "Migrating Phase 5C or the whole corpus without separate explicit approval."
migration_status: "reviewed"
---

# Publication Brief: Roles And Skills Catalog

This Phase 5B page is an operator reference for AEther-Flow roles and local
skills. It helps a reader find the authoritative registry rows and contracts,
but it does not alter those rows, contracts, validators, routing behavior,
permissions, or claim status.
