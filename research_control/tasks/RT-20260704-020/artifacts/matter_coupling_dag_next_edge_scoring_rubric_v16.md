<!-- authority: control -->

# Matter-Coupling DAG Next-Edge Scoring Rubric v16

Scores are route-selection evidence only. They are not proof authority and do
not promote any physics claim.

## Dimensions

Higher is better for burden discharge, available inputs, certificate-instance
feasibility, Refuter testability, formalization feasibility, and
Distance-to-GR specificity. Lower is better for target-import risk, dependency
on missing `EqSrc`/`RetainH`/`GenH`, route-orbit risk, and public-overread risk.

## Scoring Matrix

| Candidate edge | Burden | Inputs | Certs | Import risk | Upstream dependency | Refuter | Formalization | Orbit risk | Overread risk | Specificity | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `mc_source_matter_semantics_equivalence_theorem -> mc_coupling_law_target` | 5 | 5 | 4 | 2 | 2 | 5 | 4 | 2 | 3 | 5 | selected |
| `mc_detector_semantics_target -> mc_universal_matter_coupling_derivation` | 5 | 1 | 1 | 5 | 4 | 3 | 2 | 4 | 5 | 4 | not selected |
| `mc_coupling_law_target -> mc_universal_matter_coupling_derivation` | 5 | 1 | 2 | 4 | 3 | 4 | 3 | 3 | 5 | 5 | not selected |
| `mc_stress_energy_semantics_target -> mc_stress_energy_tensor_target` | 4 | 1 | 1 | 5 | 4 | 3 | 2 | 4 | 5 | 4 | not selected |
| `mc_stress_energy_tensor_target -> mc_matter_action_target` | 4 | 1 | 1 | 5 | 4 | 3 | 2 | 4 | 5 | 4 | not selected |
| `mc_matter_action_target -> mc_einstein_equation_dependency` | 4 | 1 | 1 | 5 | 5 | 3 | 2 | 4 | 5 | 5 | not selected |
| `mc_universal_matter_coupling_derivation -> mc_einstein_equation_dependency` | 4 | 1 | 1 | 5 | 5 | 3 | 2 | 4 | 5 | 5 | not selected |
| `mc_certificate_gap_obstruction -> mc_source_matter_semantics_equivalence_theorem` | 3 | 5 | 4 | 1 | 1 | 5 | 5 | 2 | 2 | 3 | not selected |
| `mc_rr_e_certificate_boundary -> mc_source_matter_semantics_equivalence_theorem` | 3 | 5 | 4 | 2 | 2 | 4 | 5 | 2 | 3 | 3 | not selected |

## Selection Rule

Select the highest-value edge that can create new mathematical payload without
requiring protected adoption authority. Under live evidence, that is:

`mc_source_matter_semantics_equivalence_theorem -> mc_coupling_law_target`.
