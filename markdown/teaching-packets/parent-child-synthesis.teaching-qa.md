---
packet_id: "parent-child-synthesis.teaching-qa.v0.1"
topic_slug: "parent-child-synthesis"
source_spec: "markdown/html-explainer-specs/parent-child-synthesis-explainer.md"
derived_outputs:
  - "html/parent-child-synthesis-explainer.html"
  - "github-facing/parent-child-synthesis-explainer.md"
audience_model: "technical_newcomer"
student_role: "documentation-student@0.1.0"
teacher_role: "documentation-teacher@0.1.0"
rounds: "2"
source_materials:
  - "AGENTS.md"
  - "research_control/README.md"
  - "research_control/AGENTS.md"
  - ".agents/schemas/AGENT_JOB_SCHEMA.md"
  - ".agents/schemas/EXECUTION_ROLE_SCHEMA.md"
claim_boundary: "Explanatory Q&A only for Parent-Child Parallel Synthesis. Does not change physics claims, role authority, routing behavior, validators, or generated-output authority."
authority_status: "curated_explanatory_support"
---

# Teaching Q&A Packet: Parent-Child Parallel Synthesis

## Curator Feature Selection

Plain-language topic:
Parent-Child Parallel Synthesis.

Why this feature needs teaching:
Readers can confuse source authority, generated documentation, and task permission when learning parent-child parallel synthesis. The teaching loop repairs that confusion by asking concrete reader questions and answering only from the declared source bundle.

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
Parent-child parallel synthesis increases analytical pressure inside one bounded AgentJob. A parent unit and two child-perspective units may examine the same problem from different angles, but all units inherit the outer job source restrictions, write allowlist, validators, stop conditions, claim boundary, and execution-role contract. Child outputs are support artifacts. The parent resolves conflicts into one fused output, one validation path, one completion record, and one handoff.

Technical anchor:
The declared source bundle describes the mechanism and its authority boundary.

Source paths:
- AGENTS.md
- research_control/README.md
- research_control/AGENTS.md

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
- research_control/README.md
- research_control/AGENTS.md

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
- research_control/README.md
- research_control/AGENTS.md

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
- research_control/README.md
- research_control/AGENTS.md

Boundary note:
This support material does not override the source hierarchy.

Curator note:
Put the correction in Common Confusions and What This Does Not Authorize.

### A2
Plain answer:
One physics AgentJob uses two child perspectives to test a derivation route, records a disagreement, resolves it in the fused artifact, and writes one completion.

Technical anchor:
The example stays inside the declared project workflow and source bundle.

Source paths:
- AGENTS.md
- research_control/README.md
- research_control/AGENTS.md

Boundary note:
The example does not promote a physics claim or widen write permissions.

Curator note:
Keep the example project-local and testable against real paths.

### A3
Plain answer:
Invalid: treating child perspectives as separate AgentJobs with separate permissions, claim boundaries, or completion records.

Technical anchor:
The non-example marks the authority boundary that the final page must not cross.

Source paths:
- AGENTS.md
- research_control/README.md
- research_control/AGENTS.md

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
- Valid example: One physics AgentJob uses two child perspectives to test a derivation route, records a disagreement, resolves it in the fused artifact, and writes one completion.
- Invalid non-example: Invalid: treating child perspectives as separate AgentJobs with separate permissions, claim boundaries, or completion records.

### Next reading notes
- Continue to source authority, role routing, validator workflow, and project-system improvement as needed.

### Source gaps
- None identified inside the declared source bundle for this explanatory pass.

### Claims intentionally not made
- No ontology adoption.
- No benchmark promotion.
- No completed derivation claim.
- No generated-output authority.
