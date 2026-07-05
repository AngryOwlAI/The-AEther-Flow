<!-- authority: control -->

# Source Model Zoo v1

## Status

This source model zoo implements v16 P10-T02. It instantiates eight
finite/local source models using `source_model_zoo_schema_v1`.

The zoo is a draft/control fixture library. It is not a source law, not an
unrestricted `RR_E` theorem, not detector semantics, not matter semantics, not
stress-energy semantics, not a matter action, not matter coupling, not
Einstein equations, not benchmark promotion, and not a completed derivation.

## Source Basis

- Schema: `research_control/design/source_model_zoo_schema_v1.md`.
- Certificate schema:
  `research_control/design/source_certificate_instance_library_schema_v1.md`.
- Certificate index:
  `research_control/design/source_certificate_instance_library_index_v1.md`.
- Positive P4 instances:
  `SCI-TRANSPORT-001`, `SCI-INVARIANCE-001`, and
  `SCI-FACTORIZATION-001`.
- Negative P4 packet:
  `SCI-NEG-MISSING-001`, `SCI-NEG-MALFORMED-001`,
  `SCI-NEG-FACTOR-CHANGE-001`, `SCI-NEG-TARGET-METRIC-001`,
  `SCI-NEG-DETECTOR-001`, `SCI-NEG-STRESS-ENERGY-001`,
  `SCI-NEG-VALIDATOR-PASS-001`, and `SCI-NEG-SCOPED-EVIDENCE-001`.

Generated wiki notes, validator output, registry status, role identity,
handoff state, approval state, commits, and local caches are not source model
data.

## Model Inventory

| Model ID | Model kind | Source-domain size | Positive certificate links | Negative/refuter links | Expected valid relation | Expected fail-closed relation |
| --- | --- | ---: | --- | --- | --- | --- |
| `SMZ-IDENTITY-001` | `trivial_identity_model` | 1 object, 2 local records | none | `SCI-NEG-VALIDATOR-PASS-001` as process-overread guard | identity relation on declared source object | validator-as-proof rejected |
| `SMZ-TRANSPORT-001` | `transportable_two_object_model` | 2 objects, 3 carrier elements | `SCI-TRANSPORT-001` | `SCI-NEG-MALFORMED-001` as malformed transport guard | declared finite transport allowed | malformed map blocks relation |
| `SMZ-RELABEL-001` | `invariant_relabeling_model` | 2 relabeled objects, 3 carrier elements | `SCI-INVARIANCE-001` | `SCI-NEG-DETECTOR-001` as detector-semantics guard | declared relabeling invariance allowed | detector semantics cannot justify invariance |
| `SMZ-FACTOR-001` | `factorization_through_source_object_model` | 3 objects including middle factor | `SCI-FACTORIZATION-001` | `SCI-NEG-FACTOR-CHANGE-001` | declared factorization allowed | changed factor object blocks relation |
| `SMZ-GAP-001` | `certificate_gap_model` | 1 object, absent codomain slot | none | `SCI-NEG-MISSING-001`, `SCI-NEG-MALFORMED-001` | none | missing or malformed certificate blocks relation |
| `SMZ-RRE-SEP-001` | `rr_e_separated_model` | 2 objects, 2 relation records | none | `SCI-NEG-SCOPED-EVIDENCE-001` plus local obstruction `OB-SMZ-RRE-SEP-001` | none | local separation preserved without unrestricted `RR_E` |
| `SMZ-TARGET-REJECT-001` | `target_import_rejection_model` | 2 objects, 2 carrier elements | none | `SCI-NEG-TARGET-METRIC-001`, `SCI-NEG-STRESS-ENERGY-001` | none | target metric or stress-energy import rejected |
| `SMZ-DETECTOR-REJECT-001` | `detector_semantics_collapse_rejection_model` | 2 objects, 2 response tokens | none | `SCI-NEG-DETECTOR-001` | none | detector-semantics collapse rejected |

Positive certificate mapped models: `SMZ-TRANSPORT-001`,
`SMZ-RELABEL-001`, and `SMZ-FACTOR-001`. Negative/refuter mapped models:
`SMZ-GAP-001`, `SMZ-RRE-SEP-001`, `SMZ-TARGET-REJECT-001`, and
`SMZ-DETECTOR-REJECT-001`, with additional process-overread guards on
`SMZ-IDENTITY-001`.

