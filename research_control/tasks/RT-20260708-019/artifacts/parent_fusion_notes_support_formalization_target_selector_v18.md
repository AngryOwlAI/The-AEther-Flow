<!-- authority: science_draft -->

# Parent Fusion Notes: P7-T01 Support Formalization Target Selector

## Consensus

Both child reviews select `typed_EqSrc_orbit_checker` as the single immediate
P7-T01 target. The mathematical reason is that the typed checker supplies the
finite record contract needed before closure countermodels and mutation tests
can be meaningfully scoped. The philosophical/control reason is that a finite
checker can be useful while remaining explicitly support-only.

## Selected Target

```yaml
selected_formalization_target:
  target_id: "typed_EqSrc_orbit_checker"
  selected: true
  support_only: true
  proof_authority: false
  selected_next_plan_task_id: "P7-T02"
```

## Remaining Sequence

```yaml
remaining_target_sequence:
  - plan_task_id: "P7-T03"
    target_id: "closure_countermodel_generator"
  - plan_task_id: "P7-T04"
    target_id: "no_target_import_mutation_tester"
  - plan_task_id: "P7-T05"
    target_id: "metric_use_ledger_tex_validator"
  - plan_task_id: "P7-T06"
    target_id: "detector_placeholder_collapse_checker"
```

## Boundary

This selection does not implement the checker and does not prove general
`EqSrc`. A future checker pass must be interpreted only as finite support
evidence for declared source-side records. It cannot authorize source-law
adoption, target metric import, `g_eff`, matter coupling, Einstein equations,
benchmark promotion, Gate Chair verdict, or completed derivation.

## Unresolved Limitations

No blocking conflicts remain. The main limitation is intentional: P7-T01 only
selects the target. P7-T02 must still implement and test the checker before any
tooling evidence exists.
