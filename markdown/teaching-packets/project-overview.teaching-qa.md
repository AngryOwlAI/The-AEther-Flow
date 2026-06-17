---
packet_id: "project-overview.teaching-qa.v0.1"
topic_slug: "project-overview"
source_spec: "markdown/html-explainer-specs/project-overview-explainer.md"
derived_outputs:
  - "html/project-overview-explainer.html"
  - "github-facing/project-overview-explainer.md"
audience_model: "layperson"
student_role: "documentation-student@0.1.0"
teacher_role: "documentation-teacher@0.1.0"
rounds: 2
source_materials:
  - "README.md"
  - "AGENTS.md"
  - "ontology/aether-and-aether-flow.md"
  - "research_control/README.md"
  - "registries/CLAIM_BOUNDARY_REGISTRY.csv"
  - "markdown/html-explainer-specs/source-authority-explainer.md"
claim_boundary: "Explanatory Q&A only. Does not change physics claims, role authority, routing behavior, validators, or generated-output authority."
authority_status: "curated_explanatory_support"
---

# Teaching Q&A Packet: Project Overview

## Curator Feature Selection

Plain-language topic:
AEther-Flow has two linked systems: a physics research system and an AI
research-agent system.

Why this feature needs teaching:
Readers can mistake the project for a finished physics theory, a set of visual
documentation pages, or an unrestricted autonomous agent workflow. The teaching
loop should explain the actual project functionality: how the physics lane and
the agent-control lane work together while preserving source authority.

## Round 1 Student Questions

### Q1
What is the project trying to do in plain language?

### Q2
Why are there two lanes instead of one ordinary research folder?

### Q3
What is accepted physics in the project, and what remains open?

### Q4
What does the AI research-agent system do?

### Q5
Why are generated explanations not enough by themselves?

## Round 1 Teacher Answers

### A1
Plain answer:
The project studies whether an Æther-flow substrate can explain ordinary
relativistic geometry while building a controlled agent workflow for doing
that research without losing track of claims, sources, or failures.

Technical anchor:
The root guidance names two linked missions: physics research around an
exact-GR benchmark and AI research-agent development using routing,
refutation, novelty search, claim gates, manuscript memory, and negative-result
preservation.

Source paths:
- README.md
- AGENTS.md

Boundary note:
This answer does not promote the Æther-flow derivation to completed physics.

Curator note:
The final docs should open with the two-system model rather than with page
metadata.

### A2
Plain answer:
The physics lane asks the scientific question, while the agent lane controls
how work on that question is selected, bounded, checked, recorded, and handed
off.

Technical anchor:
The research-control guidance separates research continuation from
project-system improvement. The root guidance also separates canonical physics
sources, registries, registered Markdown, and generated derivatives.

Source paths:
- AGENTS.md
- research_control/README.md

Boundary note:
This answer does not make workflow machinery a source of physics claims.

Curator note:
Use a simple two-lane diagram or prose map: physics target on one side,
research-control machinery on the other.

### A3
Plain answer:
Ordinary exact general relativity is the observable benchmark. A
first-principles derivation from Æther or Æther-flow substrate structure
remains open until authorized gates establish it.

Technical anchor:
The root guidance explicitly says exact GR is maintained as benchmark while
first-principles derivation from the substrate is open. Claim-boundary records
exist to keep status language constrained.

Source paths:
- AGENTS.md
- ontology/aether-and-aether-flow.md
- registries/CLAIM_BOUNDARY_REGISTRY.csv

Boundary note:
This answer distinguishes benchmark adoption from derivation success.

Curator note:
The final docs should repeat this distinction wherever the physics lane is
introduced.

### A4
Plain answer:
The AI research-agent system turns requests and continuation state into one
bounded job with a selected role, allowed paths, expected outputs, validators,
completion evidence, and the next handoff.

Technical anchor:
Research-control guidance describes tracked state, Director decisions,
AgentJobs, role records, artifacts, completion records, handoffs, and registry
updates as the operating path.

Source paths:
- research_control/README.md
- AGENTS.md

Boundary note:
This answer does not grant agents authority outside their selected job.

Curator note:
The final docs should describe the agent system as a governance workflow, not
as generic AI assistance.

### A5
Plain answer:
Generated explanations are useful for humans, but they are not the source of
truth. They must point back to registered sources, registries, and task
records.

Technical anchor:
The authority hierarchy states that PDFs, wiki notes, generated indexes,
HTML explainers, and generated registry outputs are derivative artifacts.

Source paths:
- AGENTS.md
- markdown/html-explainer-specs/source-authority-explainer.md

Boundary note:
Generated outputs do not override canonical TeX, registries, registered
Markdown, or control records.

Curator note:
The final docs should keep source authority visible without letting
nonauthority warnings replace the functional explanation.