## Model Records

### SMZ-IDENTITY-001

```yaml
model_id: "SMZ-IDENTITY-001"
model_kind: "trivial_identity_model"
source_domain:
  domain_id: "SD-SMZ-IDENTITY-001"
  finite: true
  carrier: ["i0", "i1"]
source_objects:
  - object_id: "ID_src"
    local_carrier: ["i0", "i1"]
    source_labels: ["id_label"]
    source_guards: ["guard_identity_scope_declared"]
source_labels: ["id_label"]
source_guards: ["guard_identity_scope_declared"]
response_tokens: ["resp_id_0", "resp_id_1"]
certificate_instances:
  allowed: []
  blocked:
    - "SCI-NEG-VALIDATOR-PASS-001"
rr_e_records:
  - relation_id: "RR-SMZ-IDENTITY-LOCAL"
    source_pair: ["ID_src", "ID_src"]
    relation_status: "declared_equivalence_allowed"
    scope: "identity bookkeeping inside SD-SMZ-IDENTITY-001"
target_import_status: "not_used"
detector_semantics_status: "not_used"
stress_energy_status: "not_used"
matter_action_status: "not_used"
benchmark_status: "not_claimed"
expected_valid_relations:
  - "local identity relation on ID_src"
expected_fail_closed_relations:
  - "validator-pass-as-proof is rejected through SCI-NEG-VALIDATOR-PASS-001"
source_paths:
  - "research_control/design/source_model_zoo_schema_v1.md"
  - "research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex"
allowed_reuse:
  - "support-only identity fixture for P10 validation"
  - "baseline fixture for compact frontier examples"
forbidden_overreads:
  - "identity bookkeeping as source-law adoption"
  - "validator status as proof authority"
  - "identity fixture as matter coupling"
```

Summary fields required by the plan:

| Required item | Value |
| --- | --- |
| Model definition | One object `ID_src` with local identity relation over `{i0,i1}`. |
| Finite object table | `ID_src`: carrier `{i0,i1}`, label `id_label`, guard `guard_identity_scope_declared`. |
| Allowed certificates | none required. |
| Blocked certificates | `SCI-NEG-VALIDATOR-PASS-001`. |
| Expected theorem result | Identity relation is allowed only as declared local bookkeeping. |
| Expected fail-closed result | Process authority cannot create proof authority. |
| Relation to P4 certificate instances | Uses the negative process-authority guard from P4. |
| Forbidden overreads | No source law, no proof authority, no matter coupling, no benchmark. |

### SMZ-TRANSPORT-001

```yaml
model_id: "SMZ-TRANSPORT-001"
model_kind: "transportable_two_object_model"
source_domain:
  domain_id: "SD-SMZ-TRANSPORT-001"
  finite: true
  carrier: ["0", "1", "2"]
source_objects:
  - object_id: "A_src"
    local_carrier: ["0", "1", "2"]
    source_labels: ["L0", "L1", "L2"]
    source_guards: ["guard_transport_domain"]
  - object_id: "B_src"
    local_carrier: ["0p", "1p", "2p"]
    source_labels: ["L0p", "L1p", "L2p"]
    source_guards: ["guard_transport_codomain"]
source_labels: ["L0", "L1", "L2", "L0p", "L1p", "L2p"]
source_guards: ["guard_transport_domain", "guard_transport_codomain", "guard_transport_map_total"]
response_tokens: ["resp_transport_0", "resp_transport_1", "resp_transport_2"]
certificate_instances:
  allowed:
    - "SCI-TRANSPORT-001"
  blocked:
    - "SCI-NEG-MALFORMED-001"
rr_e_records:
  - relation_id: "RR-SMZ-TRANSPORT-DECLARED"
    source_pair: ["A_src", "B_src"]
    relation_status: "declared_equivalence_allowed"
    scope: "SCI-TRANSPORT-001 finite transport witness only"
target_import_status: "not_used"
detector_semantics_status: "not_used"
stress_energy_status: "not_used"
matter_action_status: "not_used"
benchmark_status: "not_claimed"
expected_valid_relations:
  - "declared A_src to B_src transport allowed under SCI-TRANSPORT-001"
expected_fail_closed_relations:
  - "malformed transport candidate blocks relation through SCI-NEG-MALFORMED-001"
source_paths:
  - "research_control/tasks/RT-20260704-026/artifacts/finite_local_transport_certificate_instance_v1.tex"
  - "research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex"
allowed_reuse:
  - "finite/local positive transport fixture"
  - "target-import attack baseline with source-pure positive control"
forbidden_overreads:
  - "transport witness as source-law adoption"
  - "transport witness as unrestricted RR_E"
  - "transport witness as matter coupling"
```

