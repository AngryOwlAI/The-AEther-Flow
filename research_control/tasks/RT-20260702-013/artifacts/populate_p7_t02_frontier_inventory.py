from pathlib import Path
import re


INVENTORY_PATH = Path("research_control/design/frontier_theorem_inventory.md")


DOWNSTREAM_BLOCKS = (
    "source-law adoption; MetricData(E) adoption; g_eff scope expansion; "
    "coupling-law adoption; matter-semantics adoption; detector-semantics "
    "adoption; matter-coupling derivation or adoption; stress-energy "
    "semantics; stress-energy tensor; matter action; Einstein equations; "
    "benchmark promotion; completed derivation"
)


BASE_FIELD_VALUES = {
    "source_ontology_primitives": {
        "milestone": "`source_ontology`",
        "object_type": "`definition;missing_theorem`",
        "authority_level": "`registered_control_markdown;registry_row;draft_control`",
        "definitions_introduced": "`none`; this row summarizes draft/control ontology-boundary material.",
        "theorem_like_claims": "`none`; this is a missing-theorem and draft-control boundary row.",
        "audits_passed": "`none`.",
        "stress_results": "`none`.",
        "gate_chair_results": "`none`; canonical ontology adoption remains protected and absent.",
        "fail_closed_branches": "`none`.",
        "known_obstructions": "Canonical ontology adoption rule and derivation-critical primitives remain missing.",
        "forbidden_overread": "Draft ontology language as canonical ontology, benchmark recovery, or completed derivation.",
        "downstream_blocked_targets": "Source-law adoption, downstream GR recovery, benchmark promotion, and completed derivation.",
        "next_theorem_needed": "Canonical ontology adoption rule or derivation-critical source primitive under protected authority.",
        "three_tier_classification": "`open_or_blocked_physical_target`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "source_equivalence_eqsrc": {
        "milestone": "`source_equivalence_eqsrc`",
        "object_type": "`missing_theorem`",
        "authority_level": "`registry_row;registered_control_markdown;draft_control`",
        "definitions_introduced": "`none`; the row summarizes an open equivalence burden.",
        "theorem_like_claims": "Missing general source-equivalence theorem under the declared variation regime.",
        "audits_passed": "`none`.",
        "stress_results": "`none`.",
        "gate_chair_results": "`none`.",
        "fail_closed_branches": "`none`.",
        "known_obstructions": "General `EqSrc` theorem remains undischarged; local witnesses do not supply it.",
        "forbidden_overread": "Local or finite witness status as the general `EqSrc` theorem.",
        "downstream_blocked_targets": "RetainH, GenH, robust source-manifold obligations, downstream GR recovery.",
        "next_theorem_needed": "General source-equivalence theorem under the declared variation regime.",
        "three_tier_classification": "`open_or_blocked_physical_target`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "retain_h": {
        "milestone": "`retain_h`",
        "object_type": "`missing_theorem;obstruction`",
        "authority_level": "`registry_row;registered_control_markdown`",
        "definitions_introduced": "`none`; the row summarizes a missing retention primitive.",
        "theorem_like_claims": "RetainH is blocked by a missing canonical primitive or theorem.",
        "audits_passed": "`none`.",
        "stress_results": "`none`.",
        "gate_chair_results": "`none`.",
        "fail_closed_branches": "`none`.",
        "known_obstructions": "Missing retention primitive.",
        "forbidden_overread": "Route progress or local witness survival as RetainH adoption.",
        "downstream_blocked_targets": "Retention-law adoption, source-law closure, downstream GR recovery.",
        "next_theorem_needed": "Canonical retention primitive or theorem.",
        "three_tier_classification": "`open_or_blocked_physical_target`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "gen_h": {
        "milestone": "`gen_h`",
        "object_type": "`missing_theorem;obstruction`",
        "authority_level": "`registry_row;registered_control_markdown`",
        "definitions_introduced": "`none`; the row summarizes a missing generator primitive.",
        "theorem_like_claims": "GenH is blocked by a missing canonical primitive or theorem.",
        "audits_passed": "`none`.",
        "stress_results": "`none`.",
        "gate_chair_results": "`none`.",
        "fail_closed_branches": "`none`.",
        "known_obstructions": "Missing generator primitive.",
        "forbidden_overread": "Finite examples, source-extension data, or validation status as GenH adoption.",
        "downstream_blocked_targets": "Generator-law adoption, source-law closure, downstream GR recovery.",
        "next_theorem_needed": "Canonical generator primitive or theorem.",
        "three_tier_classification": "`open_or_blocked_physical_target`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "obsloc_lc": {
        "milestone": "`source_localization_obsloc_lc`",
        "object_type": "`witness`",
        "authority_level": "`canonical_tex;registry_row;draft_control`",
        "definitions_introduced": "Local exact-branch witness terms recorded by the cited artifact.",
        "theorem_like_claims": "Constructive source-local exact-branch witness under the finite exact-branch scope.",
        "audits_passed": "Hidden-import audit survived for the exact finite local branch.",
        "stress_results": "`none` beyond the cited source-purity audit boundary.",
        "gate_chair_results": "`none`.",
        "fail_closed_branches": "Non-exact, quotient-transport, and bridge overreads remain blocked.",
        "known_obstructions": "Robust non-exact localization and quotient transport remain missing.",
        "forbidden_overread": "Exact-branch witness as robust global localization, target geometry, metric, matter, or bridge evidence.",
        "downstream_blocked_targets": "Robust localization, quotient transport, matter coupling, Einstein equations, benchmark promotion.",
        "next_theorem_needed": "Robust non-exact localization or quotient-transport theorem.",
        "three_tier_classification": "`accepted_evidence_precondition`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "resp_lc": {
        "milestone": "`response_localization_resp_lc`",
        "object_type": "`source_extension_evidence;gate_decision;accepted_scoped_object`",
        "authority_level": "`gate_chair_artifact;registry_row`",
        "definitions_introduced": "`Resp_lc`; `Xi_X^R`; response selector source-extension data under the cited scope.",
        "theorem_like_claims": "Scoped Gate Chair acceptance of response selector data as source-extension input only.",
        "audits_passed": "Prior smuggling/audit chain summarized by the Gate Chair artifact.",
        "stress_results": "Old `S_X`-only route remains obstructed under the forgetful reduct.",
        "gate_chair_results": "Accepted only as admissible source-extension data for `Resp_lc` continuation.",
        "fail_closed_branches": "Old tuple route without `Xi_X^R` remains blocked.",
        "known_obstructions": "Derivation of selector data from the old tuple remains absent.",
        "forbidden_overread": "Response-token semantics as detector semantics, matter coupling, or canonical ontology edit.",
        "downstream_blocked_targets": "Detector semantics, matter coupling, Einstein equations, benchmark promotion, completed derivation.",
        "next_theorem_needed": "Derivation of selector data from old source tuple or separately gated detector/matter semantics.",
        "three_tier_classification": "`accepted_evidence_precondition`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "m_src_gsc": {
        "milestone": "`source_manifold_m_src`",
        "object_type": "`gate_decision;accepted_scoped_object`",
        "authority_level": "`gate_chair_artifact;registry_row`",
        "definitions_introduced": "`M_src^{GSC-cand}` and scoped source-only object boundary under H1-H13.",
        "theorem_like_claims": "Scoped source-only `M_src` adoption under the declared assumptions and non-conclusion guards.",
        "audits_passed": "Integrated source-only adoption chain passed its cited review boundary.",
        "stress_results": "Fail-closed obstruction behavior retained for unsupported branches.",
        "gate_chair_results": "Gate Chair adopted only the scoped source-only `M_src` object.",
        "fail_closed_branches": "Conditional `RegSold` and `FVR` clauses remain conditional outside the scoped boundary.",
        "known_obstructions": "Target geometry, metric law, matter-coupling route, and Einstein-equation dynamics remain missing.",
        "forbidden_overread": "Scoped source-only `M_src` as target manifold, metric, matter coupling, or GR derivation.",
        "downstream_blocked_targets": "MetricData(E), unscoped g_eff, matter coupling, Einstein equations, benchmark promotion.",
        "next_theorem_needed": "Effective metric law, matter-coupling bridge, and field-equation dynamics.",
        "three_tier_classification": "`adopted_object`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "g_eff_gsc_cand": {
        "milestone": "`effective_metric_g_eff`",
        "object_type": "`gate_decision;accepted_scoped_object;source_extension_evidence`",
        "authority_level": "`gate_chair_artifact;registry_row`",
        "definitions_introduced": "`g_eff^{GSC-cand}` scoped source-extension object under beta-separated finite-graph scope.",
        "theorem_like_claims": "Scoped source-extension `g_eff` object adoption under declared source-side scope only.",
        "audits_passed": "Candidate audit chain summarized by the Gate Chair artifact.",
        "stress_results": "Fail-closed bottom behavior retained for unsupported branches.",
        "gate_chair_results": "Gate Chair adopted the accepted candidate only as a scoped source-extension `g_eff` object.",
        "fail_closed_branches": "MetricData(E), MetricFormAssign, SigScaleCont, and unscoped Lorentzian readings remain blocked.",
        "known_obstructions": "Unscoped metric theorem and metric-data source-law adoption remain missing.",
        "forbidden_overread": "Scoped source-extension `g_eff` as unscoped Lorentzian metric, matter-sector input, field-equation premise, or benchmark recovery.",
        "downstream_blocked_targets": "MetricData(E), unscoped g_eff, matter coupling, Einstein equations, benchmark promotion.",
        "next_theorem_needed": "Unscoped metric theorem, metric-data law, matter-coupling bridge, and field-equation dynamics.",
        "three_tier_classification": "`adopted_object`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "matter_coupling_bridge_target_v1": {
        "milestone": "`matter_coupling`",
        "object_type": "`definition;theorem_target;missing_theorem`",
        "authority_level": "`canonical_tex;draft_control`",
        "definitions_introduced": "`MatterCouplingBridgeTarget_v1`; `PTMI_E`; source-domain package obligations.",
        "theorem_like_claims": "Proposal-only bridge target and eligibility conditions for future candidates.",
        "audits_passed": "`none` for adoption; target formalization only.",
        "stress_results": "`none` for adoption; target formalization only.",
        "gate_chair_results": "`none`.",
        "fail_closed_branches": "Target satisfaction does not imply matter-coupling adoption.",
        "known_obstructions": "Actual bridge candidate, tensorial semantics, coupling law, matter action, and detector semantics remain missing.",
        "forbidden_overread": "Bridge target as matter coupling, stress-energy, matter action, or coupling-law adoption.",
        "downstream_blocked_targets": DOWNSTREAM_BLOCKS,
        "next_theorem_needed": "Actual source-local bridge candidate and a law connecting it to matter semantics without target import.",
        "three_tier_classification": "`open_or_blocked_physical_target`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "matter_coupling_precondition_evidence": {
        "milestone": "`matter_coupling`",
        "object_type": "`source_extension_evidence;witness;gate_decision`",
        "authority_level": "`gate_chair_artifact;canonical_tex;registry_row`",
        "definitions_introduced": "`ParamFiniteLocalWitness_v1`; `BridgeSlot_n`; `NoTargetImport_n`; later scoped profile and RR_E transport evidence labels.",
        "theorem_like_claims": "Scoped evidence/precondition status for finite/local witness and later RR_E/profile evidence only.",
        "audits_passed": "Finite/local source-family and no-target-import checks summarized by the cited sources.",
        "stress_results": "Support-only mechanization and finite/local checks remain non-authoritative proof aids.",
        "gate_chair_results": "Accepted only as scoped evidence/precondition; no adoption of source law or matter coupling.",
        "fail_closed_branches": "Checker proof authority, target import, and evidence-as-adoption branches remain blocked.",
        "known_obstructions": "Source-law adoption, coupling law, matter semantics, detector semantics, stress-energy, matter action, and Einstein equations remain missing.",
        "forbidden_overread": "Finite/local evidence or profile labels as matter coupling, stress-energy, detector semantics, source-law adoption, or downstream GR proof.",
        "downstream_blocked_targets": DOWNSTREAM_BLOCKS,
        "next_theorem_needed": "Source-law or coupling-law theorem sufficient for matter semantics and matter coupling under no-target-import constraints.",
        "three_tier_classification": "`accepted_evidence_precondition`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "rr_e_theorem_target_v1": {
        "milestone": "`matter_coupling`",
        "object_type": "`theorem_target;missing_theorem`",
        "authority_level": "`canonical_tex;draft_control`",
        "definitions_introduced": "`RR_E` theorem target for detector-irrelevance relation.",
        "theorem_like_claims": "Proposal-only RR_E theorem target; no theorem proof.",
        "audits_passed": "`none` for proof; target formalization only.",
        "stress_results": "`none` for proof; later stress is recorded separately.",
        "gate_chair_results": "`none`.",
        "fail_closed_branches": "Target naming cannot be reused as theorem proof.",
        "known_obstructions": "A sufficient source-side law or invariant remains missing.",
        "forbidden_overread": "RR_E target formalization as unrestricted theorem, detector semantics, or matter coupling.",
        "downstream_blocked_targets": "Unrestricted RR_E theorem, detector semantics, matter coupling, Einstein equations, benchmark promotion.",
        "next_theorem_needed": "Source-side law or theorem sufficient to prove the target.",
        "three_tier_classification": "`open_or_blocked_physical_target`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "rr_e_underdetermination_obstruction": {
        "milestone": "`matter_coupling`",
        "object_type": "`obstruction;missing_theorem`",
        "authority_level": "`canonical_tex;refuter_artifact`",
        "definitions_introduced": "`none`; this row records the current-ontology obstruction to a named missing law.",
        "theorem_like_claims": "Current ontology does not derive the derivation-critical RR_E transport-completeness or invariance law.",
        "audits_passed": "Obstruction attempt and refuter-stress artifacts preserve the scoped boundary.",
        "stress_results": "Refuter stress preserved the scoped RR_E obstruction and separation.",
        "gate_chair_results": "`none` for law adoption.",
        "fail_closed_branches": "Same-milestone continuation remains open through conservative source-side extension.",
        "known_obstructions": "`RR_ETransportCompletenessOrInvarianceLaw_v1` missing under current ontology.",
        "forbidden_overread": "Current-ontology underdetermination as future source-extension impossibility or program-wide no-go conclusion.",
        "downstream_blocked_targets": "Unrestricted RR_E theorem, matter coupling, detector semantics, benchmark promotion.",
        "next_theorem_needed": "`RR_ETransportCompletenessOrInvarianceLaw_v1` or equivalent source-side discriminator/transport law.",
        "three_tier_classification": "`open_or_blocked_physical_target`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "rr_e_factor_through_conditional_lemma": {
        "milestone": "`matter_coupling`",
        "object_type": "`conditional_lemma;missing_theorem`",
        "authority_level": "`canonical_tex;draft_control`",
        "definitions_introduced": "Conditional RR_E factor-through lemma shape.",
        "theorem_like_claims": "Conditional lemma shape depending on a missing source-side RR_E law.",
        "audits_passed": "`none` for unconditional proof.",
        "stress_results": "`none` for unconditional proof.",
        "gate_chair_results": "`none`.",
        "fail_closed_branches": "Conditional route fails closed without the missing transport law.",
        "known_obstructions": "Missing RR_E transport or invariance law.",
        "forbidden_overread": "Conditional factor-through shape as completed unrestricted theorem.",
        "downstream_blocked_targets": "Unrestricted RR_E theorem, detector semantics, matter coupling, benchmark promotion.",
        "next_theorem_needed": "RR_E transport-completeness or invariance source law.",
        "three_tier_classification": "`open_or_blocked_physical_target`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "rr_e_separation_obstruction_witness_v1": {
        "milestone": "`matter_coupling`",
        "object_type": "`witness;obstruction`",
        "authority_level": "`refuter_artifact`",
        "definitions_introduced": "Finite two-record RR_E separation witness under the cited stress route.",
        "theorem_like_claims": "Finite scoped witness supports the current obstruction classification.",
        "audits_passed": "Source-boundary stress artifact preserves finite scope.",
        "stress_results": "Finite two-record separation witness recorded.",
        "gate_chair_results": "`none`.",
        "fail_closed_branches": "Witness remains scoped and cannot close all future source-extension routes.",
        "known_obstructions": "Current premises do not prove unrestricted RR_E relation.",
        "forbidden_overread": "Finite witness as global impossibility, matter coupling, detector semantics, or benchmark result.",
        "downstream_blocked_targets": "Unrestricted RR_E theorem, matter coupling, detector semantics, Einstein equations, benchmark promotion.",
        "next_theorem_needed": "Source-side RR_E transport-completeness or invariance law closing the separation gap.",
        "three_tier_classification": "`accepted_evidence_precondition`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "rr_e_transport_completeness_or_invariance_law_v1": {
        "milestone": "`matter_coupling`",
        "object_type": "`source_extension_evidence;gate_decision;accepted_scoped_object`",
        "authority_level": "`gate_chair_artifact;canonical_tex;registry_row`",
        "definitions_introduced": "`RR_ETransportCompletenessOrInvarianceLaw_v1` proposal-only schema and scoped evidence/precondition boundary.",
        "theorem_like_claims": "Scoped evidence/precondition status for the RR_E transport-completeness or invariance schema only.",
        "audits_passed": "Smuggling audit passed under the source-side certificate-indexed scope.",
        "stress_results": "Refuter stress preserved fail-closed and no-target-import boundaries.",
        "gate_chair_results": "Accepted only as scoped source-extension evidence/precondition; not adopted as law.",
        "fail_closed_branches": "Unrestricted RR_E theorem, law adoption, detector semantics, and matter semantics remain blocked.",
        "known_obstructions": "Source-law adoption and unrestricted RR_E theorem proof remain missing.",
        "forbidden_overread": "Scoped RR_E transport evidence as adopted law, unrestricted theorem, detector semantics, matter semantics, or coupling law.",
        "downstream_blocked_targets": DOWNSTREAM_BLOCKS + "; unrestricted RR_E theorem",
        "next_theorem_needed": "Source-law adoption route or theorem proving unrestricted RR_E under declared assumptions.",
        "three_tier_classification": "`accepted_evidence_precondition`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "finite_toy_metric_response": {
        "milestone": "`finite_toy_metric_response`",
        "object_type": "`obstruction;frozen_negative_route`",
        "authority_level": "`refuter_artifact;registry_row`",
        "definitions_introduced": "Finite toy response family and tag-erasure variation obstruction.",
        "theorem_like_claims": "Scoped obstruction for the explicit-tag-only finite toy route.",
        "audits_passed": "`none` beyond the cited stress route.",
        "stress_results": "Tag removal collapses the response relation for the finite toy route.",
        "gate_chair_results": "`none`.",
        "fail_closed_branches": "Finite toy route is frozen locally under tag-removal and equivariant-totalization obstruction.",
        "known_obstructions": "`NDCL-RESP-LC-SELECTOR-UNDERDETERMINATION`; source-side response selector remains missing.",
        "forbidden_overread": "Local finite toy freeze as program-wide no-go conclusion or future source-extension impossibility.",
        "downstream_blocked_targets": "g_eff scope expansion, matter coupling, Einstein equations, benchmark promotion, completed derivation.",
        "next_theorem_needed": "Source-side response selector without explicit tags for sign, normalization, and token semantics.",
        "three_tier_classification": "`open_or_blocked_physical_target`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "finite_variation_robustness": {
        "milestone": "`finite_variation_robustness`",
        "object_type": "`theorem;source_extension_evidence`",
        "authority_level": "`refuter_artifact;registry_row;draft_control`",
        "definitions_introduced": "`FVR_src^{GSC}` fail-closed interface and stress-survival boundary.",
        "theorem_like_claims": "Named stress cases do not refute FVR as written; adoption remains absent.",
        "audits_passed": "Audited fail-closed interface summarized by the stress artifact.",
        "stress_results": "Refuter stress passed for written FVR interface and refuted non-fail-closed variants.",
        "gate_chair_results": "`none`; no adoption result.",
        "fail_closed_branches": "Unsupported or forbidden branches return bottom or defined failure.",
        "known_obstructions": "Human-gated adoption and arbitrary finite-variation theorem remain absent.",
        "forbidden_overread": "Stress survival as source-law adoption or arbitrary finite-variation robustness theorem.",
        "downstream_blocked_targets": "Source-law adoption, matter coupling, Einstein equations, benchmark promotion.",
        "next_theorem_needed": "Human-gated adoption and arbitrary finite-variation theorem if later routed.",
        "three_tier_classification": "`accepted_evidence_precondition`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "einstein_equations": {
        "milestone": "`einstein_equations`",
        "object_type": "`missing_theorem`",
        "authority_level": "`registry_row;registered_control_markdown`",
        "definitions_introduced": "`none`; the row records a downstream missing-theorem burden.",
        "theorem_like_claims": "No field-equation derivation is present.",
        "audits_passed": "`none`.",
        "stress_results": "`none`.",
        "gate_chair_results": "`none`.",
        "fail_closed_branches": "`none`.",
        "known_obstructions": "Dynamics, action, variation, or equivalent field-equation route remains missing.",
        "forbidden_overread": "Scoped `g_eff`, matter-coupling preconditions, or checker outputs as Einstein equations.",
        "downstream_blocked_targets": "Einstein equations, benchmark promotion, completed derivation.",
        "next_theorem_needed": "Source-side dynamics/action/variation principle and field-equation theorem.",
        "three_tier_classification": "`open_or_blocked_physical_target`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "benchmark_promotion": {
        "milestone": "`benchmark_promotion`",
        "object_type": "`missing_theorem;gate_decision`",
        "authority_level": "`registry_row;registered_control_markdown;human_gated`",
        "definitions_introduced": "`none`; the row records the benchmark-promotion block.",
        "theorem_like_claims": "Exact-GR benchmark promotion remains blocked by missing upstream burdens and protected authority.",
        "audits_passed": "`none` for promotion.",
        "stress_results": "`none` for promotion.",
        "gate_chair_results": "`none` for protected benchmark closure.",
        "fail_closed_branches": "Upstream scoped objects cannot be promoted to benchmark status.",
        "known_obstructions": "Matter semantics, Einstein equations, and protected benchmark review remain missing.",
        "forbidden_overread": "Scoped source objects, route progress, or narrow approvals as exact-GR benchmark promotion.",
        "downstream_blocked_targets": "Benchmark promotion and completed derivation.",
        "next_theorem_needed": "All upstream derivation burdens plus protected benchmark Gate Chair approval.",
        "three_tier_classification": "`open_or_blocked_physical_target`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
    "gate_chair_benchmark_closure": {
        "milestone": "`benchmark_promotion`",
        "object_type": "`gate_decision;missing_theorem`",
        "authority_level": "`registered_control_markdown;registry_row;human_gated`",
        "definitions_introduced": "`none`; the row records protected benchmark closure authority.",
        "theorem_like_claims": "Protected benchmark closure verdict is missing.",
        "audits_passed": "`none` for benchmark closure.",
        "stress_results": "`none` for benchmark closure.",
        "gate_chair_results": "Protected benchmark closure missing; narrower approvals do not satisfy it.",
        "fail_closed_branches": "Local implementation authorization cannot become benchmark closure authority.",
        "known_obstructions": "Protected benchmark Gate Chair review and upstream burdens remain missing.",
        "forbidden_overread": "Narrow scoped approvals, validation, or checkpoint commits as protected benchmark closure.",
        "downstream_blocked_targets": "Benchmark closure, benchmark promotion, completed derivation.",
        "next_theorem_needed": "Protected benchmark Gate Chair review and verdict after upstream burdens are discharged.",
        "three_tier_classification": "`open_or_blocked_physical_target`.",
        "linter_status": "`PASS`; P7-T02 inventory population claim-language scan.",
    },
}


INSERT_ORDER = [
    ("object_or_claim_name", ["milestone", "object_type"]),
    ("source_authority_type", ["authority_level"]),
    ("statement_or_decision", ["definitions_introduced", "theorem_like_claims"]),
    ("physical_non_conclusions", ["audits_passed", "stress_results", "gate_chair_results", "fail_closed_branches", "known_obstructions"]),
    ("allowed_reuse", ["forbidden_overread", "downstream_blocked_targets"]),
    ("candidate_next_task", ["next_theorem_needed"]),
    ("overread_guard", ["three_tier_classification", "linter_status"]),
]


NEW_ITEMS = r'''
### Item 10F: matter_coupling_precondition_assembly_v1

- `frontier_item_id`: `matter_coupling_precondition_assembly_v1`
- `frontier_item_class`: `source_extension_evidence;gate_decision`
- `object_or_claim_name`: `MatterCouplingPreconditionAssembly_v1(E)` /
  `MCPA^cand_v1(E)` scoped pre-coupling assembly evidence.
- `milestone`: `matter_coupling`
- `object_type`: `source_extension_evidence;gate_decision`
- `status_layer_summary`:
  - `control_status`: `accepted_as_scoped_evidence_precondition`
  - `mathematical_status`: `proposal_only_pre_coupling_assembly_candidate`
  - `physical_status`: `not_source_law_not_coupling_law_not_matter_coupling`
  - `promotion_status`: `scoped_source_evidence_only`
  - `overread_guard`: `no_source_law_adoption;no_metricdata_e_adoption;no_geff_scope_expansion;no_coupling_law_adoption;no_matter_coupling_derivation;no_matter_coupling_adoption;no_stress_energy_semantics;no_stress_energy_tensor;no_matter_action;no_detector_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation;no_future_source_extension_impossibility;no_global_theory_rejection`
- `source_artifact_path`:
  `research_control/tasks/RT-20260630-008/artifacts/matter_coupling_precondition_assembly_target_v1.tex`;
  `research_control/tasks/RT-20260630-009/artifacts/matter_coupling_precondition_assembly_candidate_v1.tex`;
  `research_control/tasks/RT-20260630-010/artifacts/matter_coupling_precondition_assembly_candidate_smuggling_audit_v1.tex`;
  `research_control/tasks/RT-20260630-011/artifacts/matter_coupling_precondition_assembly_candidate_refuter_stress_v1.tex`;
  `research_control/tasks/RT-20260630-013/artifacts/matter_coupling_precondition_assembly_source_extension_evidence_gate_chair_review_v1.tex`;
  `registries/DISTANCE_TO_GR_LEDGER.csv` row `matter_coupling`.
- `source_authority_type`: `registered_tex_artifact;gate_chair_artifact;distance_to_gr_ledger_row`
- `authority_level`: `gate_chair_artifact;canonical_tex;registry_row`
- `assumptions`:
  - The candidate is source-local and pre-coupling.
  - The accepted status is evidence/precondition only.
  - The candidate completed construction, smuggling audit, Refuter stress, and
    narrow Gate Chair evidence-status review.
- `definitions_used`: `MatterCouplingPreconditionAssembly_v1(E)`;
  `MCPA^cand_v1(E)`; source-local pre-coupling assembly; no-target-import
  certificate.
- `definitions_introduced`: Target and candidate grammar for source-local
  pre-coupling assembly in the cited RT-008 and RT-009 artifacts.
- `statement_or_decision`: Gate Chair accepted `MCPA^cand_v1(E)` only as
  scoped source-extension matter-coupling precondition evidence/precondition.
- `theorem_like_claims`: Scoped evidence/precondition status for the
  proposal-only MCPA candidate; no source-law or coupling-law theorem.
- `mathematical_conclusion`: The object can be cited only as scoped
  source-extension precondition evidence for later non-promotional routing.
- `audits_passed`: Smuggling audit passed as source-pure under RT-20260630-010
  scope.
- `stress_results`: Refuter stress survived as a draft/control bridge-facing
  candidate path under RT-20260630-011 scope.
- `gate_chair_results`: RT-20260630-013 accepted scoped evidence/precondition
  status only.
- `fail_closed_branches`: Adoption, source-extension data beyond the exact
  gate question, coupling law, matter coupling, and downstream GR routes remain
  blocked.
- `known_obstructions`: Current ontology does not derive MCPA as an adopted
  source-side coupling-precondition assembly law.
- `physical_non_conclusions`:
  - Not source-law adoption.
  - Not source-extension data adoption beyond the exact scoped Gate result.
  - Not coupling-law adoption.
  - Not matter coupling, stress-energy semantics, detector semantics, matter
    action, Einstein equations, benchmark promotion, or completed derivation.
- `forbidden_overread`: MCPA evidence/precondition as adopted MCPA, adopted
  source law, coupling law, matter coupling, field equation, benchmark status,
  future source-extension impossibility, or program-wide no-go conclusion.
- `downstream_blocked_targets`: `source-law adoption`; `coupling-law adoption`;
  `matter-coupling derivation or adoption`; `stress-energy semantics`;
  `matter action`; `Einstein equations`; `benchmark promotion`; `completed derivation`.
- `allowed_reuse`: Cite as scoped precondition evidence for later source-side
  coupling-law target or candidate packets.
- `blocked_reuse`: Do not cite as matter coupling, stress-energy, detector
  semantics, source law, or coupling law.
- `dependency_items`: `matter_coupling_precondition_evidence`;
  `g_eff_gsc_cand`; `m_src_gsc`
- `missing_theorem_or_primitive`: Adopted source-side law connecting the
  precondition assembly to matter semantics or matter coupling remains missing.
- `next_theorem_needed`: Source-side coupling-law target/candidate theorem or
  obstruction under no-target-import constraints.
- `candidate_next_task`: none from this inventory; use live continue-research
  routing.
- `three_tier_classification`: `accepted_evidence_precondition`
- `linter_status`: `PASS`; P7-T02 inventory population claim-language scan.
- `overread_guard`: `no_source_law_adoption;no_metricdata_e_adoption;no_geff_scope_expansion;no_coupling_law_adoption;no_matter_coupling_derivation;no_matter_coupling_adoption;no_stress_energy_semantics;no_stress_energy_tensor;no_matter_action;no_detector_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation;no_future_source_extension_impossibility;no_global_theory_rejection`
- `external_review_notes`: This row separates the MCPA evidence/precondition
  gate from the older aggregate matter-coupling evidence row. It adds no
  matter-coupling adoption.

### Item 10G: source_coupling_law_candidate_cand_v1

- `frontier_item_id`: `source_coupling_law_candidate_cand_v1`
- `frontier_item_class`: `source_extension_evidence;gate_decision`
- `object_or_claim_name`: `SourceCouplingLawCandidate^cand_v1(E)` scoped
  source-coupling-law candidate evidence.
- `milestone`: `matter_coupling`
- `object_type`: `source_extension_evidence;gate_decision`
- `status_layer_summary`:
  - `control_status`: `accepted_as_scoped_evidence_precondition`
  - `mathematical_status`: `proposal_only_source_coupling_law_candidate`
  - `physical_status`: `not_source_law_not_coupling_law_not_matter_coupling`
  - `promotion_status`: `scoped_source_evidence_only`
  - `overread_guard`: `no_source_law_adoption;no_metricdata_e_adoption;no_geff_scope_expansion;no_coupling_law_adoption;no_matter_coupling_derivation;no_matter_coupling_adoption;no_stress_energy_semantics;no_matter_action;no_detector_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation`
- `source_artifact_path`:
  `research_control/tasks/RT-20260630-015/artifacts/source_coupling_law_target_v1.tex`;
  `research_control/tasks/RT-20260630-016/artifacts/source_coupling_law_candidate_v1.tex`;
  `research_control/tasks/RT-20260630-017/artifacts/source_coupling_law_candidate_smuggling_audit_v1.tex`;
  `research_control/tasks/RT-20260630-018/artifacts/source_coupling_law_candidate_refuter_stress_v1.tex`;
  `research_control/tasks/RT-20260630-020/artifacts/source_coupling_law_candidate_source_extension_evidence_gate_chair_review_v1.tex`;
  `registries/DISTANCE_TO_GR_LEDGER.csv` row `matter_coupling`.
- `source_authority_type`: `registered_tex_artifact;gate_chair_artifact;distance_to_gr_ledger_row`
- `authority_level`: `gate_chair_artifact;canonical_tex;registry_row`
- `assumptions`:
  - The candidate uses scoped MCPA evidence/precondition only as input.
  - The candidate is proposal-only unless and until separately adopted under
    protected authority.
  - Gate Chair acceptance is evidence/precondition status only.
- `definitions_used`: `SourceCouplingLawCandidate^cand_v1(E)`;
  `SourceCouplingLawTarget_v1`; `MCPA^cand_v1(E)`.
- `definitions_introduced`: Source-coupling-law target and proposal-only
  candidate grammar in the cited RT-015 and RT-016 artifacts.
- `statement_or_decision`: Gate Chair accepted the candidate only as scoped
  source-extension source-coupling-law-candidate evidence/precondition.
- `theorem_like_claims`: Proposal-only candidate evidence/precondition status;
  no source-law or coupling-law adoption.
- `mathematical_conclusion`: The candidate may be used as scoped evidence in
  later non-promotional matter-coupling research packets.
- `audits_passed`: Smuggling audit passed as source-pure under RT-20260630-017
  scope.
- `stress_results`: Refuter stress survived as a bridge-facing candidate path
  under RT-20260630-018 scope.
- `gate_chair_results`: RT-20260630-020 accepted scoped evidence/precondition
  status only.
- `fail_closed_branches`: Candidate status does not adopt source law,
  coupling law, matter semantics, detector semantics, matter coupling, or
  downstream GR.
- `known_obstructions`: Source-law adoption, coupling-law adoption, and matter
  coupling remain missing.
- `physical_non_conclusions`:
  - Not source-law adoption.
  - Not coupling-law adoption.
  - Not matter-coupling derivation or adoption.
  - Not stress-energy semantics, detector semantics, matter action, Einstein
    equations, benchmark promotion, or completed derivation.
- `forbidden_overread`: SourceCouplingLawCandidate evidence as adopted source
  law, adopted coupling law, matter coupling, or field-equation premise.
- `downstream_blocked_targets`: `coupling-law adoption`; `matter-coupling
  derivation or adoption`; `stress-energy semantics`; `matter action`;
  `Einstein equations`; `benchmark promotion`; `completed derivation`.
- `allowed_reuse`: Cite as scoped source-coupling-law candidate evidence in
  future bounded packets.
- `blocked_reuse`: Do not treat candidate construction, audit, stress, or Gate
  evidence status as law adoption.
- `dependency_items`: `matter_coupling_precondition_assembly_v1`;
  `matter_coupling_precondition_evidence`; `g_eff_gsc_cand`
- `missing_theorem_or_primitive`: Adopted source-side coupling law remains
  missing.
- `next_theorem_needed`: Source-side coupling-law adoption theorem or precise
  obstruction, if selected by live routing and protected authority.
- `candidate_next_task`: none from this inventory; use live continue-research
  routing.
- `three_tier_classification`: `accepted_evidence_precondition`
- `linter_status`: `PASS`; P7-T02 inventory population claim-language scan.
- `overread_guard`: `no_source_law_adoption;no_metricdata_e_adoption;no_geff_scope_expansion;no_coupling_law_adoption;no_matter_coupling_derivation;no_matter_coupling_adoption;no_stress_energy_semantics;no_matter_action;no_detector_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation`
- `external_review_notes`: This row distinguishes source-coupling-law
  candidate evidence from actual coupling-law adoption.

### Item 10H: ms_stable_partition_precondition_v1

- `frontier_item_id`: `ms_stable_partition_precondition_v1`
- `frontier_item_class`: `source_extension_evidence;gate_decision`
- `object_or_claim_name`: `MSStablePartitionPrecondition_v1` scoped stable
  matter-semantics partition precondition.
- `milestone`: `matter_coupling`
- `object_type`: `source_extension_evidence;gate_decision`
- `status_layer_summary`:
  - `control_status`: `accepted_as_scoped_evidence_precondition`
  - `mathematical_status`: `stable_partition_precondition_evidence`
  - `physical_status`: `not_matter_semantics_not_detector_semantics_not_matter_coupling`
  - `promotion_status`: `scoped_source_evidence_only`
  - `overread_guard`: `no_source_law_adoption;no_coupling_law_adoption;no_matter_coupling_derivation;no_matter_coupling_adoption;no_stress_energy_semantics;no_matter_action;no_detector_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation`
- `source_artifact_path`:
  `research_control/tasks/RT-20260630-046/artifacts/matter_semantics_stable_partition_precondition_v1.tex`;
  `research_control/tasks/RT-20260630-047/artifacts/matter_semantics_stable_partition_precondition_smuggling_audit_v1.tex`;
  `research_control/tasks/RT-20260630-048/artifacts/matter_semantics_stable_partition_precondition_refuter_stress_v1.tex`;
  `research_control/tasks/RT-20260630-050/artifacts/ms_stable_partition_precondition_source_extension_evidence_gate_chair_review_v1.tex`;
  `registries/DISTANCE_TO_GR_LEDGER.csv` row `matter_coupling`.
- `source_authority_type`: `registered_tex_artifact;gate_chair_artifact;distance_to_gr_ledger_row`
- `authority_level`: `gate_chair_artifact;canonical_tex;registry_row`
- `assumptions`:
  - Stable partition status is a source-side precondition.
  - Acceptance does not adopt matter semantics or detector semantics.
- `definitions_used`: `MSStablePartitionPrecondition_v1`; source-side stable
  partition precondition.
- `definitions_introduced`: Stable partition precondition target and evidence
  grammar from the cited RT-046 artifact.
- `statement_or_decision`: Gate Chair accepted the partition precondition only
  as scoped source-extension evidence/precondition.
- `theorem_like_claims`: Scoped precondition evidence only; no matter
  semantics theorem.
- `mathematical_conclusion`: The stable partition precondition can be cited as
  scoped input for later matter-semantics bridge work.
- `audits_passed`: Smuggling audit passed under RT-20260630-047 scope.
- `stress_results`: Refuter stress survived under RT-20260630-048 scope.
- `gate_chair_results`: RT-20260630-050 accepted scoped evidence/precondition
  status only.
- `fail_closed_branches`: Matter semantics, detector semantics, coupling law,
  matter coupling, and downstream GR remain blocked.
- `known_obstructions`: Adopted matter semantics and coupling law remain
  missing.
- `physical_non_conclusions`:
  - Not matter-semantics adoption.
  - Not detector-semantics adoption.
  - Not coupling-law adoption.
  - Not matter-coupling derivation or adoption.
  - Not Einstein equations, benchmark promotion, or completed derivation.
- `forbidden_overread`: Partition precondition evidence as matter semantics,
  detector semantics, coupling law, or matter coupling.
- `downstream_blocked_targets`: `matter-semantics adoption`;
  `detector-semantics adoption`; `coupling-law adoption`; `matter-coupling
  derivation or adoption`; `Einstein equations`; `benchmark promotion`.
- `allowed_reuse`: Cite as scoped stable-partition precondition evidence.
- `blocked_reuse`: Do not cite as matter semantics or physical matter-sector
  semantics.
- `dependency_items`: `matter_coupling_precondition_evidence`;
  `source_coupling_law_candidate_cand_v1`
- `missing_theorem_or_primitive`: Adopted matter-semantics law remains
  missing.
- `next_theorem_needed`: Matter-semantics bridge theorem or precise
  obstruction.
- `candidate_next_task`: none from this inventory; use live continue-research
  routing.
- `three_tier_classification`: `accepted_evidence_precondition`
- `linter_status`: `PASS`; P7-T02 inventory population claim-language scan.
- `overread_guard`: `no_source_law_adoption;no_coupling_law_adoption;no_matter_coupling_derivation;no_matter_coupling_adoption;no_stress_energy_semantics;no_matter_action;no_detector_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation`
- `external_review_notes`: Stable partition evidence is source-side and
  precondition-only.

### Item 10I: ms_stable_matter_semantics_bridge_v1

- `frontier_item_id`: `ms_stable_matter_semantics_bridge_v1`
- `frontier_item_class`: `source_extension_evidence;gate_decision`
- `object_or_claim_name`: `MSStableMatterSemanticsBridge_v1(E;B_current)`
  scoped stable matter-semantics bridge evidence.
- `milestone`: `matter_coupling`
- `object_type`: `source_extension_evidence;gate_decision`
- `status_layer_summary`:
  - `control_status`: `accepted_as_scoped_evidence_precondition`
  - `mathematical_status`: `stable_matter_semantics_bridge_evidence`
  - `physical_status`: `not_matter_semantics_not_detector_semantics_not_matter_coupling`
  - `promotion_status`: `scoped_source_evidence_only`
  - `overread_guard`: `no_source_law_adoption;no_coupling_law_adoption;no_matter_coupling_derivation;no_matter_coupling_adoption;no_stress_energy_semantics;no_matter_action;no_detector_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation;no_future_source_extension_impossibility;no_global_theory_rejection`
- `source_artifact_path`:
  `research_control/tasks/RT-20260630-052/artifacts/ms_stable_matter_semantics_bridge_candidate_v1.tex`;
  `research_control/tasks/RT-20260630-053/artifacts/ms_stable_matter_semantics_bridge_smuggling_audit_v1.tex`;
  `research_control/tasks/RT-20260630-054/artifacts/ms_stable_matter_semantics_bridge_refuter_stress_v1.tex`;
  `research_control/tasks/RT-20260630-056/artifacts/ms_stable_matter_semantics_bridge_source_extension_evidence_gate_chair_review_v1.tex`;
  `registries/DISTANCE_TO_GR_LEDGER.csv` row `matter_coupling`.
- `source_authority_type`: `registered_tex_artifact;gate_chair_artifact;distance_to_gr_ledger_row`
- `authority_level`: `gate_chair_artifact;canonical_tex;registry_row`
- `assumptions`:
  - The bridge is finite/local, source-side, and fail-closed.
  - Acceptance is scoped evidence/precondition only.
- `definitions_used`: `MSStableMatterSemanticsBridge_v1(E;B_current)`;
  stable matter-semantics bridge evidence; source-side fail-closed route.
- `definitions_introduced`: Stable matter-semantics bridge candidate grammar
  from RT-20260630-052.
- `statement_or_decision`: Gate Chair accepted the constructed bridge object
  only as scoped source-extension stable matter-semantics bridge
  evidence/precondition.
- `theorem_like_claims`: Scoped bridge evidence/precondition status only; no
  adopted matter-semantics theorem.
- `mathematical_conclusion`: The bridge can be cited as scoped precondition
  evidence for later readiness or profile targets.
- `audits_passed`: Smuggling audit passed under RT-20260630-053 scope.
- `stress_results`: Refuter stress survived under RT-20260630-054 scope.
- `gate_chair_results`: RT-20260630-056 accepted scoped evidence/precondition
  status only.
- `fail_closed_branches`: Source-law adoption, matter-semantics adoption,
  detector-semantics adoption, coupling law, matter coupling, and downstream GR
  remain blocked.
- `known_obstructions`: Current ontology does not derive a source-side law
  adopting the bridge as matter semantics, detector semantics, coupling law, or
  matter coupling.
- `physical_non_conclusions`:
  - Not source-law adoption.
  - Not matter-semantics adoption.
  - Not detector-semantics adoption.
  - Not coupling-law adoption.
  - Not matter-coupling derivation or adoption.
  - Not stress-energy semantics, matter action, Einstein equations, benchmark
    promotion, or completed derivation.
- `forbidden_overread`: Bridge evidence as adopted matter semantics, detector
  semantics, coupling law, matter coupling, or future source-extension
  impossibility.
- `downstream_blocked_targets`: `matter-semantics adoption`;
  `detector-semantics adoption`; `coupling-law adoption`; `matter-coupling
  derivation or adoption`; `stress-energy semantics`; `matter action`;
  `Einstein equations`; `benchmark promotion`.
- `allowed_reuse`: Cite as scoped bridge evidence/precondition for readiness
  or positive-profile targets.
- `blocked_reuse`: Do not cite as adopted matter semantics, physical detector
  semantics, or coupling law.
- `dependency_items`: `ms_stable_partition_precondition_v1`;
  `matter_coupling_precondition_evidence`
- `missing_theorem_or_primitive`: Source-side law adopting matter semantics,
  detector semantics, coupling law, or matter coupling remains missing.
- `next_theorem_needed`: Readiness-law or positive-profile theorem route if
  selected by live state and protected authority.
- `candidate_next_task`: none from this inventory; use live continue-research
  routing.
- `three_tier_classification`: `accepted_evidence_precondition`
- `linter_status`: `PASS`; P7-T02 inventory population claim-language scan.
- `overread_guard`: `no_source_law_adoption;no_coupling_law_adoption;no_matter_coupling_derivation;no_matter_coupling_adoption;no_stress_energy_semantics;no_matter_action;no_detector_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation;no_future_source_extension_impossibility;no_global_theory_rejection`
- `external_review_notes`: The bridge row is evidence/precondition only and
  must not be collapsed into matter-semantics adoption.

### Item 10J: source_matter_semantics_adoption_readiness_law_v1

- `frontier_item_id`: `source_matter_semantics_adoption_readiness_law_v1`
- `frontier_item_class`: `source_extension_evidence;gate_decision`
- `object_or_claim_name`: `SourceMatterSemanticsAdoptionReadinessLaw_v1`
  scoped adoption-readiness evidence.
- `milestone`: `matter_coupling`
- `object_type`: `source_extension_evidence;gate_decision`
- `status_layer_summary`:
  - `control_status`: `accepted_as_scoped_evidence_precondition`
  - `mathematical_status`: `proposal_only_adoption_readiness_evidence`
  - `physical_status`: `not_source_law_not_matter_semantics_not_matter_coupling`
  - `promotion_status`: `scoped_source_evidence_only`
  - `overread_guard`: `no_source_law_adoption;no_coupling_law_adoption;no_matter_coupling_derivation;no_matter_coupling_adoption;no_stress_energy_semantics;no_matter_action;no_detector_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation;no_future_source_extension_impossibility;no_global_theory_rejection`
- `source_artifact_path`:
  `research_control/tasks/RT-20260701-001/artifacts/source_matter_semantics_adoption_readiness_law_target_v1.tex`;
  `research_control/tasks/RT-20260701-002/artifacts/source_matter_semantics_adoption_readiness_law_smuggling_audit_v1.tex`;
  `research_control/tasks/RT-20260701-007/artifacts/source_matter_semantics_adoption_readiness_law_refuter_stress_v1.tex`;
  `research_control/tasks/RT-20260701-009/artifacts/source_matter_semantics_adoption_readiness_law_evidence_gate_chair_review_v1.tex`;
  `registries/DISTANCE_TO_GR_LEDGER.csv` row `matter_coupling`.
- `source_authority_type`: `registered_tex_artifact;gate_chair_artifact;distance_to_gr_ledger_row`
- `authority_level`: `gate_chair_artifact;canonical_tex;registry_row`
- `assumptions`:
  - The object is proposal-only except for scoped evidence/precondition status.
  - Acceptance does not adopt the object as a law.
- `definitions_used`: `SourceMatterSemanticsAdoptionReadinessLaw_v1`;
  matter-semantics adoption-readiness evidence; source-side fail-closed route.
- `definitions_introduced`: Adoption-readiness target grammar from
  RT-20260701-001.
- `statement_or_decision`: Gate Chair accepted the object only as scoped
  source-extension matter-semantics adoption-readiness evidence/precondition.
- `theorem_like_claims`: Scoped readiness evidence/precondition status only;
  no law adoption.
- `mathematical_conclusion`: The readiness object can be cited as scoped
  precondition evidence for positive source-matter-semantics target/profile
  work.
- `audits_passed`: Smuggling audit passed under RT-20260701-002 scope.
- `stress_results`: Refuter stress survived under RT-20260701-007 scope.
- `gate_chair_results`: RT-20260701-009 accepted scoped evidence/precondition
  status only.
- `fail_closed_branches`: Source-law adoption,
  `SourceMatterSemanticsAdoptionReadinessLaw_v1` law adoption, matter
  semantics, detector semantics, coupling law, matter coupling, and downstream
  GR remain blocked.
- `known_obstructions`: Current ontology does not derive adoption of this
  object as a source law or matter semantics.
- `physical_non_conclusions`:
  - Not source-law adoption.
  - Not `SourceMatterSemanticsAdoptionReadinessLaw_v1` law adoption.
  - Not matter-semantics adoption.
  - Not detector-semantics adoption.
  - Not coupling-law adoption.
  - Not matter-coupling derivation or adoption.
  - Not Einstein equations, benchmark promotion, or completed derivation.
- `forbidden_overread`: Readiness evidence as adopted law, adopted matter
  semantics, detector semantics, coupling law, matter coupling, or downstream
  GR premise.
- `downstream_blocked_targets`: `SourceMatterSemanticsAdoptionReadinessLaw_v1`
  law adoption; `matter-semantics adoption`; `detector-semantics adoption`;
  `coupling-law adoption`; `matter-coupling derivation or adoption`;
  `Einstein equations`; `benchmark promotion`.
- `allowed_reuse`: Cite as scoped readiness evidence/precondition for positive
  source-matter-semantics target/profile work.
- `blocked_reuse`: Do not cite as a source law, matter semantics, detector
  semantics, or coupling law.
- `dependency_items`: `ms_stable_matter_semantics_bridge_v1`;
  `ms_stable_partition_precondition_v1`
- `missing_theorem_or_primitive`: Adopted readiness law, adopted matter
  semantics, and coupling law remain missing.
- `next_theorem_needed`: Positive source-matter-semantics target/profile route
  or precise obstruction under protected boundaries.
- `candidate_next_task`: none from this inventory; use live continue-research
  routing.
- `three_tier_classification`: `accepted_evidence_precondition`
- `linter_status`: `PASS`; P7-T02 inventory population claim-language scan.
- `overread_guard`: `no_source_law_adoption;no_coupling_law_adoption;no_matter_coupling_derivation;no_matter_coupling_adoption;no_stress_energy_semantics;no_matter_action;no_detector_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation;no_future_source_extension_impossibility;no_global_theory_rejection`
- `external_review_notes`: The word "Law" is part of the candidate name here;
  the tracked status is not law adoption.

### Item 10K: positive_source_matter_semantics_target_v1

- `frontier_item_id`: `positive_source_matter_semantics_target_v1`
- `frontier_item_class`: `definition;theorem_target;missing_theorem`
- `object_or_claim_name`: `PositiveSourceMatterSemanticsTarget_v1`
  proposal-only source-side matter-semantics target.
- `milestone`: `matter_coupling`
- `object_type`: `definition;theorem_target;missing_theorem`
- `status_layer_summary`:
  - `control_status`: `proposal_only_target_formalized`
  - `mathematical_status`: `source_side_target_grammar_only`
  - `physical_status`: `not_matter_semantics_not_detector_semantics_not_matter_coupling`
  - `promotion_status`: `draft_control_only`
  - `overread_guard`: `no_source_law_adoption;no_coupling_law_adoption;no_matter_coupling_derivation;no_matter_coupling_adoption;no_stress_energy_semantics;no_matter_action;no_detector_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation`
- `source_artifact_path`:
  `research_control/tasks/RT-20260701-015/artifacts/positive_source_matter_semantics_target_v1.tex`;
  `registries/DISTANCE_TO_GR_LEDGER.csv` row `matter_coupling`.
- `source_authority_type`: `registered_tex_artifact;distance_to_gr_ledger_row`
- `authority_level`: `canonical_tex;registry_row;draft_control`
- `assumptions`:
  - The target formalizes admissible source records and source-side labels.
  - A target grammar is not an adopted matter-semantics candidate.
- `definitions_used`: `PositiveSourceMatterSemanticsTarget_v1`;
  admissible source records; source-side labels; source equivalence and
  separation conditions.
- `definitions_introduced`: Positive source-side matter-semantics target
  grammar from RT-20260701-015.
- `statement_or_decision`: The target is proposal-only draft/control
  formalization for future candidate construction or obstruction.
- `theorem_like_claims`: Conditional source-purity property for future
  candidates satisfying all target clauses; no matter-semantics adoption.
- `mathematical_conclusion`: Target grammar exists for later candidate
  construction; no candidate is adopted by this target.
- `audits_passed`: `none`; target formalization only.
- `stress_results`: `none`; target formalization only.
- `gate_chair_results`: `none`; prior readiness and bridge Gate results are
  retained only as scoped inputs.
- `fail_closed_branches`: Target formalization cannot be reused as matter
  semantics, detector semantics, coupling law, or matter coupling.
- `known_obstructions`: Actual adopted matter-semantics candidate and coupling
  law remain missing.
- `physical_non_conclusions`:
  - Not matter-semantics adoption.
  - Not detector-semantics adoption.
  - Not coupling-law adoption.
  - Not matter-coupling derivation or adoption.
  - Not stress-energy semantics, matter action, Einstein equations, benchmark
    promotion, or completed derivation.
- `forbidden_overread`: Target grammar as positive matter semantics, physical
  detector semantics, coupling law, or matter-coupling proof.
- `downstream_blocked_targets`: `matter-semantics adoption`;
  `detector-semantics adoption`; `coupling-law adoption`; `matter-coupling
  derivation or adoption`; `Einstein equations`; `benchmark promotion`.
- `allowed_reuse`: Cite as source-side target grammar for future candidate
  construction or obstruction.
- `blocked_reuse`: Do not cite as a constructed or adopted matter-semantics
  profile.
- `dependency_items`: `source_matter_semantics_adoption_readiness_law_v1`;
  `ms_stable_matter_semantics_bridge_v1`
- `missing_theorem_or_primitive`: Positive matter-semantics candidate theorem
  or obstruction remains missing at this target stage.
- `next_theorem_needed`: Candidate constructor result under the target or
  precise obstruction.
- `candidate_next_task`: none from this inventory; use live continue-research
  routing.
- `three_tier_classification`: `open_or_blocked_physical_target`
- `linter_status`: `PASS`; P7-T02 inventory population claim-language scan.
- `overread_guard`: `no_source_law_adoption;no_coupling_law_adoption;no_matter_coupling_derivation;no_matter_coupling_adoption;no_stress_energy_semantics;no_matter_action;no_detector_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation`
- `external_review_notes`: The target is useful because it states the
  admissibility grammar; it does not supply matter semantics.

### Item 10L: positive_ms_profile_v1

- `frontier_item_id`: `positive_ms_profile_v1`
- `frontier_item_class`: `source_extension_evidence;gate_decision`
- `object_or_claim_name`: `PositiveMSProfile_v1` scoped positive
  source-matter-semantics profile evidence.
- `milestone`: `matter_coupling`
- `object_type`: `source_extension_evidence;gate_decision`
- `status_layer_summary`:
  - `control_status`: `accepted_as_scoped_evidence_precondition`
  - `mathematical_status`: `positive_source_matter_semantics_profile_evidence`
  - `physical_status`: `not_matter_semantics_not_detector_semantics_not_matter_coupling`
  - `promotion_status`: `scoped_source_evidence_only`
  - `overread_guard`: `no_source_law_adoption;no_coupling_law_adoption;no_matter_coupling_derivation;no_matter_coupling_adoption;no_stress_energy_semantics;no_matter_action;no_detector_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation;no_future_source_extension_impossibility;no_global_theory_rejection`
- `source_artifact_path`:
  `research_control/tasks/RT-20260701-016/artifacts/positive_source_matter_semantics_profile_candidate_v1.tex`;
  `research_control/tasks/RT-20260701-017/artifacts/positive_source_matter_semantics_profile_smuggling_audit_v1.tex`;
  `research_control/tasks/RT-20260701-018/artifacts/positive_source_matter_semantics_profile_refuter_stress_v1.tex`;
  `research_control/tasks/RT-20260701-020/artifacts/positive_source_matter_semantics_profile_gate_chair_review_v1.tex`;
  `registries/DISTANCE_TO_GR_LEDGER.csv` row `matter_coupling`.
- `source_authority_type`: `registered_tex_artifact;gate_chair_artifact;distance_to_gr_ledger_row`
- `authority_level`: `gate_chair_artifact;canonical_tex;registry_row`
- `assumptions`:
  - The profile is source-side and fail-closed.
  - Profile labels and readiness predicates remain guarded source syntax and
    routing status only.
  - Gate Chair acceptance is scoped evidence/precondition only.
- `definitions_used`: `PositiveMSProfile_v1`; profile label; readiness
  predicate; no-target certificates; RR_E separation structures.
- `definitions_introduced`: Positive source-matter-semantics profile candidate
  grammar from RT-20260701-016.
- `statement_or_decision`: Gate Chair accepted `PositiveMSProfile_v1` only as
  scoped source-extension positive source-matter-semantics profile
  evidence/precondition.
- `theorem_like_claims`: Scoped positive profile evidence/precondition status
  only; no matter-semantics adoption.
- `mathematical_conclusion`: The profile can be cited as scoped evidence for
  boundary vocabulary and future non-promotional continuation.
- `audits_passed`: Smuggling audit passed under RT-20260701-017 scope.
- `stress_results`: Refuter stress survived under RT-20260701-018 scope.
- `gate_chair_results`: RT-20260701-020 accepted scoped evidence/precondition
  status only.
- `fail_closed_branches`: Source-law adoption, PositiveMSProfile adoption,
  readiness-law adoption, matter semantics, detector semantics, coupling law,
  matter coupling, and downstream GR remain blocked.
- `known_obstructions`: Adopted matter semantics, detector semantics, coupling
  law, matter coupling, and Einstein equations remain missing.
- `physical_non_conclusions`:
  - Not source-law adoption.
  - Not `PositiveMSProfile_v1` adoption.
  - Not `SourceMatterSemanticsAdoptionReadinessLaw_v1` law adoption.
  - Not matter-semantics adoption.
  - Not detector-semantics adoption.
  - Not coupling-law adoption.
  - Not matter-coupling derivation or adoption.
  - Not stress-energy semantics, matter action, Einstein equations, benchmark
    promotion, or completed derivation.
- `forbidden_overread`: Positive profile evidence as adopted matter semantics,
  detector semantics, coupling law, matter coupling, benchmark status, future
  source-extension impossibility, or program-wide no-go conclusion.
- `downstream_blocked_targets`: `PositiveMSProfile_v1 adoption`;
  `matter-semantics adoption`; `detector-semantics adoption`;
  `coupling-law adoption`; `matter-coupling derivation or adoption`;
  `Einstein equations`; `benchmark promotion`; `completed derivation`.
- `allowed_reuse`: Cite as scoped positive profile evidence/precondition for
  claim-vocabulary control and later non-promotional route selection.
- `blocked_reuse`: Do not cite as adopted matter semantics, physical detector
  semantics, coupling law, matter coupling, or benchmark evidence.
- `dependency_items`: `positive_source_matter_semantics_target_v1`;
  `source_matter_semantics_adoption_readiness_law_v1`;
  `ms_stable_matter_semantics_bridge_v1`;
  `rr_e_transport_completeness_or_invariance_law_v1`
- `missing_theorem_or_primitive`: Adopted matter-semantics law, detector
  semantics, coupling law, matter coupling, and field equations remain missing.
- `next_theorem_needed`: Source-law or coupling-law adoption theorem, or a
  precise obstruction, under protected authority.
- `candidate_next_task`: none from this inventory; use live continue-research
  routing.
- `three_tier_classification`: `accepted_evidence_precondition`
- `linter_status`: `PASS`; P7-T02 inventory population claim-language scan.
- `overread_guard`: `no_source_law_adoption;no_coupling_law_adoption;no_matter_coupling_derivation;no_matter_coupling_adoption;no_stress_energy_semantics;no_matter_action;no_detector_semantics;no_einstein_equations;no_benchmark_promotion;no_completed_derivation;no_future_source_extension_impossibility;no_global_theory_rejection`
- `external_review_notes`: The profile is the highest-risk positive-sounding
  row. It is accepted evidence/precondition only, not matter-semantics
  adoption.
'''


P7_COVERAGE = r'''
P7-T02 live-core item coverage:

| Required item | Inventory item |
| --- | --- |
| `source_ontology_primitives` | `source_ontology_primitives` |
| `EqSrc` | `source_equivalence_eqsrc` |
| `RetainH` | `retain_h` |
| `GenH` | `gen_h` |
| `ObsLoc_lc` | `obsloc_lc` |
| `Resp_lc` | `resp_lc` |
| `M_src^{GSC}(E)` | `m_src_gsc` |
| `g_eff^{GSC-cand}(E;G^beta,T_src(E))` | `g_eff_gsc_cand` |
| `MatterCouplingPreconditionAssembly` / MCPA evidence/precondition | `matter_coupling_precondition_assembly_v1`; `matter_coupling_precondition_evidence` |
| `SourceCouplingLawCandidate^cand_v1(E)` | `source_coupling_law_candidate_cand_v1` |
| `MSStablePartitionPrecondition_v1` | `ms_stable_partition_precondition_v1` |
| `MSStableMatterSemanticsBridge_v1(E;B_current)` | `ms_stable_matter_semantics_bridge_v1` |
| `SourceMatterSemanticsAdoptionReadinessLaw_v1` | `source_matter_semantics_adoption_readiness_law_v1` |
| `PositiveSourceMatterSemanticsTarget_v1` | `positive_source_matter_semantics_target_v1` |
| `PositiveMSProfile_v1` | `positive_ms_profile_v1` |
| `RR_ETheoremTarget_v1` | `rr_e_theorem_target_v1` |
| `RR_E_underdetermination_obstruction` | `rr_e_underdetermination_obstruction` |
| finite two-record `RR_E` witness/countermodel | `rr_e_separation_obstruction_witness_v1` |
| `RR_ETransportCompletenessOrInvarianceLaw_v1` | `rr_e_transport_completeness_or_invariance_law_v1` |
| finite toy metric-response frozen negative route | `finite_toy_metric_response` |
| Einstein equations open burden | `einstein_equations` |
| benchmark promotion blocked burden | `benchmark_promotion`; `gate_chair_benchmark_closure` |

P7-T02 population boundary: every row above is a control inventory row backed
by the cited source paths or registry rows. This population does not create new
theorem statements, source-law adoption, matter-semantics adoption,
matter-coupling derivation or adoption, Einstein equations, benchmark
promotion, or completed derivation.
'''


NEW_SOURCES = r'''
The AEther-Flow Research Project. (2026, June 30). *Matter-coupling
precondition assembly target v1* [Internal research-control TeX artifact].

The AEther-Flow Research Project. (2026, June 30). *Matter-coupling
precondition assembly source-extension evidence Gate Chair review v1*
[Internal research-control TeX artifact].

The AEther-Flow Research Project. (2026, June 30). *Source coupling law
candidate source-extension evidence Gate Chair review v1* [Internal
research-control TeX artifact].

The AEther-Flow Research Project. (2026, June 30). *MS stable partition
precondition source-extension evidence Gate Chair review v1* [Internal
research-control TeX artifact].

The AEther-Flow Research Project. (2026, June 30). *MS stable matter semantics
bridge source-extension evidence Gate Chair review v1* [Internal
research-control TeX artifact].

The AEther-Flow Research Project. (2026, July 1). *Source matter semantics
adoption-readiness law evidence Gate Chair review v1* [Internal
research-control TeX artifact].

The AEther-Flow Research Project. (2026, July 1). *Positive source
matter-semantics target v1* [Internal research-control TeX artifact].

The AEther-Flow Research Project. (2026, July 1). *Positive source
matter-semantics profile Gate Chair review v1* [Internal research-control TeX
artifact].
'''


def field_block(field: str, value: str) -> str:
    return f"- `{field}`: {value}\n"


def insert_before_anchor(section: str, anchor_field: str, fields: list[str], values: dict[str, str]) -> str:
    if not any(f"- `{f}`:" not in section for f in fields):
        return section
    anchor_match = re.search(rf"(?m)^- `{re.escape(anchor_field)}`:", section)
    if anchor_match is None:
        return section
    idx = anchor_match.start()
    block = ""
    for f in fields:
        if f"- `{f}`:" not in section:
            block += field_block(f, values[f])
    return section[:idx] + block + section[idx:]


def remove_top_level_field(section: str, field: str) -> str:
    return re.sub(rf"(?m)^- `{re.escape(field)}`:.*\n", "", section)


def remove_nested_field(section: str, field: str) -> str:
    return re.sub(rf"(?m)^  - `{re.escape(field)}`:.*\n", "", section)


def ensure_status_layer_overread(section: str) -> str:
    if re.search(r"(?m)^  - `overread_guard`:", section):
        return section
    top_level = re.search(r"(?m)^- `overread_guard`: (.*)$", section)
    if top_level is None:
        return section
    promotion = re.search(r"(?m)^  - `promotion_status`:.*\n", section)
    if promotion is None:
        return section
    guard_line = f"  - `overread_guard`: {top_level.group(1)}\n"
    return section[: promotion.end()] + guard_line + section[promotion.end() :]


def populate_existing_item(section: str) -> str:
    match = re.search(r"- `frontier_item_id`: `([^`]+)`", section)
    if not match:
        return section
    item_id = match.group(1)
    values = BASE_FIELD_VALUES.get(item_id)
    if not values:
        return section
    for misplaced_field in ("three_tier_classification", "linter_status"):
        section = remove_nested_field(section, misplaced_field)
        section = remove_top_level_field(section, misplaced_field)
    for anchor, fields in INSERT_ORDER:
        section = insert_before_anchor(section, anchor, fields, values)
    section = ensure_status_layer_overread(section)
    return section


def main() -> None:
    text = INVENTORY_PATH.read_text()

    if "P7-T02 v14 live-core population" not in text:
        text = text.replace(
            "- Synchronized by: `RT-20260701-031`, P5-T06 RR_E boundary update after\n"
            "  `handoff-0439`.\n",
            "- Synchronized by: `RT-20260701-031`, P5-T06 RR_E boundary update after\n"
            "  `handoff-0439`.\n"
            "- P7-T02 v14 live-core population: `RT-20260702-013`, adding explicit\n"
            "  v14 fields and separate tracked matter-semantics/precondition rows.\n",
        )

    body, tail = text.split("\n## Coverage Receipt\n", 1)
    body = body.rstrip()

    sections = re.split(r"(?=^### Item )", body, flags=re.M)
    rebuilt = [sections[0].rstrip()]
    for section in sections[1:]:
        rebuilt.append(populate_existing_item(section.rstrip()))
    body = "\n\n".join(rebuilt)

    if "### Item 10F: matter_coupling_precondition_assembly_v1" not in body:
        body = body.replace(
            "\n\n### Item 11: finite_toy_metric_response",
            "\n" + NEW_ITEMS.rstrip() + "\n\n### Item 11: finite_toy_metric_response",
        )

    text = body + "\n\n## Coverage Receipt\n" + tail

    text = text.replace(
        "Gate Chair adopted the accepted candidate only as a scoped source-extension `g_eff` object.",
        "Gate Chair decision accepted the candidate only as a scoped source-extension `g_eff` object.",
    )
    text = text.replace(
        "no_benchmark_gate_chair_closure;no_benchmark_promotion;no_completed_derivation",
        "no_benchmark_gate_chair_closure;no_benchmark_promotion;no_completed_derivation;no_future_source_extension_impossibility;no_global_theory_rejection",
    )

    if "P7-T02 live-core item coverage:" not in text:
        text = text.replace("\n## Source Materials\n", "\n" + P7_COVERAGE.rstrip() + "\n\n## Source Materials\n")

    if "Matter-coupling\nprecondition assembly source-extension evidence Gate Chair review v1" not in text:
        text = text.rstrip() + "\n\n" + NEW_SOURCES.strip() + "\n"

    INVENTORY_PATH.write_text(text)


if __name__ == "__main__":
    main()
