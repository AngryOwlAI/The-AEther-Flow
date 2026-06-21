<!-- authority: control -->

# Mathematical Decisiveness Branch Validation Cleanup

## Analysis

The branch contains two different work families relative to `origin/main`:

1. Project-system implementation work for the mathematical-decisiveness
   completion contract, schema/template support, validator enforcement,
   obstruction/freeze control, Candidate Constructor no-fog rules, and generated
   memory/wiki derivatives.
2. A physics Candidate Constructor task, `RT-20260614-084`, applying the
   upgraded contract to the general source-cover candidate construction.

`validate_research_control.py --check-diff --base-ref origin/main` selects the
latest active or completed AgentJob by `created_at` and compares the whole
requested Git diff against that single job's allowed paths. Before this cleanup,
the latest row was `AJ-RT-20260614-084-001`. That job correctly allows the
Phase 6 Candidate Constructor paths, but it does not allow the earlier
project-system Phase 1-5 paths. Therefore the whole-branch check failed for a
boundary-selection reason.

## Branch-Level Rationale

This cleanup records a closure-level project-control boundary for the already
batched branch. It does not rewrite prior completions and does not retroactively
change the scientific meaning of any artifact.

The correct interpretation is:

- Per-AgentJob validation remains the normal research-control discipline.
- A whole-branch diff against `origin/main` spans multiple completed AgentJobs.
- The whole-branch check must be evaluated against a branch-closure
  project-control packet, not against only the latest physics job.
- `.local/` retrieval outputs remain non-authoritative retrieval layers and are
  not independent validation authority.

## Phase Scope Decision

The completed branch implements the decisive core through Phase 6:

- Phase 1 contract surface.
- Phase 2 schema/template support.
- Phase 3 validator enforcement.
- Phase 4 obstruction and freeze-control machinery.
- Phase 5 Candidate Constructor no-fog rules.
- Phase 6 application to `RT-20260614-084`.

Phase 8 and Phase 9 are not implemented by this cleanup:

- Phase 8 backfill is deferred. It should create metadata overlays only, avoid
  rewriting prior scientific artifacts, and be routed as a separate bounded
  project-system AgentJob.
- Phase 9 metrics are deferred. A future metrics script or report should be
  based on tracked completions and registries and must not promote physics
  claims.

## Conclusion

The logical cleanup is a branch-level project-control closure record. It makes
the validation boundary explicit and prevents the completed Phase 1-6 work from
being described as complete against the optional Phase 8 and Phase 9 plan items.

## References

The AEther-Flow Research Project. (2026, June 21). *AEther recommendations
implementation plan* [Local implementation plan].

The AEther-Flow Research Project. (2026, June 21). *Mathematical decisiveness
completion contract* [Project-control design note].

The AEther-Flow Research Project. (2026, June 21). *Research-control validator*
[Source code].