| Required item | Value |
| --- | --- |
| Model definition | Two source objects linked by the finite transport witness in `SCI-TRANSPORT-001`. |
| Finite object table | `A_src`: `{0,1,2}`; `B_src`: `{0p,1p,2p}`. |
| Allowed certificates | `SCI-TRANSPORT-001`. |
| Blocked certificates | `SCI-NEG-MALFORMED-001`. |
| Expected theorem result | Declared equivalence allowed only inside the finite transport scope. |
| Expected fail-closed result | Malformed candidate leaving codomain blocks transport. |
| Relation to P4 certificate instances | Positive P4 transport instance plus malformed negative guard. |
| Forbidden overreads | No source-law adoption, unrestricted `RR_E`, matter coupling, or benchmark. |

### SMZ-RELABEL-001

```yaml
model_id: "SMZ-RELABEL-001"
model_kind: "invariant_relabeling_model"
source_domain:
  domain_id: "SD-SMZ-RELABEL-001"
  finite: true
  carrier: ["0", "1", "2"]
source_objects:
  - object_id: "A_src"
    local_carrier: ["0", "1", "2"]
    source_labels: ["q0", "q1", "q2"]
    source_guards: ["guard_cycle_domain"]
  - object_id: "A_src_sigma"
    local_carrier: ["1", "2", "0"]
    source_labels: ["q1", "q2", "q0"]
    source_guards: ["guard_cycle_codomain"]
source_labels: ["q0", "q1", "q2"]
source_guards: ["guard_cycle_domain", "guard_cycle_codomain", "guard_relabeling_bijection"]
response_tokens: ["resp_cycle_0", "resp_cycle_1", "resp_cycle_2"]
certificate_instances:
  allowed:
    - "SCI-INVARIANCE-001"
  blocked:
    - "SCI-NEG-DETECTOR-001"
rr_e_records:
  - relation_id: "RR-SMZ-RELABEL-DECLARED"
    source_pair: ["A_src", "A_src_sigma"]
    relation_status: "declared_equivalence_allowed"
    scope: "SCI-INVARIANCE-001 cyclic relabeling only"
target_import_status: "not_used"
detector_semantics_status: "not_used"
stress_energy_status: "not_used"
matter_action_status: "not_used"
benchmark_status: "not_claimed"
expected_valid_relations:
  - "declared source relabeling invariance under SCI-INVARIANCE-001"
expected_fail_closed_relations:
  - "detector-event sameness cannot justify source relabeling"
source_paths:
  - "research_control/tasks/RT-20260704-027/artifacts/finite_local_invariance_certificate_instance_v1.tex"
  - "research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex"
allowed_reuse:
  - "finite/local relabeling fixture"
  - "detector-semantics collapse contrast fixture"
forbidden_overreads:
  - "source relabeling as detector invariance"
  - "source relabeling as empirical invariance"
  - "source relabeling as benchmark recovery"
```

| Required item | Value |
| --- | --- |
| Model definition | Source object and cyclic relabeling partner over `{0,1,2}`. |
| Finite object table | `A_src`: labels `{q0,q1,q2}`; `A_src_sigma`: labels `{q1,q2,q0}`. |
| Allowed certificates | `SCI-INVARIANCE-001`. |
| Blocked certificates | `SCI-NEG-DETECTOR-001`. |
| Expected theorem result | Declared relabeling equivalence allowed inside source-label scope. |
| Expected fail-closed result | Detector-semantics import cannot justify invariance. |
| Relation to P4 certificate instances | Positive P4 invariance instance plus detector negative guard. |
| Forbidden overreads | No detector invariance, empirical invariance, matter coupling, or benchmark. |

### SMZ-FACTOR-001

