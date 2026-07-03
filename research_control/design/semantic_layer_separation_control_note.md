<!-- authority: control -->

# Semantic-Layer Separation Control Note

## Purpose

This note implements P4-T03 of
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`.
It is a source-backed control surface for keeping three matter-sector semantic
layers distinct:

1. `SourceMatterSemantics_src`
2. `DetectorSemantics_det`
3. `StressEnergyAction_sem`

The note is project-control guidance. It is not a theorem, not a source-law
adoption, not matter-semantics adoption, not detector-semantics adoption, not
stress-energy semantics, not a stress-energy tensor, not a matter action, not
matter-coupling derivation or adoption, not Einstein equations, not benchmark
promotion, and not a completed derivation.

## Authority Boundary

The control rule is:

```text
Source-side matter-semantics evidence may support later work only inside its
declared source and certificate scope. It must not be reused as detector,
readout, measurement, stress-energy, action, variational, coupling-law,
Einstein-equation, benchmark, or completed-derivation authority.
```

Tracked TeX artifacts, registered control Markdown, registries, task records,
AgentJobs, completions, handoffs, and approvals are the only source surfaces
used below. Generated wiki notes, local Obsidian notes, semantic extracts,
SQLite memory, PDFs, validator output, registry metadata, role identity,
handoff text, local cache freshness, file order, commit status, and checkpoint
status are support surfaces only. They do not promote scientific claims.

No-target certificates are hygiene only. They prevent forbidden imports and
process-authority laundering. They do not supply positive matter theory,
detector semantics, stress-energy semantics, a stress-energy tensor, a matter
action, a coupling law, matter coupling, Einstein equations, benchmark
authority, or completed-derivation authority.

## Source Inventory

| Source ID | Path | Registry | Object ID | Hash or ledger field | Authority use |
| --- | --- | --- | --- | --- | --- |
| `src_plan_v15` | `implementations_plans/recommendations_implementation_plan_continue_task-v15.md` | `MARKDOWN_SOURCE_REGISTRY.csv` | `MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V15` | `624f13305a1518a63b25c9b543f5fbf408b983fb3cf9c0b504475c5ef320e5ba` | P4-T03 layer list and done criteria. |
| `src_current_frontier` | `research_control/current_frontier.md` | `MARKDOWN_SOURCE_REGISTRY.csv` | `MD-RESEARCH-CONTROL-CURRENT-FRONTIER` | `cc47fa01235053056947461becf8968a6cce52c15e0245c32add55ceee63d1e0` | Active matter-coupling boundary and P4-T03 next-route state. |
| `src_handoff_0520` | `research_control/handoffs/handoff-0520.yaml` | `research_control/handoffs/` | `handoff-0520` | `e521c9b7f02faa4e82b54bdc4dbe92eb99a45371578835ec2c7a219944e42c20` | Immediate routing authority for this packet. |
| `src_dag_schema` | `research_control/design/matter_coupling_dependency_dag_schema_v1.md` | `MARKDOWN_SOURCE_REGISTRY.csv` | `MD-RESEARCH-CONTROL-DESIGN-MATTER-COUPLING-DEPENDENCY-DAG-SCHEMA-V1` | `7e63b792cc9d7effc7da57750d166724496cbd368d4399ab086f8634b6af4834` | Semantic-layer vocabulary and edge-kind separation contract. |
| `src_dag` | `research_control/design/matter_coupling_dependency_dag_v1.md` | `MARKDOWN_SOURCE_REGISTRY.csv` | `MD-RESEARCH-CONTROL-DESIGN-MATTER-COUPLING-DEPENDENCY-DAG-V1` | `8cca047480ae21c3b0641a5221277ae43cd5fdf1eb688a9080a168e27b1e98c3` | Populated nodes and exact missing burdens. |
| `src_no_target_map` | `research_control/design/no_target_import_guard_map.md` | `MARKDOWN_SOURCE_REGISTRY.csv` | `MD-RESEARCH-CONTROL-DESIGN-NO-TARGET-IMPORT-GUARD-MAP` | `4c4e736a84bb59ae11710fa185788e86bd6de6de3176f748b2689d9fcda755ce` | No-target and process-authority guard categories. |
| `src_certificate_checklist` | `research_control/design/source_certificate_algebra_checklist.md` | `MARKDOWN_SOURCE_REGISTRY.csv` | `MD-RESEARCH-CONTROL-DESIGN-SOURCE-CERTIFICATE-ALGEBRA-CHECKLIST` | `158dee6549b691b82d2e31a3d8df0caafe9d8e0ce8ef62dd2213800cc11f91fa` | Certificate-record requirements and linter-fixture precedent. |
| `src_moratorium` | `research_control/design/matter_coupling_derivation_moratorium.md` | `MARKDOWN_SOURCE_REGISTRY.csv` | `MD-RESEARCH-CONTROL-DESIGN-MATTER-COUPLING-DERIVATION-MORATORIUM` | `435e92ca1340c5b69fae97895ffe2b3fe203087384864d13be30fa0890370e0c` | Direct matter-coupling route blocks and narrower route permissions. |
| `src_pre_adoption` | `research_control/design/matter_coupling_pre_adoption_checklist.md` | `MARKDOWN_SOURCE_REGISTRY.csv` | `MD-RESEARCH-CONTROL-DESIGN-MATTER-COUPLING-PRE-ADOPTION-CHECKLIST` | `7586f1ea939eb508a451498d0f15225308fc98127803d58e81fa1adbfd3e9d60` | Adoption-facing missing-law and protected-authority checklist. |
| `src_distance_ledger` | `registries/DISTANCE_TO_GR_LEDGER.csv` | `DISTANCE_TO_GR_LEDGER.csv` | `matter_coupling` row and downstream rows | `0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61` | Layered matter-coupling physical-status and promotion-status boundaries. |
| `src_p2_manifest` | `research_control/tasks/RT-20260702-057/artifacts/source_side_matter_semantics_object_certificate_manifest_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V15-P2-T01-T02-SOURCE-SIDE-MATTER-SEMANTICS-OBJECT-CERTIFICATE-MANIFEST` | `81f8d552d04c942522bd7aab128a9bb65b4ab1a165c0c2e6468d8a877069c24d` | Source-side object, record, bridge, certificate, no-target, and fail-closed definitions. |
| `src_p2_theorem` | `research_control/tasks/RT-20260702-058/artifacts/narrow_source_side_matter_semantics_equivalence_theorem_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V15-P2-T03-NARROW-SOURCE-SIDE-MATTER-SEMANTICS-EQUIVALENCE-THEOREM` | `aca8af857f2a53bfcbdd775b147323dab9e8a814ec78409faace45eef61bc04b` | Conditional source-side theorem scope and non-equivalence statements. |
| `src_p2_audit` | `research_control/tasks/RT-20260702-059/artifacts/matter_semantics_equivalence_theorem_smuggling_audit_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V15-P2-T04-MATTER-SEMANTICS-EQUIVALENCE-THEOREM-SMUGGLING-AUDIT` | `3521b359ead752d615983aa942d6e93a302aeba6be8a882aed8dc5b513524820` | Hidden-import audit for target, detector, metric, stress-energy, matter-action, Einstein-equation, process-authority, and status laundering. |
| `src_p2_stress` | `research_control/tasks/RT-20260702-060/artifacts/matter_semantics_equivalence_theorem_refuter_stress_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V15-P2-T05-MATTER-SEMANTICS-EQUIVALENCE-THEOREM-REFUTER-STRESS` | `1be7ba5ac04095d7582612e0831fadcc55e58be0938ab25f2c7b7705da541182` | Certificate-gap witness and no-target certificate misuse result. |
| `src_gate_narrow_ms` | `research_control/tasks/RT-20260702-062/artifacts/narrow_ms_cert_eq_gate_chair_review_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V15-NARROW-MS-CERT-EQ-GATE-CHAIR-REVIEW` | `34e2f86e377edc3d13513d6f0a9e8d3083829bda230d32309177a82879770ca7` | Scoped evidence-status only for `NarrowMSCertEq_v1`. |
| `src_p3_primitives` | `research_control/tasks/RT-20260702-063/artifacts/source_certificate_algebra_primitives_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V15-P3-T01-SOURCE-CERTIFICATE-ALGEBRA-PRIMITIVES` | `43d20536f39682c42743739715534096c06d5e445ae269378bab9db95e73fa1e` | Draft/control certificate primitive vocabulary. |
| `src_p3_laws` | `research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex` | `TEX_SOURCE_REGISTRY.csv` | `TEX-V15-P3-T02-SOURCE-CERTIFICATE-OPERATION-LAWS` | `2ebc781bd82b4d39ab394255e5d3836d992625bdece8b8f912a8ab809669b986` | Draft/control operation-law and fail-closed certificate discipline. |

## Layer Definitions

### `SourceMatterSemantics_src`

`SourceMatterSemantics_src` contains source-side matter-semantics objects,
source records, source labels, response-token or source-readout families,
guard families, certificate bundles, declared source scopes, source
transport, source invariance, source factorization, certificate-indexed
source equivalence, fail-closed branches, and scoped source-extension
evidence/preconditions.

Allowed reuse:

- cite as source-side vocabulary or scoped evidence/precondition;
- cite as conditional theorem support only when explicit source certificates
  and no-target guards are present;
- cite `NarrowMSCertEq_v1` only as scoped evidence-status for its declared
  conditional source-side theorem role;
- cite certificate algebra primitives or operation laws only as draft/control
  source-certificate discipline;
- cite no-target certificates only as import-prevention hygiene;
- cite the populated DAG only to identify dependencies, blocked targets, and
  missing burdens; and
- route later lower-authority theorem, audit, stress, target-formalization, or
  linter-fixture packets.

Blocked reuse:

- do not reuse as adopted matter semantics unless a separate protected
  tracked authority adopts the exact object;
- do not reuse as detector, readout, measurement, empirical protocol, or
  observer semantics;
- do not reuse as stress-energy semantics, stress-energy tensor, matter
  action, or variational input;
- do not reuse as coupling-law adoption, matter-coupling derivation, or
  matter-coupling adoption;
- do not reuse scoped evidence/precondition status as source-law adoption,
  `RR_ETransportCompletenessOrInvarianceLaw_v1` adoption, unrestricted
  `RR_E` theorem authority, `PositiveMSProfile_v1` adoption, or
  `SourceMatterSemanticsAdoptionReadinessLaw_v1` law adoption;
- do not reuse as `MetricData(E)`, unscoped `g_eff`, Einstein-equation
  premise, benchmark fit, benchmark promotion, or completed derivation; and
- do not reuse registry, validator, role, handoff, approval, cache, file-order,
  or commit status as proof.

### `DetectorSemantics_det`

`DetectorSemantics_det` contains detector protocols, readout semantics,
measurement semantics, empirical calibration, observer-protocol semantics, and
any explicitly source-side replacement for those functions.

Allowed reuse:

- cite as a blocked downstream target;
- cite as a missing prerequisite for direct universal matter coupling;
- cite as an audit pressure category for hidden empirical import;
- cite as a future formalization target if a later bounded packet creates a
  source-side replacement without adoption; and
- cite only under tracked authority if a later protected decision establishes
  exact detector semantics or an exact replacement.

Blocked reuse:

- do not infer detector semantics from `SourceMatterSemantics_src`;
- do not treat source labels, source readouts, response tokens, or certificate
  scopes as measurement protocols;
- do not treat no-target certificate success as detector semantics;
- do not treat benchmark behavior, exact-GR resemblance, or empirical
  recovery language as detector semantics without a separate tracked route;
- do not treat detector semantics as a source certificate field or proof
  premise in `SourceMatterSemantics_src`; and
- do not reuse a detector-semantics target as matter coupling, stress-energy
  semantics, Einstein equations, benchmark promotion, or completed derivation.

### `StressEnergyAction_sem`

`StressEnergyAction_sem` contains stress-energy semantics, stress-energy
tensor construction, matter-action semantics, matter action, explicit
alternative dynamics paths, and variational input for field-equation work.

Allowed reuse:

- cite as a blocked downstream target;
- cite as a missing prerequisite for stress-energy tensor construction,
  matter action, Einstein-equation derivation, and benchmark promotion;
- cite as an audit pressure category for hidden dynamics or action import;
- cite as a future target-formalization route if the route is explicitly
  non-adoptive; and
- cite only under tracked authority if a later protected decision establishes
  exact stress-energy, action, or alternative dynamics content.

Blocked reuse:

- do not infer stress-energy semantics from `SourceMatterSemantics_src`;
- do not infer a stress-energy tensor from source-side equivalence, source
  certificate algebra, no-target hygiene, `M_src`, scoped `g_eff`, scoped
  evidence-status, or the matter-coupling DAG;
- do not infer a matter action or variational principle from a stress-energy
  target row unless a separate tracked authority establishes it;
- do not treat certificate composition, source restriction, or fail-closed
  branch behavior as dynamics;
- do not treat stress-energy/action targets as detector semantics or as a
  coupling law; and
- do not reuse stress-energy/action language as Einstein equations, benchmark
  promotion, or completed derivation.

## Separation Matrix

| From layer | To layer | Allowed relation | Blocked collapse |
| --- | --- | --- | --- |
| `SourceMatterSemantics_src` | `DetectorSemantics_det` | May name detector semantics as blocked target or hidden-import audit category. | Source-side objects, records, readouts, labels, response tokens, certificates, and theorem status may not be detector semantics. |
| `SourceMatterSemantics_src` | `StressEnergyAction_sem` | May name stress-energy/action as blocked downstream target or hidden-import audit category. | Source-side equivalence, certificate algebra, and no-target hygiene may not be stress-energy semantics, stress-energy tensor, matter action, or variational input. |
| `DetectorSemantics_det` | `StressEnergyAction_sem` | May both be prerequisites for later matter-sector or Einstein-equation work. | Detector/readout/measurement semantics may not be matter action, stress-energy tensor, or dynamics by naming alone. |
| `StressEnergyAction_sem` | `DetectorSemantics_det` | May both appear in a future adoption-facing checklist as separate missing semantics. | Stress-energy/action targets may not supply empirical detector protocol or readout semantics. |
| Any layer | Benchmark or completed derivation | May identify missing burden or protected authority. | No layer, validator, registry row, handoff, role, approval, or commit status may promote benchmark or completed-derivation status. |

## No-Target Certificate Hygiene Rule

No-target certificates answer a negative question:

```text
Does this packet avoid forbidden target, empirical, benchmark, generated,
registry, validator, role, handoff, local-cache, file-order, and commit-state
premises?
```

They do not answer the positive matter-sector questions:

- What is the adopted matter semantics?
- What is the detector/readout/measurement semantics?
- What is the coupling law?
- What is the stress-energy semantics?
- What stress-energy tensor is constructed?
- What matter action or alternative dynamics path is established?
- What variational input derives field equations?
- What benchmark authority promotes exact-GR recovery?

If a later packet uses a no-target certificate as a positive answer to any of
those questions, the branch must fail closed and route to a linter failure,
smuggling audit, Refuter stress, or lower-authority target-formalization
packet.

## Claim-Language Linter Fixture Proposal

P4-T04 may implement the following fixtures. This P4-T03 packet proposes them
without editing the linter.

Bad fixture phrases:

| Fixture ID | Bad phrase | Required result |
| --- | --- | --- |
| `semantic_layer_bad_source_as_detector` | source matter semantics as detector semantics | fail |
| `semantic_layer_bad_source_as_stress_energy` | source matter semantics as stress-energy | fail |
| `semantic_layer_bad_no_target_as_matter_theory` | no-target certificate as matter theory | fail |
| `semantic_layer_bad_rr_e_as_unrestricted_theorem` | RR_E transport evidence as unrestricted theorem | fail |
| `semantic_layer_bad_positive_profile_as_adoption` | PositiveMSProfile_v1 as matter-semantics adoption | fail |
| `semantic_layer_bad_geff_as_unscoped_metric` | g_eff as unscoped Lorentzian metric | fail |
| `semantic_layer_bad_evidence_as_coupling_law` | matter-sector evidence as coupling law | fail |
| `semantic_layer_bad_scoped_evidence_as_einstein_premise` | scoped evidence as Einstein-equation premise | fail |
| `semantic_layer_bad_certificate_as_detector_protocol` | source certificate supplies detector protocol | fail |
| `semantic_layer_bad_stress_target_as_action` | stress-energy target supplies matter action | fail |

Passing fixture phrases:

| Fixture ID | Passing phrase | Required result |
| --- | --- | --- |
| `semantic_layer_pass_source_scope` | source-side matter-semantics evidence remains inside declared source certificate scope | pass |
| `semantic_layer_pass_detector_blocked` | detector semantics remain blocked unless separately derived or adopted by tracked authority | pass |
| `semantic_layer_pass_stress_action_blocked` | stress-energy semantics and matter action remain blocked unless separately derived or adopted by tracked authority | pass |
| `semantic_layer_pass_no_target_hygiene` | no-target certificates are hygiene only and do not supply positive matter theory | pass |
| `semantic_layer_pass_scoped_evidence` | scoped evidence/precondition status supports later work without adopting matter semantics or coupling law | pass |

## Machine-Readable Control Summary

```yaml
semantic_layer_separation_control_note:
  schema_id: "semantic_layer_separation_control_note_v1"
  plan_task_id: "v15_p4_t03"
  authority_status: "project_control"
  physics_promotion_authorized: false
  proof_authority: false
  layers:
    SourceMatterSemantics_src:
      allowed_reuse:
        - "source-side vocabulary"
        - "scoped evidence/precondition"
        - "conditional theorem support under explicit certificates"
        - "draft/control certificate discipline"
        - "no-target hygiene"
      blocked_reuse:
        - "adopted matter semantics"
        - "detector semantics"
        - "stress-energy semantics"
        - "stress-energy tensor"
        - "matter action"
        - "coupling-law adoption"
        - "matter-coupling derivation or adoption"
        - "Einstein equations"
        - "benchmark promotion"
        - "completed derivation"
    DetectorSemantics_det:
      allowed_reuse:
        - "blocked downstream target"
        - "missing prerequisite"
        - "hidden-import audit category"
      blocked_reuse:
        - "inference from source-side matter-semantics evidence"
        - "inference from no-target hygiene"
        - "source certificate field or premise"
        - "matter coupling"
        - "stress-energy/action"
        - "Einstein equations"
    StressEnergyAction_sem:
      allowed_reuse:
        - "blocked downstream target"
        - "missing prerequisite"
        - "hidden dynamics or action import audit category"
      blocked_reuse:
        - "inference from source-side matter-semantics evidence"
        - "inference from source certificate algebra"
        - "inference from no-target hygiene"
        - "detector semantics"
        - "coupling law"
        - "Einstein equations"
  no_target_certificates:
    hygiene_only: true
    positive_matter_theory: false
    detector_semantics: false
    stress_energy_semantics: false
    matter_action: false
    coupling_law: false
    matter_coupling: false
    einstein_equations: false
    benchmark_promotion: false
  linter_fixtures:
    status: "proposed"
    next_plan_task_id: "P4-T04"
