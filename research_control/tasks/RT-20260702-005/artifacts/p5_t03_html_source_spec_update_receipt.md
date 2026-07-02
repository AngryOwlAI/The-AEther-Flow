<!-- authority: control -->

# P5-T03 HTML Explainer Source-Spec Update Receipt

## Scope

This receipt records one bounded v14 P5-T03 documentation-control packet. It
updates affected Markdown source specs for generated HTML explainers so later
generated public derivatives can render current status-layer wording from
tracked source authority. It also synchronizes only the affected generated
HTML `aether-flow-source-basis-hash` metadata to the updated source-spec
hashes so bootstrap validation can preserve the source-to-derivative binding.
It does not regenerate generated HTML content, GitHub-facing Markdown, README,
publication briefs, source registries as scientific authority, or physics
claim status.

## Updated Source Specs

| Source spec | Result |
| --- | --- |
| `markdown/html-explainer-specs/project-overview-explainer.md` | Added `research_control/design/public_status_table_source_spec.md` as source material and required public status boundary preservation. |
| `markdown/html-explainer-specs/aether-flow-physics-program-explainer.md` | Added public status table source basis and explicit high-risk public status boundary criteria. |
| `markdown/html-explainer-specs/exact-gr-benchmark-boundary-explainer.md` | Added public status table source basis and blocked benchmark-promotion status criteria. |
| `markdown/html-explainer-specs/gr-derivation-roadmap-explainer.md` | Corrected stale `M_src` and `g_eff` status wording and added public status table source basis. |
| `markdown/html-explainer-specs/claim-gates-explainer.md` | Added public status table source basis and public-status gate examples. |
| `markdown/html-explainer-specs/source-authority-explainer.md` | Added public status table source-spec authority routing to the source-authority model. |
| `markdown/html-explainer-specs/validator-operator-workflow-explainer.md` | Added public status table source-spec checks as validator PASS limit examples. |

## Generated HTML Metadata Synchronization

| Generated derivative | Result |
| --- | --- |
| `html/project-overview-explainer.html` | Updated `aether-flow-source-basis-hash` to the current source-spec hash only. |
| `html/aether-flow-physics-program-explainer.html` | Updated `aether-flow-source-basis-hash` to the current source-spec hash only. |
| `html/exact-gr-benchmark-boundary-explainer.html` | Updated `aether-flow-source-basis-hash` to the current source-spec hash only. |
| `html/gr-derivation-roadmap-explainer.html` | Updated `aether-flow-source-basis-hash` to the current source-spec hash only. |
| `html/claim-gates-explainer.html` | Updated `aether-flow-source-basis-hash` to the current source-spec hash only. |
| `html/source-authority-explainer.html` | Updated `aether-flow-source-basis-hash` to the current source-spec hash only. |
| `html/validator-operator-workflow-explainer.html` | Updated `aether-flow-source-basis-hash` to the current source-spec hash only. |

## Acceptance Criteria

| Criterion | Result | Evidence |
| --- | --- | --- |
| HTML source specs cite or link the public status table source spec where current public status may be rendered. | PASS | All seven candidate specs include `research_control/design/public_status_table_source_spec.md` in source materials or source basis. |
| HTML source specs preserve that GR is not derived. | PASS | Physics-program and roadmap specs require no completed derivation and no GR derivation overread. |
| HTML source specs do not underclaim source-only `M_src`. | PASS | Roadmap source basis and criteria describe `M_src` as scoped source-only. |
| HTML source specs do not underclaim scoped `g_eff`. | PASS | Roadmap and public-status criteria describe `g_eff` as scoped source-extension object status. |
| HTML source specs do not imply matter coupling is solved. | PASS | Specs state matter coupling remains scoped evidence/precondition only or not derived/adopted. |
| HTML source specs do not imply `RR_ETransportCompletenessOrInvarianceLaw_v1` is adopted as a source law. | PASS | Physics-program criteria name it as scoped evidence/precondition only. |
| HTML source specs do not imply no-target certificates provide positive matter theory. | PASS | Physics-program criteria state no-target certificates are not positive matter theory. |

## Validation Receipts

| Check | Result | Evidence |
| --- | --- | --- |
| Memory preflight | PASS | `core_validation_status=PASS`, `freshness_status=PASS`, `local_retrieval_status=PASS`, `refresh_performed=false` |
| Targeted memory query | PASS | Lookup of `MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V14` returned the canonical v14 plan and related public status source spec. |
| Continue-research route | PASS | Resolver selected `v14_p5_t03_html_explainer_source_spec_update` from `handoff-0457`. |
| Changed source-spec claim-language gate | PASS | `validate_claim_language.py --json --changed` reported `hard_fail_count=0`, `warning_count=0`, and `scanned_path_count=7` after source-spec edits. |

## Interpretation Boundary

P5-T03 is a source-spec documentation packet. It does not establish or change
the physics status of any row. It does not authorize ontology edits,
source-law adoption, `MetricData(E)` adoption, `g_eff` scope expansion,
matter-coupling derivation, stress-energy semantics, matter action, Einstein
equations, benchmark promotion, or completed derivation.

## Next Route

The logical next packet is v14 P5-T04 public status regeneration. Public
status claim-language validation and downstream physics routes remain blocked
until their own tracked packets authorize them.