```yaml
model_id: "SMZ-FACTOR-001"
model_kind: "factorization_through_source_object_model"
source_domain:
  domain_id: "SD-SMZ-FACTOR-001"
  finite: true
  carrier: ["a0", "a1", "a2", "b0", "b1", "alpha", "beta"]
source_objects:
  - object_id: "A_src"
    local_carrier: ["a0", "a1", "a2"]
    source_labels: ["A0", "A1", "A2"]
    source_guards: ["guard_factor_domain"]
  - object_id: "F_src"
    local_carrier: ["alpha", "beta"]
    source_labels: ["F_alpha", "F_beta"]
    source_guards: ["guard_middle_factor"]
  - object_id: "B_src"
    local_carrier: ["b0", "b1"]
    source_labels: ["B0", "B1"]
    source_guards: ["guard_factor_codomain"]
source_labels: ["A0", "A1", "A2", "F_alpha", "F_beta", "B0", "B1"]
source_guards: ["guard_factor_domain", "guard_middle_factor", "guard_factor_codomain"]
response_tokens: ["resp_factor_a0", "resp_factor_a1", "resp_factor_a2"]
certificate_instances:
  allowed:
    - "SCI-FACTORIZATION-001"
  blocked:
    - "SCI-NEG-FACTOR-CHANGE-001"
rr_e_records:
  - relation_id: "RR-SMZ-FACTOR-DECLARED"
    source_pair: ["A_src", "B_src"]
    relation_status: "declared_equivalence_allowed"
    scope: "SCI-FACTORIZATION-001 through F_src only"
target_import_status: "not_used"
detector_semantics_status: "not_used"
stress_energy_status: "not_used"
matter_action_status: "not_used"
benchmark_status: "not_claimed"
expected_valid_relations:
  - "declared factorization relation through F_src allowed"
expected_fail_closed_relations:
  - "changed factor object blocks relation through SCI-NEG-FACTOR-CHANGE-001"
source_paths:
  - "research_control/tasks/RT-20260705-001/artifacts/finite_local_factorization_certificate_instance_v1.tex"
  - "research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex"
allowed_reuse:
  - "finite/local factorization fixture"
  - "factor-object identity stress fixture"
forbidden_overreads:
  - "factorization as global RR_E collapse"
  - "factorization as coupling-law adoption"
  - "factorization as matter coupling"
```

| Required item | Value |
| --- | --- |
| Model definition | `A_src` factors through `F_src` to `B_src` inside declared finite support. |
| Finite object table | `A_src`: `{a0,a1,a2}`; `F_src`: `{alpha,beta}`; `B_src`: `{b0,b1}`. |
| Allowed certificates | `SCI-FACTORIZATION-001`. |
| Blocked certificates | `SCI-NEG-FACTOR-CHANGE-001`. |
| Expected theorem result | Declared factorization relation allowed only through the named `F_src`. |
| Expected fail-closed result | Changing the middle factor object blocks the relation. |
| Relation to P4 certificate instances | Positive P4 factorization instance plus factor-change negative guard. |
| Forbidden overreads | No global `RR_E` collapse, coupling law, matter coupling, or benchmark. |

### SMZ-GAP-001

```yaml
model_id: "SMZ-GAP-001"
model_kind: "certificate_gap_model"
source_domain:
  domain_id: "SD-SMZ-GAP-001"
  finite: true
  carrier: ["g0", "g1"]
source_objects:
  - object_id: "G_src"
    local_carrier: ["g0", "g1"]
    source_labels: ["G0", "G1"]
    source_guards: ["guard_gap_domain"]
source_labels: ["G0", "G1"]
source_guards: ["guard_gap_domain", "guard_certificate_required"]
response_tokens: ["resp_gap_0", "resp_gap_1"]
certificate_instances:
  allowed: []
  blocked:
    - "SCI-NEG-MISSING-001"
    - "SCI-NEG-MALFORMED-001"
rr_e_records:
  - relation_id: "RR-SMZ-GAP-BLOCKED"
    source_pair: ["G_src", null]
    relation_status: "declared_equivalence_blocked"
    scope: "missing or malformed certificate branch only"
target_import_status: "not_used"
detector_semantics_status: "not_used"
stress_energy_status: "not_used"
matter_action_status: "not_used"
benchmark_status: "blocked"
expected_valid_relations: []
expected_fail_closed_relations:
  - "missing certificate payload blocks relation"
  - "malformed certificate blocks relation"
source_paths:
  - "research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex"
allowed_reuse:
  - "fail-closed certificate-gap fixture"
  - "negative-result reader-language support"
forbidden_overreads:
  - "certificate gap as global no-go theorem"
  - "certificate gap as source-extension impossibility"
  - "certificate gap as benchmark failure proof"
```

