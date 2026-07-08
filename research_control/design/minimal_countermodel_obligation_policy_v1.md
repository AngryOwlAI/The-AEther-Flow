<!-- authority: control -->

# Minimal Countermodel Obligation Policy v1

## Source Basis

This policy implements v18 P4-T01 and recommendation `V18-R03`. It is a
project-control policy for future theorem and theorem-like packets. It changes
no canonical physics source, adopts no source law, proves no EqSrc result, and
does not update the Distance-to-GR ledger.

The policy exists because the v18 EqSrc family-closure attempt exposed a
recurring hazard: a packet can prove a conditional theorem under supplied
closure assumptions while leaving the failure modes under assumption removal
too implicit for later routing. Future theorem attempts must preserve the
positive theorem branch and the local failure branch in the same receipt.

## 1. Why Theorem Attempts Require Countermodel Slots

A theorem attempt is incomplete as project-control evidence if it records only
the assumptions under which a statement works. The control record must also
state what is expected to fail when one derivation-critical assumption is
removed, weakened, made nonunique, made partial, or shown to import target-side
structure.

Countermodel slots are mandatory because they:

- expose which assumption is doing the work;
- separate a conditional theorem from a source-derived theorem;
- preserve local negative evidence without inflating it into a program-wide
  conclusion;
- give later repair, selector, Refuter, and Gate Chair packets a deterministic
  surface to inspect;
- prevent hidden promotion from "the theorem holds under H" to "H was derived
  by the current ontology."

Every future theorem attempt must either fill the required countermodel slots
for its theorem family or cite an explicit Director Decision Record waiver.
The waiver must name the omitted slot, the reason it is not applicable, the
source path for that decision, and the next packet that will cover the risk if
the risk is deferred rather than impossible.

## 2. Countermodel, Obstruction, Freeze, And Program-Wide No-Go

The following terms are control statuses, not interchangeable conclusions.

| Term | Meaning | Allowed consequence | Forbidden overread |
| --- | --- | --- | --- |
| Countermodel | A bounded source-side example, partial model, assumption-deletion case, or fail-closed branch showing that a stated theorem condition is not automatic. | Records local failure pressure and informs repair or selector routing. | It is not proof that every future source-extension route is impossible. |
| Obstruction | A named local block showing that the current route cannot claim the stronger result without additional source-side data, repair, audit, or gate authority. | Blocks the current overread and may route to repair, selector, or freeze review. | It is not a program-wide no-go by itself. |
| Freeze | A control decision to stop repeating a route because repeated burdens or scoped obstruction criteria are met. | Preserves negative-result evidence and prevents process orbit. | It is not rejection of the entire research program unless a separate tracked theorem proves that broader claim. |
| Program-wide no-go | A protected conclusion that a broad research path cannot work under a stated class of extensions. | Requires a separate theorem, audit, stress, and appropriate authority. | It must not be inferred from one local countermodel, one obstruction, one validator warning, or one freeze record. |

Agents must report local scope first: "countermodel for this slot under these
assumptions." They must not compress that result into "the route is impossible"
unless the exact broader impossibility claim has separate tracked support.

## 3. Required Countermodel Slots By Theorem Family

Every theorem attempt must include the common slots below unless a slot is
inapplicable and waived by an explicit Director Decision Record.

```yaml
common_countermodel_slots:
  assumption_deletion_countermodel:
    purpose: "Remove one derivation-critical assumption and record the first fail-closed branch."
  missing_inverse_or_left_inverse_countermodel:
    purpose: "Show whether a required inverse, partial inverse, or recovery map is supplied or merely assumed."
  missing_composition_or_closure_countermodel:
    purpose: "Show whether composition, transitivity, closure, or family stability is supplied or derived."
  nonunique_selector_countermodel:
    purpose: "Show whether the theorem depends on an unproven selector, discriminator, or tie-break rule."
  finite_variation_fragility_countermodel:
    purpose: "Show whether the result survives the smallest relevant finite or local variation."
  hidden_target_import_countermodel:
    purpose: "Show whether the theorem needs target metric, detector, stress-energy, action, benchmark, or process-authority structure."
  accepted_evidence_overread_countermodel:
    purpose: "Show whether scoped positive evidence was silently used as adoption or proof authority."
```

A theorem family may add more slots. It may not remove these common slots
without a waiver.

## 4. EqSrc-Specific Slots

EqSrc theorem attempts must include these slots:

```yaml
eqsrc_countermodel_slots:
  - missing_inverse_countermodel
  - missing_composition_countermodel
  - invariant_ledger_not_family_stable_countermodel
  - target_import_needed_countermodel
  - RetainH_needed_countermodel
  - GenH_needed_countermodel
```

Required interpretation:

- `missing_inverse_countermodel` checks whether inverse or recovery data are
  derived by source-side structure or supplied as an assumption.
- `missing_composition_countermodel` checks whether family composition is
  closed without adding hidden RetainH or GenH assumptions.
- `invariant_ledger_not_family_stable_countermodel` checks whether a ledger
  invariant stays stable under the family operation.
- `target_import_needed_countermodel` checks whether target atlas, target
  metric, detector, benchmark, or process-authority data entered the proof.
