<!-- authority: control -->

# Handoff 0952 — Gate A exact-object registry-validator parity

Status: `ready_after_checkpoint`.

`handoff-0952` records the bounded generation-240 project-system repair.

## Result

The exact Gate A decision object now has operational registry-validation parity:

- object ID `TEX-V21-P4-T05-ONTOLOGY-REGIME-GATE-CHAIR-DECISION-V1`;
- canonical path `research_control/tasks/RT-20260724-004/artifacts/ontology_regime_gate_chair_decision_v1.tex`;
- exact source SHA-256 `20ea795bbe93333b489e4f13601fd6bb1623f318b7847f9d2d24402c7490c934`;
- operational registry validation status `PASS`.

The new task-local validator binds all four values. Six regressions prove that
missing, duplicate, wrong-path, wrong-hash, and cross-object PASS rows fail
closed. The sealed RT-20260803-005 validator and report hashes remain exact.
`PIS-RT-20260803-010-001` is resolved by this matching completion.

## Next action

Invoke the single governed checkpoint for `AJ-RT-20260803-011-001`. After that
checkpoint, route one fresh `continue-research` P16-T02 canonical Gate A-E
consistency re-audit. Do not execute P16-T03 or P16-T04 first.

## Authority boundary

Operational registry-validation PASS is not a new Gate A scientific verdict.
This repair does not modify the protected Gate A source, adopt ontology or a
source law, derive a metric, matter coupling, or Einstein equations, promote a
benchmark, establish proof, complete external review, authorize publication or
push, or complete the GR derivation.