| Required item | Value |
| --- | --- |
| Model definition | One source object with absent or malformed certificate path. |
| Finite object table | `G_src`: carrier `{g0,g1}`, labels `{G0,G1}`. |
| Allowed certificates | none. |
| Blocked certificates | `SCI-NEG-MISSING-001`, `SCI-NEG-MALFORMED-001`. |
| Expected theorem result | No positive theorem result. |
| Expected fail-closed result | Missing or malformed certificate blocks declared equivalence. |
| Relation to P4 certificate instances | Uses P4 negative missing and malformed instances. |
| Forbidden overreads | No global no-go theorem, no source-extension impossibility, no benchmark proof. |

### SMZ-RRE-SEP-001

```yaml
model_id: "SMZ-RRE-SEP-001"
model_kind: "rr_e_separated_model"
source_domain:
  domain_id: "SD-SMZ-RRE-SEP-001"
  finite: true
  carrier: ["r0", "r1"]
source_objects:
  - object_id: "R_src_left"
    local_carrier: ["r0"]
    source_labels: ["R_left"]
    source_guards: ["guard_rre_left"]
  - object_id: "R_src_right"
    local_carrier: ["r1"]
    source_labels: ["R_right"]
    source_guards: ["guard_rre_right"]
source_labels: ["R_left", "R_right"]
source_guards: ["guard_rre_left", "guard_rre_right", "guard_no_certificate_no_identification"]
response_tokens: ["resp_rre_left", "resp_rre_right"]
certificate_instances:
  allowed: []
  blocked:
    - "SCI-NEG-SCOPED-EVIDENCE-001"
rr_e_records:
  - relation_id: "RR-SMZ-RRE-SEPARATED"
    source_pair: ["R_src_left", "R_src_right"]
    relation_status: "does_not_identify"
    scope: "local separation with no certificate witness"
  - relation_id: "OB-SMZ-RRE-SEP-001"
    source_pair: ["R_src_left", "R_src_right"]
    relation_status: "obstruction_recorded"
    scope: "scoped evidence cannot be expanded into adoption"
target_import_status: "not_used"
detector_semantics_status: "not_used"
stress_energy_status: "not_used"
matter_action_status: "not_used"
benchmark_status: "blocked"
expected_valid_relations: []
expected_fail_closed_relations:
  - "local separation persists without an explicit certificate"
  - "scoped evidence cannot be converted into unrestricted adoption"
source_paths:
  - "research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex"
allowed_reuse:
  - "local separation fixture"
  - "negative/refuter model for unrestricted RR_E overread tests"
forbidden_overreads:
  - "local separation as unrestricted RR_E theorem"
  - "local separation as unrestricted negative conclusion"
  - "local separation as matter-coupling obstruction for all future routes"
```

| Required item | Value |
| --- | --- |
| Model definition | Two source objects remain locally separated without certificate witness. |
| Finite object table | `R_src_left`: `{r0}`; `R_src_right`: `{r1}`. |
| Allowed certificates | none. |
| Blocked certificates | `SCI-NEG-SCOPED-EVIDENCE-001`; local obstruction `OB-SMZ-RRE-SEP-001`. |
| Expected theorem result | No positive theorem result. |
| Expected fail-closed result | Local separation persists and scope expansion is blocked. |
| Relation to P4 certificate instances | Uses P4 scoped-evidence adoption rejection as authority guard. |
| Forbidden overreads | No unrestricted `RR_E`, no global rejection, no universal obstruction. |

### SMZ-TARGET-REJECT-001

