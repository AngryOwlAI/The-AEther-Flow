---
brief_id: "PB-SOURCE-AUTHORITY"
subject: "Source Authority And Generated Derivatives"
reader: "Contributor, maintainer, or external AI deciding which files may be cited as authority."
reader_job: "Distinguish canonical sources from generated or local retrieval surfaces before summarizing, editing, or routing work."
document_type: "comparison_or_boundary_map"
reading_experience: "Boundary-map reference with a trust ladder, failure modes, and an action checklist."
narrative_structure:
  - "Start with the trust question."
  - "Present authority layers as a matrix."
  - "Explain how to use generated pages without overclaiming."
  - "Close with common failure modes and a source-first checklist."
visual_strategy: "source_matrix"
source_basis:
  - "AGENTS.md"
  - ".codex/skills/project-memory-system/SKILL.md"
  - ".codex/skills/html-visual-explainer/SKILL.md"
  - "registries/MARKDOWN_SOURCE_REGISTRY.csv"
  - "registries/HTML_EXPLAINER_REGISTRY.csv"
  - "registries/WIKI_ARTIFACT_REGISTRY.csv"
  - "registries/FILE_OBJECT_REGISTRY.csv"
authority_boundaries:
  - "Generated and local retrieval layers are useful only when traced back to registered sources."
  - "The page does not change the authority hierarchy or grant generated-output authority."
output_surfaces:
  - "github-facing/source-authority-explainer.md"
  - "html/source-authority-explainer.html"
acceptance_criteria:
  - "Opens with the trust problem, not metadata."
  - "Uses a page-specific authority matrix rather than a generic system map."
  - "Names concrete source surfaces and generated surfaces."
  - "HTML is standalone, accessible, mobile-safe, and screenshot verified."
forbidden_patterns:
  - "Old universal heading sequence."
  - "Raw Student/Teacher transcript shape."
  - "Claiming a generated page, wiki note, PDF, semantic extract, Obsidian note, or .local cache is authority."
migration_status: "reviewed"
---

# Publication Brief: Source Authority And Generated Derivatives

The Source Authority pilot should act as a trust boundary map. It should make
generated surfaces easier to use while making them harder to overclaim.
