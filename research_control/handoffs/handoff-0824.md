# Handoff 0824 — P12-T03 dual-budget policy complete

Handoff ID: `handoff-0824`.

P12-T03 is complete as a project-control-only packet. It adds four explicit
categories—physics-bearing, system-bearing, mixed, and support-only—with
exactly one primary task-count credit. Physics and project-system elapsed
effort, compute, durable outputs, and acceptance criteria remain separate.
Mixed work cannot reuse one output or criterion in both lanes, and unmeasured
compute remains unmeasured rather than becoming zero.

The task-local fixture matrix passes 12 of 12 cases. The dashboard is
support-only. System, validator, route-selection, and dashboard success do not
count as physics evidence or a Distance-to-GR change.

The existing three-system-task threshold remains advisory in P12-T03. P12-T04
is now dependency-ready and owns the ordinary-route hard guard, including
hash-bound exceptions when a control failure genuinely blocks science work.
P12-T05 is also dependency-ready but is not selected ahead of P12-T04 in plan
order.

Next action: run exactly one bounded P12-T04
`project-control-maintainer@0.2.0` project-system AgentJob after the governed
P12-T03 checkpoint succeeds. This handoff does not authorize P12-T04
execution inside P12-T03, scientific-source or ledger changes, ontology
adoption, physics promotion, proof, publication, or a completed derivation.
