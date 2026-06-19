# Research-Agent Workflow

AEther-Flow uses a research-agent workflow to keep theoretical work auditable.
The workflow does not replace scientific proof, human gates, or source
authority. It is the operating discipline that turns a request into one
bounded transaction with explicit sources, role limits, checks, and completion
evidence.

This page is a generated noncanonical reader surface. It explains the
workflow, but it does not change routing behavior, role authority, validator
requirements, write permissions, claim boundaries, or physics status.

## Operating Lanes

The repository has two linked missions: a physics research program and an AI
research-agent system. The workflow exists because both missions need bounded
state changes.

| Lane | Use it for | Primary skill | Authority limit |
| --- | --- | --- | --- |
| Physics continuation | Derivation work, candidate construction, refutation, audit, theoretical packet selection, or controlled scientific handoff. | `.codex/skills/continue-research/SKILL.md` | Does not promote claims without the required gates. |
| Project-system improvement | Documentation drift, validator work, role or schema maintenance, memory tooling, workflow clarification, or public explainer packets. | `.codex/skills/improve-project-system/SKILL.md` | Does not change physics status or canonical science sources. |

The lane matters because each one has different stop conditions. A missing
scientific datum may justify a bounded research packet. A stale documentation
surface may justify a Documentation Curator packet. Neither lane allows a
generated page, local cache, or validator pass to become source authority.

## Request To Bounded Job

The usual path is deliberately narrow:

1. Inspect repository guidance, tracked state, and relevant registries.
2. Run memory preflight as navigation.
3. Classify the request or resolve the active research-control state.
4. Route exactly one bounded AgentJob when a state change is authorized.
5. Bind the job to a role or execution-role record.
6. Execute only the allowed read and write paths.
7. Run the required checks.
8. Write completion evidence and any required handoff or documentation-impact
   receipt.

The key invariant is one bounded AgentJob per invocation. The rule is not a
ceremony. It prevents a documentation repair from silently becoming a schema
change, and it prevents a physics packet from silently becoming a claim
promotion.

## Memory As Navigation

Memory preflight is required before current routing and AgentJob creation. It
helps find relevant source objects and prior decisions, but it does not decide
truth or authority.

The source rule is simple: if memory influences routing, claim language, source
selection, or project-control changes, inspect the canonical file or registry
row named by the memory hit. Obsidian notes, wiki notes, content-semantic
extracts, `.local` files, and the memory index remain retrieval layers only.

This is why stale local retrieval warnings can coexist with a valid
transaction. They are useful maintenance information, not source authority.

## Role Authority And Human Gates

`registries/AGENT_ROLE_REGISTRY.csv` records role identity, authority level,
human-gate status, and default checks. A registered role is a template. The
execution-role record is the task-local contract that states the exact role
semantics for one AgentJob.

The workflow distinguishes:

- registered role: the template fits without authority change;
- task overlay: the same role is used with explicit task-local constraints or
  non-protected adjustments;
- one-job provisional role: a temporary role exists for one job and is not
  reusable until registered.

Protected authority remains protected. Ontology adoption, benchmark promotion,
Gate Chair approval, role authority expansion, and claim promotion require the
appropriate human-gated path. A normal AgentJob cannot imply those outcomes by
finishing successfully.

## Validators And Generated Outputs

Checks enforce the transaction boundary. They can detect malformed YAML,
missing documentation-impact evidence, orphan public pages, unsafe authority
phrasing, write-path violations, or registry drift.

They do not prove physics. They do not authorize ontology adoption. They do
not promote a benchmark. They do not turn generated public documentation into
source authority.

Generated outputs have specific jobs:

| Output | Useful for | Boundary |
| --- | --- | --- |
| GitHub-facing Markdown | Human-readable orientation. | Generated noncanonical reader surface. |
| Tracked HTML | Human-only visual explanation. | Generated noncanonical reader surface. |
| Wiki notes and indexes | Retrieval and navigation. | Generated derivative, not authority. |
| `.local` caches | Scratch, mirrors, previews, and indexes. | Local retrieval layer only. |

## Stop Conditions

The workflow should stop or route a different bounded packet when the requested
work would:

- edit canonical ontology, benchmark, or science-draft sources without the
  required gate;
- mutate activated or completed control records instead of superseding them;
- write outside the AgentJob allowlist;
- change role authority, schema behavior, validator behavior, routing
  behavior, or checkpoint gates without a matching project-system packet;
- treat a generated output, validator pass, or memory hit as scientific
  authority;
- require more than one AgentJob to complete honestly.

A stop condition is not failure. It is the control system identifying the
next honest boundary.

## Source Materials

- AEther-Flow Project. (2026). `README.md` [Project front door].
- AEther-Flow Project. (2026). `AGENTS.md` [Repository authority hierarchy].
- AEther-Flow Project. (2026). `research_control/README.md` [Research-control guide].
- AEther-Flow Project. (2026). `research_control/AGENTS.md` [Scoped research-control guidance].
- AEther-Flow Project. (2026). `.codex/skills/continue-research/SKILL.md` [Continuation workflow].
- AEther-Flow Project. (2026). `.codex/skills/improve-project-system/SKILL.md` [Project-system workflow].
- AEther-Flow Project. (2026). `registries/AGENT_ROLE_REGISTRY.csv` [Agent role registry].

## Source Binding

- **Derived from spec:** `markdown/html-explainer-specs/research-agent-workflow-explainer.md`
- **Related HTML:** `html/research-agent-workflow-explainer.html`
- **Publication brief:** `markdown/publication-briefs/research-agent-workflow.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

## Safe Operating Summary

Safe summary: AEther-Flow routes physics continuation and project-system
improvement through one bounded AgentJob, source inspection, role constraints,
checks, completion evidence, and human gates.

Unsafe summary: the workflow proves physics autonomously, memory overrides
tracked sources, validators promote claims, generated pages are authority, or a
role template grants permission beyond the current execution-role record.
