# Project-System Improvement Loop

Project-system improvement is the maintenance lane for the research system itself. It handles documentation drift, control-contract drift, validator gaps, memory retrieval problems, trigger logic, generated-document pipelines, and routing ambiguity. It is deliberately separate from physics continuation: it can repair the operating machinery around the research, but it cannot promote ontology, benchmark status, Gate Chair decisions, or completed derivation language.

The loop starts from observable evidence. A current working-tree diff can trigger the classifier. A registered open signal can trigger advisory routing. Useful memory hits can point to prior decisions, but they must lead back to canonical source files and registry rows before they influence action. Only after that source inspection does the Director route one bounded AgentJob with a write-path allowlist and a claim boundary.

A reader should come away with a practical rule: classify or resolve the state first, execute at most one project-system packet, record documentation impact when the packet changes state, and close any signal only with explicit PASS completion evidence or a documented rejection decision.

## Improvement Loop Map

| Item | Function | Boundary |
| --- | --- | --- |
| Observed issue | Current Git diff, registered open signal, or a repeated workflow problem. | No action is authorized before source inspection. |
| Memory preflight | Status plus targeted lookup or search identifies likely prior context. | Memory is navigation; source files and registry rows remain authority. |
| Classification | The classifier determines live documentation-impact and project-system reason codes. | Classification is routing evidence, not correctness proof. |
| Resolver | The resolver ranks open signals against live diff state. | Resolver output is advisory unless validators or boundaries fail. |
| One AgentJob | The selected role executes one bounded write-path packet. | No hidden second objective or permission expansion. |
| Completion | Checks, documentation-impact receipt, and completion evidence close the transaction. | Signals close only with explicit evidence. |

## Diff, Signal, Resolver

| Item | Function | Boundary |
| --- | --- | --- |
| Current diff | Changed paths drive immediate classifier output. | Use when the working tree already contains project-system or documentation-impact work. |
| Registered signal | A concrete row in the signal registry records backlog or routed project-system work. | High or critical open signals outrank ordinary backlog. |
| Advisory resolver | The resolver compares those inputs and recommends one boundary. | It does not create a hard checkpoint gate by itself. |

## Evidence To Close A Signal

| Item | Function | Boundary |
| --- | --- | --- |
| resolved_by_job_id | Names the bounded AgentJob that resolved, completed, or closed the signal. | Required for non-open terminal states. |
| resolution_evidence_path | Points to a PASS completion YAML with matching job_id, or to a rejection decision. | Command strings stay in the completion record. |
| resolved_at | Records the timestamp for the resolution row. | Resolution must be auditable, not implied by prose. |

## Failure Boundaries

| Item | Function | Boundary |
| --- | --- | --- |
| Free-text signal | A completion mentions a signal term that is absent from the registry. | Register or reject through the controlled signal path. |
| Resolver overread | A future recommendation is treated as a hard checkpoint block. | Use validators and concrete authority violations as hard gates. |
| Receipt gap | A project-system AgentJob changes state without documentation impact. | Write the receipt or stop before checkpointing. |
| Physics overreach | A project-system packet changes science status. | Route physics continuation or human-gated authority separately. |

## Reader Scope

Reader scope: project-system workflow orientation only. This page cannot create or close signals, change routing behavior, change validator behavior, expand role authority, or authorize physics claim promotion.

<!-- explainer-control: authority_footer -->

## Source Binding And Authority

- **Derived from spec:** `markdown/html-explainer-specs/project-system-improvement-explainer.md`
- **Related HTML:** `html/project-system-improvement-explainer.html`
- **Publication brief:** `markdown/publication-briefs/project-system-improvement.publication-brief.md`
- **Authority status:** generated noncanonical reader surface

This page is a generated noncanonical reader surface. It explains classifier output, registered signal routing, advisory resolver output, one bounded AgentJob execution, documentation-impact receipts, and signal-resolution evidence without changing validators, routing behavior, role authority, signal rows, signal types, checkpoint behavior, generated-output authority, or physics claim status.

## Source Materials

- AEther-Flow Project. (2026). `AGENTS.md` [Root authority hierarchy and the split between physics continuation and project-system work.]
- AEther-Flow Project. (2026). `research_control/README.md` [Research-control memory preflight, project-system signal, documentation-impact, and resolver rules.]
- AEther-Flow Project. (2026). `.codex/skills/improve-project-system/SKILL.md` [Execution workflow for project-system improvement packets.]
- AEther-Flow Project. (2026). `scripts/project_control/classify_project_changes.py` [Deterministic current-diff classification.]
- AEther-Flow Project. (2026). `scripts/project_control/resolve_project_improvement.py` [Advisory routing across current diffs and open signals.]
- AEther-Flow Project. (2026). `registries/PROJECT_IMPROVEMENT_SIGNAL_TYPE_REGISTRY.csv` [Controlled signal vocabulary and default routing metadata.]
- AEther-Flow Project. (2026). `registries/PROJECT_IMPROVEMENT_SIGNAL_REGISTRY.csv` [Concrete signal instances, severity, status, evidence, and resolution fields.]

## Safe Operating Summary

Safe summary: Project-system improvement classifies current diffs, inspects registered signals, routes one bounded AgentJob, records documentation impact, and closes signals only with explicit evidence.

Unsafe summary: Project-system improvement is physics continuation, resolver output alone blocks checkpointing, or a signal can close without PASS completion or rejection evidence.
