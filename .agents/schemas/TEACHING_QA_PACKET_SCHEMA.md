---
schema_id: "TEACHING_QA_PACKET_SCHEMA"
version: "0.1.0"
status: "active"
---

# Teaching Q&A Packet Schema

Teaching Q&A packets are Curator-reviewed explanatory support for source-backed
HTML explainers. They are not canonical science, registry, role, schema,
validator, routing, or generated-output authority.

## Required Frontmatter Fields

- `packet_id`
- `topic_slug`
- `source_spec`
- `derived_outputs`
- `audience_model`
- `student_role`
- `teacher_role`
- `rounds`
- `source_materials`
- `claim_boundary`
- `authority_status`

## Required Body Sections

- `## Curator Feature Selection`
- `## Round 1 Student Questions`
- `## Round 1 Teacher Answers`
- `## Round 2 Student Follow-up Questions`
- `## Round 2 Teacher Answers`
- `## Curator Synthesis Notes`

The Curator synthesis section must include:

- `### Concepts that must appear in the HTML explainer`
- `### Concepts that must appear in GitHub-facing Markdown`
- `### Glossary candidates`
- `### Common confusions to repair`
- `### Examples and non-examples`
- `### Next reading notes`
- `### Source gaps`
- `### Claims intentionally not made`

## Rules

- Student sections contain questions only.
- Teacher sections must answer every Student question.
- Teacher answers must include a plain answer, technical anchor, source paths,
  boundary note, and Curator note.
- Packet `source_materials` must be selected from the source spec's declared
  `source_materials`.
- Packets may not cite generated HTML, wiki notes, PDFs, or `.local/` output as
  authority.
- Source gaps must be labeled explicitly rather than filled from outside
  knowledge.
- The Curator may distill the packet into source specs and GitHub-facing
  Markdown, but the packet itself does not change project behavior or claim
  status.
