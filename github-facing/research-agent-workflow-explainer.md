# Research-Agent Workflow

AEther-Flow uses its research-agent workflow as an operating discipline for
turning requests into bounded, inspectable transactions. A request first has
to be understood as either physics continuation, project-system improvement,
or a stop condition. The workflow then uses memory as navigation, verifies any
useful memory hit against canonical sources or registry rows, selects one
execution lane, binds the work to a role or execution-role record, runs only
the allowed job, and records validation and handoff evidence.

The important constraint is not speed. The important constraint is that each
state change remains small enough to audit. A physics packet can search,
construct, refute, or hand off without promoting a claim. A project-system
packet can repair documentation, validators, memory tooling, or control
records without changing physics status. Generated pages, local caches, and
validator success remain supporting evidence for their own transaction, not
source authority.

## Process Lane

The reader learns how a request narrows from intake to exactly one bounded
AgentJob and then to completion or handoff.

| Step | Narrowing action | Boundary preserved |
| --- | --- | --- |
| Request | Identify whether the user is asking for physics continuation, project-system improvement, documentation, validation, or a stop condition. | No action before source inspection. |
| Classify or resolve | Run the relevant classifier or resolve tracked control state. | Advisory routing does not override validators. |
| Memory preflight | Use memory to find likely sources and prior decisions. | Memory is navigation, not authority. |
| Source inspection | Inspect the canonical file or registry row named by useful memory hits. | Source authority remains tracked. |
| One lane | Route one physics or project-system AgentJob. | No hidden second objective. |
| Completion | Run checks, record outputs, and hand off if needed. | Completion proves only the bounded transaction. |

## Two Operating Lanes

| Lane | Use it for | Primary skill | Authority limit |
| --- | --- | --- | --- |
| Physics continuation | Derivation work, candidate construction, refutation, audit, theoretical packet selection, or controlled scientific handoff. | `.codex/skills/continue-research/SKILL.md` | Does not promote claims without required gates. |
| Project-system improvement | Documentation drift, validator work, role or schema maintenance, memory tooling, workflow clarification, or public explainer packets. | `.codex/skills/improve-project-system/SKILL.md` | Does not change physics status or canonical science sources. |

The lane matters because the honest next step differs by problem type. A
missing theoretical datum may authorize one bounded physics packet. A stale
public explanation may authorize one Documentation Curator packet. A request
that needs role authority, schema behavior, routing behavior, checkpoint
behavior, ontology adoption, or claim promotion needs its own protected path.

## Memory And Source Inspection

Memory preflight is required before current routing and AgentJob creation. It
helps find prior tasks, registered source objects, and relevant decision
history. It does not decide truth. It does not override the hierarchy in
`AGENTS.md`, where registered TeX, registries, and registered Markdown remain
the authority layers.

The safe rule is direct: if memory influences routing, claim language, source
selection, or project-control changes, inspect the canonical source file or
CSV registry row named by the hit. Obsidian notes, wiki notes, semantic
extracts, `.local` files, and the SQLite memory index are retrieval layers.
Freshness warnings from those layers can be useful maintenance signals while
remaining non-authoritative.

## One Bounded AgentJob

The workflow reduces action to one bounded AgentJob per invocation. The
AgentJob states allowed reads, allowed writes, generated paths, forbidden
paths, source classes, validators, expected outputs, and claim boundary. Its
role binding says whether the job uses a registered role directly, a
task-local overlay, or a one-job provisional role.

This one-job invariant prevents silent widening. A documentation repair should
not become a schema change by accident. A physics construction should not
become benchmark promotion by wording drift. A validator pass should not be
treated as scientific proof.

## Roles, Gates, And Outputs

`registries/AGENT_ROLE_REGISTRY.csv` records role identity, authority level,
human-gate status, and default checks. A role contract is a template; an
execution-role record and AgentJob allowlist are the task-local authority
surface for one transaction.

Protected authority remains protected. Ontology adoption, benchmark promotion,
Gate Chair approval, role authority expansion, and claim promotion require the
appropriate human-gated path. Generated GitHub Markdown, tracked HTML, wiki
notes, semantic extracts, Obsidian mirrors, and local caches remain reader or
retrieval derivatives.

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
  authority; or
- require more than one AgentJob to complete honestly.

A stop condition is useful information. It marks the next honest boundary.

## Reader Scope

Reader scope: public workflow orientation only. This explanation cannot change
routing behavior, role authority, validator requirements, write permissions,
claim boundaries, or physics status.

<!-- explainer-control: authority_footer -->

## Source Binding And Authority

- **Derived from spec:** `markdown/html-explainer-specs/research-agent-workflow-explainer.md`
- **Related HTML:** `html/research-agent-workflow-explainer.html`
- **Publication brief:** `markdown/publication-briefs/research-agent-workflow.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

This page is a generated noncanonical reader surface. It explains the
workflow, but it does not change routing behavior, role authority, validator
requirements, write permissions, claim boundaries, or physics status.

## Source Materials

- AEther-Flow Project. (2026). `README.md` [Project front door].
- AEther-Flow Project. (2026). `AGENTS.md` [Repository authority hierarchy].
- AEther-Flow Project. (2026). `research_control/README.md` [Research-control guide].
- AEther-Flow Project. (2026). `research_control/AGENTS.md` [Scoped research-control guidance].
- AEther-Flow Project. (2026). `.codex/skills/continue-research/SKILL.md` [Continuation workflow].
- AEther-Flow Project. (2026). `.codex/skills/improve-project-system/SKILL.md` [Project-system workflow].
- AEther-Flow Project. (2026). `registries/AGENT_ROLE_REGISTRY.csv` [Agent role registry].

## Safe Operating Summary

Safe summary: AEther-Flow routes physics continuation and project-system
improvement through one bounded AgentJob, source inspection, role constraints,
checks, completion evidence, and human gates.

Unsafe summary: the workflow proves physics autonomously, memory overrides
tracked sources, validators promote claims, generated pages are authority, or a
role template grants permission beyond the current execution-role record.
