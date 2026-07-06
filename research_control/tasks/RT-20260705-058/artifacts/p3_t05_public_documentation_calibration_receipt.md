<!-- authority: control -->

# P3-T05 Public Documentation Calibration Receipt

## Summary

`RT-20260705-058` completed one bounded v17 P3-T05 public-facing
documentation calibration pass.

The packet replaced caveat-first wording with positive-first exact-scope
wording for high-risk accepted or scoped-positive rows:

- positive status;
- exact scope;
- allowed use;
- blocked overread.

## Updated Public Surfaces

```text
README.md
github-facing/project-overview-explainer.md
github-facing/aether-flow-physics-program-explainer.md
github-facing/exact-gr-benchmark-boundary-explainer.md
github-facing/gr-derivation-roadmap-explainer.md
github-facing/claim-gates-explainer.md
```

## Updated Source Contracts

```text
markdown/html-explainer-specs/project-overview-explainer.md
markdown/html-explainer-specs/aether-flow-physics-program-explainer.md
markdown/html-explainer-specs/exact-gr-benchmark-boundary-explainer.md
markdown/html-explainer-specs/gr-derivation-roadmap-explainer.md
markdown/html-explainer-specs/claim-gates-explainer.md
markdown/publication-briefs/project-overview.publication-brief.md
markdown/publication-briefs/aether-flow-physics-program.publication-brief.md
markdown/publication-briefs/exact-gr-benchmark-boundary.publication-brief.md
markdown/publication-briefs/gr-derivation-roadmap.publication-brief.md
markdown/publication-briefs/claim-gates.publication-brief.md
```

## Unchanged Public Candidate Surface

`github-facing/negative-results-and-obstructions-explainer.md` was scanned and
left unchanged. It already states negative-result boundaries without the P3-T05
underclaim warning pattern.

## Synchronized HTML Derivatives

The five affected tracked HTML explainers were synchronized only after the
registered source-spec and publication-brief updates:

```text
html/project-overview-explainer.html
html/aether-flow-physics-program-explainer.html
html/exact-gr-benchmark-boundary-explainer.html
html/gr-derivation-roadmap-explainer.html
html/claim-gates-explainer.html
```

Direct HTML-only editing remained blocked. The task-local validator checks each
changed HTML file against its source-basis hash and calibrated marker.

## Validation Receipt

Task-local validation report:

```text
research_control/tasks/RT-20260705-058/artifacts/p3_t05_public_documentation_calibration_report.json
```

Focused P3-T05 candidate claim-language scan:

```yaml
status: "PASS"
hard_fail_count: 0
overclaim_hard_fail_count: 0
warning_count: 0
underclaim_calibration_warning_count: 0
scanned_path_count: 45
```

## Claim Boundary

This is a documentation calibration packet. It does not change the
Distance-to-GR ledger, adopt a source law, adopt detector semantics, adopt a
coupling law, derive or adopt matter coupling, import stress-energy semantics,
construct a matter action, derive Einstein equations, promote a benchmark,
issue a Gate Chair verdict, or claim a completed derivation.

## Next Route

Run one bounded v17 P3-T06 acceptance calibration red-team review.