## Round 2 Student Follow-up Questions

### Q1
How should a new reader move through the project without getting lost?

### Q2
What can go wrong if the physics lane and agent lane are confused?

### Q3
How do roles help protect the project?

### Q4
What should a reader check before trusting a result?

## Round 2 Teacher Answers

### A1
Plain answer:
A new reader should first understand the two lanes, then read ontology and
claim gates for physics status, research system and role routing for workflow,
and source authority before citing generated material.

Technical anchor:
The explainer set is organized around ontology, research workflow, control
system, role routing, claim gates, source authority, roles and skills, memory,
and technical requirements.

Source paths:
- README.md
- markdown/html-explainer-specs/source-authority-explainer.md

Boundary note:
This reading path is orientation only and does not create new authority.

Curator note:
Use the final overview as a routing map by reader need, not by file order.

### A2
Plain answer:
Confusion can make a workflow pass look like a physics result or make a
generated explanation look like a source.

Technical anchor:
The root guidance distinguishes canonical physics sources, registries,
registered Markdown, and derivative artifacts. The research-control guidance
requires bounded jobs and validation before checkpointing.

Source paths:
- AGENTS.md
- research_control/README.md

Boundary note:
The answer does not add a new validator rule; it explains the existing
authority hierarchy.

Curator note:
Use examples and non-examples to show that a completed AgentJob is not a Gate
Chair verdict.

### A3
Plain answer:
Roles keep different kinds of work from borrowing each other's authority.

Technical anchor:
The project distinguishes physics roles, documentation roles, project-control
roles, validator roles, and support subroles. Each task records the selected
role and execution boundary before work proceeds.

Source paths:
- research_control/README.md
- AGENTS.md

Boundary note:
This answer does not register or expand any role.

Curator note:
The overview should point readers to role-routing and roles-and-skills for the
full authority map.

### A4
Plain answer:
Before trusting a result, inspect the relevant source file, registry row,
AgentJob, completion record, validators, and claim boundary.

Technical anchor:
The authority hierarchy and research-control workflow make source rows,
decision records, job YAML, completion receipts, and validators the evidence
path.

Source paths:
- AGENTS.md
- research_control/README.md
- registries/CLAIM_BOUNDARY_REGISTRY.csv

Boundary note:
This answer does not make generated HTML, GitHub-facing Markdown, wiki notes,
PDFs, or local caches independent authority.

Curator note:
End the final docs with a verification path that sends readers back to sources.

## Curator Synthesis Notes

### Concepts that must appear in the HTML explainer

- Two linked systems: physics research and AI research-agent governance.
- Exact GR is the benchmark; first-principles substrate derivation remains
  open.
- Agent workflow creates bounded, inspectable jobs rather than autonomous
  proof.
- Source authority controls which files can support claims.
- Generated derivatives explain and route; they do not authorize.

### Concepts that must appear in GitHub-facing Markdown

- Start-here summary of the two lanes.
- Plain-language explanation of accepted benchmark versus open derivation.
- Guided path from reader need to source family.
- Common questions and misunderstandings.
- External AI navigation rules.
- Source-backed next reading path.

### Glossary candidates

- Physics lane: the research lane for ontology, benchmark, derivation burden,
  claim gates, audits, refutations, and candidate work.
- AI research-agent lane: the workflow lane for Director decisions, AgentJobs,
  roles, validators, completions, handoffs, and memory.
- Benchmark: ordinary exact GR as observable target.
- Open derivation: substrate-to-GR recovery not yet promoted.
- Derivative surface: generated or reader-facing output that points back to
  authority.

### Common confusions to repair

- A visual explanation is not a physics result.
- A completed AgentJob is not scientific acceptance.
- A memory search result is not stronger than its source row.
- A role can help only inside its selected task boundary.
- Exact-GR benchmark adoption is not the same as substrate derivation.

### Examples and non-examples

- Example: a reader uses the overview to route from ontology to claim gates.
- Example: an agent uses research-control state before creating one bounded
  job.
- Non-example: a GitHub-facing explanation promotes a claim.
- Non-example: generated HTML overrides a source spec.
- Non-example: a validator pass closes an open physics derivation.

### Next reading notes

- Read `ontology/aether-and-aether-flow.md` for project vocabulary.
- Read `registries/CLAIM_BOUNDARY_REGISTRY.csv` for claim boundaries.
- Read `research_control/README.md` for job workflow.
- Read `markdown/html-explainer-specs/source-authority-explainer.md` for the
  authority ladder.

### Source gaps

- No source gap for the selected project-overview teaching scope.

### Claims intentionally not made

- No physics claim is changed.
- No first-principles derivation is completed.
- No role authority is expanded.
- No routing behavior is changed.
- No validator behavior is changed.
- No generated output becomes authoritative.
