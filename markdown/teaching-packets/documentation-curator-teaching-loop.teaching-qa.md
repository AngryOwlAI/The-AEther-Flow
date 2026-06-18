---
packet_id: "documentation-curator-teaching-loop.teaching-qa.v0.1"
topic_slug: "documentation-curator-teaching-loop"
source_spec: "markdown/html-explainer-specs/documentation-curator-teaching-loop-explainer.md"
derived_outputs:
  - "html/documentation-curator-teaching-loop-explainer.html"
  - "github-facing/documentation-curator-teaching-loop-explainer.md"
audience_model: "technical_newcomer"
student_role: "documentation-student@0.1.0"
teacher_role: "documentation-teacher@0.1.0"
rounds: "2"
source_materials:
  - "AGENTS.md"
  - ".agents/roles/research_ops/documentation-curator.v1.0.0.md"
  - ".agents/roles/research_ops/documentation-student.v0.1.0.md"
  - ".agents/roles/research_ops/documentation-teacher.v0.1.0.md"
  - ".agents/schemas/TEACHING_QA_PACKET_SCHEMA.md"
claim_boundary: "Explanatory Q&A only for Documentation Curator Teaching Loop. Does not change physics claims, role authority, routing behavior, validators, or generated-output authority."
authority_status: "curated_explanatory_support"
---

# Teaching Q&A Packet: Documentation Curator Teaching Loop

## Curator Feature Selection

Plain-language topic:
Documentation Curator Teaching Loop.

Why this feature needs teaching:
Readers can confuse source authority, generated documentation, and task permission when learning the Documentation Curator teaching loop. The teaching loop repairs that confusion by asking concrete reader questions and answering only from the declared source bundle.

## Round 1 Student Questions

### Q1
What does this topic do in plain language?

### Q2
Why does AEther-Flow need this mechanism?

### Q3
Which source paths should a reader inspect first?

## Round 1 Teacher Answers

### A1
Plain answer:
The Documentation Curator teaching loop improves explanations without changing authority. The Curator selects a subject and source bundle. Documentation Student asks reader-diagnostic questions. Documentation Teacher answers only from the selected sources. The Curator turns that support into a curated teaching packet, a Markdown source spec, GitHub-facing Markdown, tracked standalone HTML, and generated wiki navigation surfaces. Student and Teacher do not write tracked docs directly.

Technical anchor:
The declared source bundle describes the mechanism and its authority boundary.

Source paths:
- AGENTS.md
- .agents/roles/research_ops/documentation-curator.v1.0.0.md
- .agents/roles/research_ops/documentation-student.v0.1.0.md

Boundary note:
This answer is explanatory support only and does not change project authority.

Curator note:
Open the public explainer with the subject mechanism before metadata.

### A2
Plain answer:
AEther-Flow needs this mechanism to keep reader understanding, project operation, source authority, and claim discipline aligned.

Technical anchor:
The root guidance and related registries separate canonical sources, project-control records, and generated derivatives.

Source paths:
- AGENTS.md
- .agents/roles/research_ops/documentation-curator.v1.0.0.md
- .agents/roles/research_ops/documentation-student.v0.1.0.md

Boundary note:
This does not add a new role, validator, route, ontology claim, or benchmark claim.

Curator note:
Use the example and non-example to show what the mechanism prevents.

### A3
Plain answer:
The reader should start with the source spec and the source bundle listed in the topic registry.

Technical anchor:
The atlas contract requires visible source paths and parity across source spec, GitHub Markdown, and HTML.

Source paths:
- AGENTS.md
- .agents/roles/research_ops/documentation-curator.v1.0.0.md
- .agents/roles/research_ops/documentation-student.v0.1.0.md

Boundary note:
Generated outputs remain noncanonical even when they are easier to read.

Curator note:
Keep the source map explicit and copyable.

## Round 2 Student Follow-up Questions

### Q1
What common misunderstanding should the final page repair?

### Q2
What is a valid project-local example?

### Q3
What must the page explicitly avoid authorizing?

## Round 2 Teacher Answers

### A1
Plain answer:
The final page should repair the mistake of treating an explanatory surface as source authority or task permission.

Technical anchor:
The project authority hierarchy distinguishes source files, registries, registered Markdown, and generated derivatives.

Source paths:
- AGENTS.md
- .agents/roles/research_ops/documentation-curator.v1.0.0.md
- .agents/roles/research_ops/documentation-student.v0.1.0.md

Boundary note:
This support material does not override the source hierarchy.

Curator note:
Put the correction in Common Confusions and What This Does Not Authorize.

### A2
Plain answer:
A hard workflow topic gets Student questions about reader confusion, Teacher answers from source paths, and Curator synthesis into source-backed public docs.

Technical anchor:
The example stays inside the declared project workflow and source bundle.

Source paths:
- AGENTS.md
- .agents/roles/research_ops/documentation-curator.v1.0.0.md
- .agents/roles/research_ops/documentation-student.v0.1.0.md

Boundary note:
The example does not promote a physics claim or widen write permissions.

Curator note:
Keep the example project-local and testable against real paths.

### A3
Plain answer:
Invalid: publishing raw Student/Teacher transcript as the public page or treating a teaching packet as role authority.

Technical anchor:
The non-example marks the authority boundary that the final page must not cross.

Source paths:
- AGENTS.md
- .agents/roles/research_ops/documentation-curator.v1.0.0.md
- .agents/roles/research_ops/documentation-student.v0.1.0.md

Boundary note:
The final page must not imply new role authority, validator authority, routing authority, ontology authority, benchmark authority, or generated-output authority.

Curator note:
Use this as the boundary panel in the public outputs.

## Curator Synthesis Notes

### Concepts that must appear in the HTML explainer
- Subject-first summary.
- Source-backed system map.
- Example, non-example, common confusions, and explicit boundary.

### Concepts that must appear in GitHub-facing Markdown
- Native Mermaid map.
- Complete source map.
- Reader-first functional opening.

### Glossary candidates
- source authority
- generated derivative
- bounded AgentJob
- claim boundary

### Common confusions to repair
- Generated docs are not source authority.
- Validator PASS is not a physics verdict.
- Tool availability is not write permission.

### Examples and non-examples
- Valid example: A hard workflow topic gets Student questions about reader confusion, Teacher answers from source paths, and Curator synthesis into source-backed public docs.
- Invalid non-example: Invalid: publishing raw Student/Teacher transcript as the public page or treating a teaching packet as role authority.

### Next reading notes
- Continue to source authority, role routing, validator workflow, and project-system improvement as needed.

### Source gaps
- None identified inside the declared source bundle for this explanatory pass.

### Claims intentionally not made
- No ontology adoption.
- No benchmark promotion.
- No completed derivation claim.
- No generated-output authority.