```yaml
model_id: "SMZ-TARGET-REJECT-001"
model_kind: "target_import_rejection_model"
source_domain:
  domain_id: "SD-SMZ-TARGET-REJECT-001"
  finite: true
  carrier: ["t0", "t1"]
source_objects:
  - object_id: "T_src_A"
    local_carrier: ["t0"]
    source_labels: ["T_A"]
    source_guards: ["guard_target_reject_A"]
  - object_id: "T_src_B"
    local_carrier: ["t1"]
    source_labels: ["T_B"]
    source_guards: ["guard_target_reject_B"]
source_labels: ["T_A", "T_B"]
source_guards: ["guard_no_target_metric", "guard_no_stress_energy_shortcut"]
response_tokens: ["resp_target_A", "resp_target_B"]
certificate_instances:
  allowed: []
  blocked:
    - "SCI-NEG-TARGET-METRIC-001"
    - "SCI-NEG-STRESS-ENERGY-001"
rr_e_records:
  - relation_id: "RR-SMZ-TARGET-IMPORT-BLOCKED"
    source_pair: ["T_src_A", "T_src_B"]
    relation_status: "declared_equivalence_blocked"
    scope: "target metric or stress-energy shortcut rejected"
target_import_status: "attempted_rejected"
detector_semantics_status: "not_used"
stress_energy_status: "attempted_rejected"
matter_action_status: "not_used"
benchmark_status: "blocked"
expected_valid_relations: []
expected_fail_closed_relations:
  - "target metric import rejected"
  - "stress-energy shortcut rejected"
source_paths:
  - "research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex"
allowed_reuse:
  - "target-import attack-suite seed"
  - "negative/refuter model for source-purity tests"
forbidden_overreads:
  - "target metric as source data"
  - "stress-energy as source certificate"
  - "rejection as global no-go theorem"
```

| Required item | Value |
| --- | --- |
| Model definition | Two source objects with attempted target metric or stress-energy import rejected. |
| Finite object table | `T_src_A`: `{t0}`; `T_src_B`: `{t1}`. |
| Allowed certificates | none. |
| Blocked certificates | `SCI-NEG-TARGET-METRIC-001`, `SCI-NEG-STRESS-ENERGY-001`. |
| Expected theorem result | No positive theorem result. |
| Expected fail-closed result | Target metric and stress-energy shortcuts are rejected. |
| Relation to P4 certificate instances | Uses P4 target-import and stress-energy negative instances. |
| Forbidden overreads | No target metric as source data, no stress-energy shortcut, no global no-go. |

### SMZ-DETECTOR-REJECT-001

```yaml
model_id: "SMZ-DETECTOR-REJECT-001"
model_kind: "detector_semantics_collapse_rejection_model"
source_domain:
  domain_id: "SD-SMZ-DETECTOR-REJECT-001"
  finite: true
  carrier: ["d0", "d1"]
source_objects:
  - object_id: "D_src_A"
    local_carrier: ["d0"]
    source_labels: ["D_A"]
    source_guards: ["guard_detector_reject_A"]
  - object_id: "D_src_B"
    local_carrier: ["d1"]
    source_labels: ["D_B"]
    source_guards: ["guard_detector_reject_B"]
source_labels: ["D_A", "D_B"]
source_guards: ["guard_no_detector_semantics", "guard_no_detector_collapse"]
response_tokens: ["resp_detector_A", "resp_detector_B"]
certificate_instances:
  allowed: []
  blocked:
    - "SCI-NEG-DETECTOR-001"
rr_e_records:
  - relation_id: "RR-SMZ-DETECTOR-COLLAPSE-BLOCKED"
    source_pair: ["D_src_A", "D_src_B"]
    relation_status: "declared_equivalence_blocked"
    scope: "detector semantics cannot collapse source distinctions"
target_import_status: "not_used"
detector_semantics_status: "attempted_rejected"
stress_energy_status: "not_used"
matter_action_status: "not_used"
benchmark_status: "blocked"
expected_valid_relations: []
expected_fail_closed_relations:
  - "detector-event sameness import rejected"
  - "detector-semantics collapse cannot supply source certificate"
source_paths:
  - "research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex"
allowed_reuse:
  - "detector-semantics attack-suite seed"
  - "reader-facing negative result fixture"
forbidden_overreads:
  - "detector event sameness as source equivalence"
  - "detector semantics as matter semantics"
  - "detector rejection as benchmark status"
```

| Required item | Value |
| --- | --- |
| Model definition | Two source objects with attempted detector-semantics collapse rejected. |
| Finite object table | `D_src_A`: `{d0}`; `D_src_B`: `{d1}`. |
| Allowed certificates | none. |
| Blocked certificates | `SCI-NEG-DETECTOR-001`. |
| Expected theorem result | No positive theorem result. |
| Expected fail-closed result | Detector semantics cannot collapse source distinctions. |
| Relation to P4 certificate instances | Uses P4 detector-semantics negative instance. |
| Forbidden overreads | No detector event sameness as source equivalence, no matter semantics, no benchmark. |

