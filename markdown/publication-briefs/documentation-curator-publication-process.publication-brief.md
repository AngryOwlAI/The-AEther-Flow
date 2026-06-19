---
brief_id: "PB-DOCUMENTATION-CURATOR-PUBLICATION-PROCESS"
subject: "Documentation Curator Publication Process"
reader: "Maintainer, reviewer, future agent, or external reader evaluating how AEther-Flow public pages are planned and accepted."
reader_job: "Understand how public pages move from publication brief to source spec, GitHub Markdown, standalone HTML, screenshot QA, before/after review, and deterministic checks without reviving the retired Visual Atlas or treating generated pages as authority."
document_type: "workflow_guide"
reading_experience: "A publication-lifecycle guide that explains brief-first planning, page-local structure, medium-specific outputs, reader-specific visual choices, pilot discipline, review evidence, and retired-process boundaries."
narrative_structure:
  - "Open by defining the publication process as public documentation discipline rather than a source-authority change."
  - "Explain why the publication brief is the quality-control surface and why headings remain page-local."
  - "Show how GitHub Markdown and HTML may diverge while sharing source basis, authority boundary, and core claims."
  - "Explain visual strategy as reader-specific work rather than mandatory decoration."
  - "Close with review evidence, explicit approval discipline, and retired-process anti-patterns."
visual_strategy: "process_timeline"
source_basis:
  - "research_control/design/documentation_curator_publication_process.md"
  - ".agents/roles/research_ops/documentation-curator.v2.0.0.md"
  - "markdown/publication-briefs/README.md"
  - "registries/PUBLICATION_BRIEF_REGISTRY.csv"
  - "scripts/validate_publication_process.py"
  - "research_control/tasks/RT-20260618-007/artifacts/publication_process_requirement_audit.md"
  - "research_control/tasks/RT-20260618-007/artifacts/publication_pilot_before_after_review.md"
authority_boundaries:
  - "The page may explain the active Documentation Curator publication process, publication briefs, page-local document types, medium-specific GitHub Markdown and HTML outputs, screenshot QA, before/after review, and deterministic publication checks."
  - "The page may not change role authority, validator behavior, schemas, routing, checkpoint gates, source authority, generated-output authority, physics claim status, or corpus-wide migration approval."
  - "Retired Visual Atlas, topic-registry creation, universal section headings, and active teaching-packet fallback must be described only as retired or forbidden patterns."
output_surfaces:
  - "github-facing/documentation-curator-publication-process-explainer.md"
  - "html/documentation-curator-publication-process-explainer.html"
acceptance_criteria:
  - "Explains the publication brief as the quality-control surface."
  - "Explains document types and page-local headings without imposing a universal section skeleton."
  - "Explains medium-specific divergence between GitHub Markdown and HTML."
  - "Explains visual strategy as reader-specific and optional rather than mandatory decoration."
  - "Explains pilot-first discipline and explicit approval before new page packets."
  - "Explains screenshot QA and before/after review evidence."
  - "Explains retirement of Visual Atlas, topic-registry creation path, and active teaching-packet fallback."
  - "Warns that deterministic checks catch mechanical failures but do not certify editorial quality by themselves."
forbidden_patterns:
  - "Reviving Visual Atlas as an active process."
  - "Reviving topic-registry public page creation."
  - "Reviving active teaching-packet fallback."
  - "Using old universal section headings as the public page model."
  - "Treating validator PASS as publication quality by itself."
  - "Treating generated GitHub Markdown, HTML, wiki notes, Obsidian notes, semantic extracts, or .local caches as authority."
migration_status: "reviewed"
---

# Publication Brief: Documentation Curator Publication Process

This Phase 4B page explains how AEther-Flow public documentation is planned,
written, reviewed, and checked under the active Documentation Curator
Publication Process. It is a workflow guide, not a validator change, role
change, routing change, or corpus-wide migration approval.
