<!-- authority: control -->

# Validation Status Layer Schema

## Purpose

This schema separates validation receipts from protected authorization and
downstream scientific-promotion authority. It applies prospectively to
research-control completions and handoffs created under the validation-status
schema split.

The aggregate `validation_status` field remains a compatibility field for
registries and checkpoint tooling. It is not sufficient reader-facing evidence
for future records unless the record also includes the layer split below.

## Validation Layers

Future completions and handoffs should use:

```yaml
validation_layers:
  pre_execution:
    status: ""
    evidence: []
  completion_internal:
    status: ""
    evidence: []
  post_write:
    status: ""
    evidence: []
  post_checkpoint:
    status: ""
    evidence: []
  renderer:
    status: ""
    evidence: []
  memory_bootstrap:
    status: ""
    evidence: []
  claim_language_linter:
    status: ""
    evidence: []
```

Allowed status values are `PASS`, `PASS_WITH_WARNINGS`, `PENDING`, `FAIL`,
`NOT_RUN`, and `NOT_APPLICABLE`.

Every layer requires nonblank evidence. A `PENDING` layer must state what is
pending and why it does not contradict any aggregate compatibility status.

## Authorization Layers

Future completions and handoffs should use:

```yaml
authorization_layers:
  protected_scoped_gate_review_authorized: false
  protected_scoped_gate_review_scope: ""
  protected_scoped_gate_review_authority_source_path: ""
  downstream_physics_promotion_authorized: false
  downstream_physics_promotion_authority_source_path: ""
  benchmark_promotion_authorized: false
  benchmark_promotion_authority_source_path: ""
  completed_derivation_authorized: false
  completed_derivation_authority_source_path: ""
```

The protected scoped gate-review field records whether a specific protected
review has been authorized for the named scope. It does not authorize
downstream physics promotion, benchmark promotion, or completed-derivation
claims.

Downstream scientific-promotion booleans must remain false unless a separate
tracked authority source explicitly authorizes that exact promotion. If any
authorization boolean is true, the matching authority source path is required.

## Legacy Compatibility

Historical records may retain `validation_status`,
`physics_progress_status.physics_promotion_authorized`, and
`forbidden_conclusion_summary.physics_promotion_authorized`. New records that
retain a legacy physics-promotion field must keep it consistent with
`authorization_layers.downstream_physics_promotion_authorized`.

Historical records must not be rewritten solely to satisfy this schema. Use
normal future completions, handoffs, or a bounded backfill packet when the
tracked plan requires public propagation.
