---
authority: control
handoff_id: handoff-0988
status: ready_for_v22_p4_t02_after_checkpoint
task_id: RT-20260809-018
job_id: AJ-RT-20260809-018-001
plan_id: recommendations_implementation_plan_continue_task-v22
plan_task_id: P4-T02
completed_plan_task_id: P4-T01
created_at: 2026-08-09T19:17:33Z
---

# Handoff 0988 — V22 P4-T01 reduced source principal symbol

P4-T01 is complete at draft/control level. The fixed P3-T02/P3-T04 system has
zero supplied algebraic constraints, differential constraints, internal field
gauge, and equation redundancy, so its lawful reduced source symbol is
`diag(k(X_1),...,k(X_6))`. Its determinant is the nontrivial square-free
degree-six polynomial
`(w+x)(w+y)(w+z)(w+x+y)(w+y+2z)(w+2x+z)`.

All six global factors have multiplicity one and source-coordinate density
weight zero. Passive source-chart covariance is exact; arbitrary field and
equation frames change the scalar representative by `det(S)/det(R)` while
preserving its zero set. Every branch is retained. All pairs cross, all
triples meet, and branches `2,3,4,6` share the unique nonzero fourfold
intersection represented by `k=(1,0,-1,-1)`, where symbol corank is four. No
nonzero fivefold intersection exists. A separate rational Leibniz
implementation reproduces five determinant cases and the fourfold rank.

All 106 focused checks pass. The TeX source compiles to six pages with zero
overfull warnings and one nonblocking, legible table underfull warning; every
page was rendered and visually inspected. The transaction now requires its
single governed checkpoint. After that commit, P4-T02 may be separately
claimed through `continue-research` for the hyperbolicity, universality,
robustness, common-cone, and hard-fail screen.

This result is proposal-only source-principal data. It is not a physical
causal cone, Lorentzian signature, clock, scale, effective metric, matter
coupling, Einstein equation, Gate verdict, external review, benchmark
promotion, publication authority, push authority, or completed derivation.
