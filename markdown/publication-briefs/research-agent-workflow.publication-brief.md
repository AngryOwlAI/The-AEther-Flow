---
brief_id: "PB-RESEARCH-AGENT-WORKFLOW"
subject: "Research-Agent Workflow"
reader: "Technical reader, maintainer, reviewer, or future agent trying to understand how AEther-Flow routes bounded physics and project-system work."
reader_job: "Understand how user requests become classified, routed, executed as one bounded AgentJob, checked, completed, and handed off without expanding authority."
document_type: "workflow_guide"
reading_experience: "A practical workflow guide with a lane split, one-job process map, memory-preflight boundary, stop conditions, and safe operating summary."
narrative_structure:
  - "Open with the purpose of the research-agent system as source-first operating discipline."
  - "Separate physics continuation from project-system improvement."
  - "Explain the one bounded AgentJob invariant from request through completion."
  - "Explain memory preflight as navigation, not authority."
  - "Clarify role contracts, execution-role records, validators, generated outputs, and human gates."
  - "Close with stop conditions and safe summary rules."
visual_strategy: "process_timeline"
source_basis:
  - "README.md"
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/AGENTS.md"
  - ".codex/skills/continue-research/SKILL.md"
  - ".codex/skills/improve-project-system/SKILL.md"
  - "registries/AGENT_ROLE_REGISTRY.csv"
authority_boundaries:
  - "The page may explain research-agent operation, but it cannot change routing behavior, role authority, validator requirements, write permissions, claim boundaries, or physics status."
  - "Memory, wiki notes, semantic extracts, Obsidian mirrors, HTML, and GitHub-facing Markdown remain navigation aids or generated noncanonical reader surfaces."
output_surfaces:
  - "github-facing/research-agent-workflow-explainer.md"
  - "html/research-agent-workflow-explainer.html"
acceptance_criteria:
  - "Explains the two linked missions and why the agent workflow exists."
  - "Separates continuation from project-system improvement."
  - "States one bounded AgentJob per invocation."
  - "Explains memory preflight as navigation, not authority."
  - "Explains role contracts and execution-role records without expanding role authority."
  - "States that validators and generated outputs are boundary checks or reader aids, not scientific verdicts."
  - "Includes page-specific before/after review and desktop/mobile screenshot evidence."
forbidden_patterns:
  - "Autonomous proof claim."
  - "Role authority expansion."
  - "Memory, wiki, semantic extract, Obsidian, HTML, or GitHub-facing Markdown treated as source authority."
  - "Validator pass treated as physics proof."
  - "New routing behavior or control-contract change."
migration_status: "reviewed"
---

# Publication Brief: Research-Agent Workflow

This Phase 3A page explains how AEther-Flow turns requests into bounded,
source-first research-control or project-system transactions. It is an
operator-facing workflow guide, not a change to routing behavior or role
authority.