```

## P4-T03 Completion Criteria

This P4-T03 packet may claim only that:

- the semantic-layer separation control note exists;
- each required layer lists allowed reuse and blocked reuse;
- no-target certificates are explicitly recorded as hygiene only;
- semantic-layer claim-language linter fixtures are proposed for P4-T04; and
- P4-T04 may implement linter fixtures in a later bounded transaction.

It may not claim any source-law adoption, matter-semantics adoption,
detector-semantics adoption, coupling-law adoption, matter-coupling derivation
or adoption, stress-energy semantics, stress-energy tensor, matter action,
Einstein equations, benchmark promotion, or completed derivation.

## Source Materials

The AEther-Flow Research Project. (2026, July 2). *Recommendations
implementation plan continue task v15* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`

The AEther-Flow Research Project. (2026, July 3). *Matter-coupling dependency
DAG v1* [Internal control source].
`research_control/design/matter_coupling_dependency_dag_v1.md`

The AEther-Flow Research Project. (2026, July 2). *Matter-coupling dependency
DAG schema v1* [Internal control source].
`research_control/design/matter_coupling_dependency_dag_schema_v1.md`

The AEther-Flow Research Project. (2026, July 2). *Source-side
matter-semantics object certificate manifest v1* [Research-control TeX
artifact].
`research_control/tasks/RT-20260702-057/artifacts/source_side_matter_semantics_object_certificate_manifest_v1.tex`

The AEther-Flow Research Project. (2026, July 2). *Narrow source-side
matter-semantics equivalence theorem v1* [Research-control TeX artifact].
`research_control/tasks/RT-20260702-058/artifacts/narrow_source_side_matter_semantics_equivalence_theorem_v1.tex`

The AEther-Flow Research Project. (2026, July 2). *Source certificate
operation laws v1* [Research-control TeX artifact].
`research_control/tasks/RT-20260702-064/artifacts/source_certificate_operation_laws_v1.tex`
