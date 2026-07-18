---
authority: control
task_id: "RT-20260718-008"
job_id: "AJ-RT-20260718-008-001"
plan_task_id: "P11-T04"
decision: "BLOCKED_EXTERNAL_PUBLICATION_AUTHORITY"
cutover_authorized: false
scientific_claims_changed: false
---

# P11-T04 hosted-CI authority decision

## Decision

Planner cutover is not authorized. The repaired checkpoint
`52af94b88c8fbe799af45dd0d97f2f5ae801a823` exists only on the local
`codex/v19-remaining-relay` branch. That branch has no upstream, no matching
branch on `origin`, and no GitHub Actions run for the exact checkpoint.

The canonical migration policy requires scheduled-full and CI evidence when
those surfaces are cut over. The live manifest therefore remains
`shadow_planner` with `legacy` execution authority and the explicit legacy
fallback retained.

## Authority boundary

This relay frame does not authorize a push, hosted workflow dispatch, branch
protection mutation, or live default mutation. It also has no scientific,
proof, benchmark, ontology, or Gate Chair authority. The absence of hosted-CI
evidence cannot be repaired locally without crossing that publication
boundary.

## Required next authority

A future frame may proceed only after the user explicitly authorizes
publication of the exact branch checkpoint. It must then observe matched
hosted CI and scheduled-full evidence before reconsidering cutover. P11-T04
remains incomplete and P11-T05 remains blocked.