## Machine-Readable Summary

```yaml
zoo_id: "source_model_zoo_v1"
implemented_plan_task: "P10-T02"
schema_source: "research_control/design/source_model_zoo_schema_v1.md"
model_count: 8
all_models_finite_or_local: true
models:
  - "SMZ-IDENTITY-001"
  - "SMZ-TRANSPORT-001"
  - "SMZ-RELABEL-001"
  - "SMZ-FACTOR-001"
  - "SMZ-GAP-001"
  - "SMZ-RRE-SEP-001"
  - "SMZ-TARGET-REJECT-001"
  - "SMZ-DETECTOR-REJECT-001"
positive_certificate_model_count: 3
negative_or_refuter_model_count: 5
positive_certificate_instances_used:
  - "SCI-TRANSPORT-001"
  - "SCI-INVARIANCE-001"
  - "SCI-FACTORIZATION-001"
negative_certificate_instances_used:
  - "SCI-NEG-MISSING-001"
  - "SCI-NEG-MALFORMED-001"
  - "SCI-NEG-FACTOR-CHANGE-001"
  - "SCI-NEG-TARGET-METRIC-001"
  - "SCI-NEG-DETECTOR-001"
  - "SCI-NEG-STRESS-ENERGY-001"
  - "SCI-NEG-VALIDATOR-PASS-001"
  - "SCI-NEG-SCOPED-EVIDENCE-001"
target_import_as_source_data: false
detector_semantics_as_source_data: false
stress_energy_as_source_data: false
matter_action_as_source_data: false
benchmark_behavior_as_source_data: false
physics_promotion_authorized: false
proof_authority: false
upstream_primitive_trigger_status:
  EqSrc:
    triggered: false
    reason: "P10-T02 constructs finite/local models with explicit certificate and obstruction records; it does not remove certificate premises or claim record-independent equivalence."
  RetainH:
    triggered: false
    reason: "P10-T02 does not claim H-indexed retention or matter-sector continuity under H."
  GenH:
    triggered: false
    reason: "P10-T02 does not construct an H-indexed generated family or use generator closure as theorem input."
blocked_authority:
  - source_law_adoption
  - EqSrc_discharge
  - RetainH_adoption
  - GenH_adoption
  - unrestricted_RR_E_theorem
  - matter_semantics_adoption
  - detector_semantics_adoption
  - coupling_law_adoption
  - matter_coupling_derivation_or_adoption
  - stress_energy_semantics
  - matter_action
  - Einstein_equations
  - benchmark_promotion
  - completed_derivation
```

## Done-Criteria Receipt

- Eight finite/local source models are defined.
- Each model has explicit finite data.
- Three models map to positive P4 certificate instances:
  `SMZ-TRANSPORT-001`, `SMZ-RELABEL-001`, and `SMZ-FACTOR-001`.
- Five models map to negative, refuter, or fail-closed instances:
  `SMZ-IDENTITY-001`, `SMZ-GAP-001`, `SMZ-RRE-SEP-001`,
  `SMZ-TARGET-REJECT-001`, and `SMZ-DETECTOR-REJECT-001`.
- No model imports target metric, detector semantics, stress-energy, matter
  action, or benchmark behavior as source data.
- No physics promotion is made.

## References

The Aether-Flow Research Project. (2026). `research_control/design/source_model_zoo_schema_v1.md` [Internal project-control schema].

The Aether-Flow Research Project. (2026). `research_control/design/source_certificate_instance_library_index_v1.md` [Internal project-control index].

The Aether-Flow Research Project. (2026). `research_control/tasks/RT-20260704-026/artifacts/finite_local_transport_certificate_instance_v1.tex` [Internal draft/control certificate instance].

The Aether-Flow Research Project. (2026). `research_control/tasks/RT-20260704-027/artifacts/finite_local_invariance_certificate_instance_v1.tex` [Internal draft/control certificate instance].

The Aether-Flow Research Project. (2026). `research_control/tasks/RT-20260705-001/artifacts/finite_local_factorization_certificate_instance_v1.tex` [Internal draft/control certificate instance].

The Aether-Flow Research Project. (2026). `research_control/tasks/RT-20260705-002/artifacts/negative_certificate_instance_packet_v1.tex` [Internal draft/control negative certificate packet].
