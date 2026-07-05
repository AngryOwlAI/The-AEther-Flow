<!-- authority: control -->

# Negative Result Reader-Language Audit v16

## Status

- Task: `RT-20260705-022`
- Plan task: `P11-T01`
- Role: `documentation-curator@2.0.0`
- Verdict: `pass_no_update_required`
- Risky wording routes to P11-T02: false
- Next route: P11-T03 negative-result integration selector
- Physics delta: none

## Audit Scope

This audit checks reader-facing and control surfaces named by P11-T01 for two
failure modes:

1. Overclaim: wording turns scoped negative results into program-wide no-go,
   future source-extension impossibility, benchmark failure or closure, matter
   coupling, Einstein equations, or completed derivation.
2. Underexposure: wording hides frozen local routes, scoped obstructions, what
   remains open, or exact source-artifact links.

The audit classifies wording only. It does not update publication surfaces,
promote physics claims, issue a Gate Chair verdict, promote benchmark status,
or change the Distance-to-GR ledger.

## Surfaces Audited

| Surface | Source role | Result | Evidence |
| --- | --- | --- | --- |
| `research_control/design/negative_result_inventory_v15.md` | negative-result inventory | pass | Five scoped entries plus the route-orbit no-freeze note identify source paths, blocked reuse, allowed reuse, and what remains open. |
| `markdown/publication-briefs/negative-results-and-obstructions.publication-brief.md` | publication brief | pass | Defines reader job, forbidden patterns, acceptance criteria, and explicit limits against program-wide rejection and future source-extension impossibility. |
| `markdown/html-explainer-specs/negative-results-and-obstructions-explainer.md` | source spec | pass | Requires source matrix, source-material visibility, exact reader-scope footer, and public-safe boundaries. |
| `github-facing/negative-results-and-obstructions-explainer.md` | generated GitHub reader surface | pass | States negative results do not reject the program, do not prove future source-extension impossibility, do not promote benchmark status, and do not complete derivation. |
| `research_control/current_frontier.md` | current status report | pass | Lists the negative local toy route as frozen negative only and blocks global-theory rejection and future source-extension impossibility. |
| `README.md` | public front door | pass | Exposes negative-result preservation as a project discipline while stating that GR has not been derived and that obstruction claims require reproducible evidence. |
| `research_control/README.md` | research-control documentation | pass | Separates scoped obstruction from impossibility and preserves `blocked_adoption_open_continuation` language. |
| `research_control/design/claim_language_linter_taxonomy.yaml` | linter policy | pass_with_intentional_examples | Taxonomy intentionally contains bad examples; linter classifies those as intentional warnings, not current/public hard failures. |

## Audit Questions

| Question | Answer |
| --- | --- |
| Are frozen local routes visible? | Yes. The finite toy metric-response route appears in the inventory, source spec, GitHub-facing explainer, and current frontier. |
| Are scoped obstructions visible? | Yes. `Resp_lc`, `RR_E`, and certificate-gap scoped obstructions are visible in the inventory and reader surfaces. |
| Does any wording imply global program rejection? | No. The audited public surfaces explicitly deny program-wide rejection. |
| Does any wording imply future source-extension impossibility? | No. The audited public surfaces explicitly deny future source-extension impossibility and name open continuation classes. |
| Does any wording imply benchmark failure or benchmark closure? | No. The audited surfaces block benchmark promotion, benchmark closure, and benchmark-derived negative overreads. |
| Does any negative result hide what remains open? | No blocking underexposure found. Each main reader surface names open redesigned routes, certificate construction, source-extension candidates, or same-milestone continuation. |
| Are negative results tied to exact source artifacts? | Yes. The inventory and GitHub-facing explainer expose source paths; the source spec requires exact source paths in generated surfaces. |

## Linter Receipt

Command:

```text
.venv/bin/python scripts/project_control/validate_claim_language.py --json --paths research_control/design/negative_result_inventory_v15.md markdown/publication-briefs/negative-results-and-obstructions.publication-brief.md markdown/html-explainer-specs/negative-results-and-obstructions-explainer.md github-facing/negative-results-and-obstructions-explainer.md research_control/current_frontier.md README.md research_control/README.md research_control/design/claim_language_linter_taxonomy.yaml
```

Result:

- status: `PASS`
- hard_fail_count: `0`
- warning_count: `133`
- warning interpretation: intentional taxonomy examples only; no P11 reader
  surface requires a wording repair.

## P11-T02 Routing Decision

P11-T02 is not required for the audited state. The required trigger for P11-T02
is risky wording found by P11-T01. This audit found no current/public
hard-fail wording and no blocking underexposure. The logical next route is
P11-T03, the negative-result integration selector.

## Claim Boundary

Allowed:

- classify negative-result reader-facing language;
- identify whether P11-T02 is required;
- route the next v16 step.

Forbidden:

- program-wide no-go or rejection claim;
- future source-extension impossibility;
- benchmark failure, closure, or promotion;
- matter semantics, detector semantics, coupling-law, matter-coupling,
  stress-energy, matter-action, or Einstein-equation claim;
- Gate Chair verdict;
- completed-derivation claim;
- treating generated reader surfaces, validators, wiki notes, or this audit as
  physics proof authority.

## References

The AEther-Flow Research Project. (2026a). *Negative result inventory v15*
[Control inventory]. `research_control/design/negative_result_inventory_v15.md`.

The AEther-Flow Research Project. (2026b). *Negative results and obstructions
publication brief* [Publication brief].
`markdown/publication-briefs/negative-results-and-obstructions.publication-brief.md`.

The AEther-Flow Research Project. (2026c). *Negative results and obstructions
source spec* [HTML explainer source spec].
`markdown/html-explainer-specs/negative-results-and-obstructions-explainer.md`.

The AEther-Flow Research Project. (2026d). *Current frontier* [Control report].
`research_control/current_frontier.md`.