- `RetainH_needed_countermodel` and `GenH_needed_countermodel` check whether
  those primitives are needed and whether they are only candidate-definition
  obligations rather than adopted source laws.

## 5. Matter-Coupling-Specific Slots

Matter-coupling theorem attempts must include these slots:

```yaml
matter_coupling_countermodel_slots:
  - source_matter_semantics_missing_countermodel
  - coupling_law_gap_countermodel
  - MetricData_or_g_eff_overread_countermodel
  - stress_energy_import_countermodel
  - matter_action_import_countermodel
  - benchmark_dependency_countermodel
```

These slots protect against treating scoped evidence, metric-language context,
or candidate bridge data as matter-coupling derivation. A local matter-coupling
countermodel may block a packet's current claim, but it does not derive the
opposite theory and does not close future source-extension work.

## 6. Detector/Readout-Specific Slots

Detector, readout, or observation-localization theorem attempts must include
these slots:

```yaml
detector_readout_countermodel_slots:
  - detector_semantics_import_countermodel
  - readout_equivalence_nonconservation_countermodel
  - rr_e_collapse_countermodel
  - calibration_import_countermodel
  - no_target_certificate_overread_countermodel
```

These slots preserve the distinction between source-side readout structure and
target-side detector semantics. A no-target certificate may block target import,
but it does not supply positive detector semantics.

## 7. Toy-Model-Specific Slots

Finite, local, toy-model, or support-only theorem attempts must include these
slots:

```yaml
toy_model_countermodel_slots:
  - missing_transport_countermodel
  - missing_invariance_countermodel
  - missing_factorization_countermodel
  - finite_variation_fragility_countermodel
  - empty_selector_countermodel
  - support_tool_overread_countermodel
```

Toy-model slots must state the finite source set, maps or relations tested,
variation allowed, and the exact claim that remains support-only. A support
tool or fixture cannot become proof authority merely because it passes.

## 8. Completion Receipt Requirements

Every future theorem or theorem-like completion must include a
`countermodel_obligations` block or a Director Decision Record waiver.

Minimum receipt structure:

```yaml
countermodel_obligations:
  policy_id: "minimal_countermodel_obligation_policy_v1"
  theorem_family: "eqsrc | matter_coupling | detector_readout | toy_model | other"
  waiver_decision_id: ""
  slots:
    - countermodel_slot: string
      status: "filled | waived_by_ddr | not_applicable_by_ddr | deferred_by_ddr"
      scope: string
      result_artifact: string
      obstruction_id: string
      local_countermodel_claim: string
      forbidden_overread: string
```

Rules:

- `status` may not be blank.
- `scope` must identify the theorem family and the assumption or primitive at
  issue.
- `result_artifact` must point to the theorem artifact, receipt, or future
  registry row containing the slot result.
- `forbidden_overread` must block adoption, downstream GR claims, benchmark
  promotion, completed derivation, and program-wide conclusion language when
  relevant.
- A deferred slot still counts as a live obligation for the next selector.

## 9. Validator Requirements

P4-T03 must add advisory validation for this policy. Until P4-T03 exists, this
policy is enforced by task design, receipt review, and Director routing.

Required validator behavior for the first v18 cycle:

```yaml
validator_requirements:
  missing_countermodel_slot: "warn_current_control"
  theorem_without_countermodel_justification: "warn_current_control"
  countermodel_scope_missing: "warn_current_control"
  waiver_without_director_decision: "warn_current_control"
  countermodel_overread_as_program_wide_no_go: "overclaim_hard_fail"
  countermodel_as_adoption_or_promotion: "overclaim_hard_fail"
```

The validator must be conservative. Missing slots warn in the first cycle so
historical packets are not invalidated. Overread of a local countermodel as
adoption, promotion, completed derivation, or program-wide conclusion must fail
hard for changed records.

## 10. Forbidden Conclusions

This policy does not authorize:

- canonical ontology edit;
- general EqSrc discharge;
- RetainH adoption;
- GenH adoption;
- source-law adoption;
- detector semantics adoption;
- matter semantics adoption;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- MetricData(E) adoption;
- g_eff adoption or scope expansion;
- stress-energy semantics;
- stress-energy tensor construction;
- matter action;
- Einstein equations;
- benchmark promotion;
- Gate Chair verdict;
- completed derivation;
- future source-extension impossibility;
- program-wide no-go conclusion;
- treating generated derivatives, validators, registries, handoffs, commits,
  caches, or current-frontier renderings as proof authority.

## Machine-Readable Summary

```yaml
minimal_countermodel_obligation_policy_v1:
  policy_status: "project_control"
  plan_task_id: "P4-T01"
  recommendation_ids: ["V18-R03"]
  theorem_attempts_require_countermodel_slots: true
  waiver_requires_explicit_director_decision_record: true
  local_countermodel_as_program_wide_no_go_forbidden: true
  first_cycle_missing_slot_behavior: "warn_current_control"
  overread_behavior: "hard_fail_for_changed_records"
  next_plan_task_id: "P4-T02"
  physics_delta_allowed: false
  physics_promotion_authorized: false
```

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v18* [Internal implementation plan].

The AEther-Flow Research Project. (2026b). *Post-EqSrc family-closure selector
receipt* [Research-control receipt].
