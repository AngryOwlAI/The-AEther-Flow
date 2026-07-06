<!-- authority: control -->

# Proof-Normal-Form Schema v1

## Purpose

This project-control schema defines a proof-normal-form row shape for
definitions, lemmas, theorem candidates, propositions, obstructions, decisions,
boundaries, and non-conclusions. It implements v17 P7-T01 only.

The proof-normal-form layer is an agent-retrieval and validation support
surface. It does not replace registered TeX authority, issue Gate Chair
verdicts, promote draft science, update Distance-to-GR ledger rows, or prove
matter coupling, Einstein equations, benchmark fitness, or completed
derivation.

## Authority Boundary

Canonical scientific and mathematical claims remain in registered source
artifacts. Proof-normal-form rows summarize source-local premises,
forbidden premises, conclusions, scope, allowed uses, non-conclusions,
dependencies, and eligible next routes so later agents can preserve exact
claim boundaries.

Rows may be used to:

- find source artifacts that need inspection;
- check whether non-conclusions are preserved;
- identify machine-checkable fragments;
- route follow-up packets under existing research-control authority.

Rows may not be used to:

- replace registered TeX or Gate Chair source inspection;
- infer a stronger conclusion than the source artifact states;
- adopt a source law, ontology primitive, `MetricData(E)`, `g_eff`, matter
  semantics, detector semantics, coupling law, matter coupling, stress-energy
  semantics, matter action, Einstein equations, benchmark promotion, or
  completed derivation.

## Registry

Canonical registry path:

```text
registries/PROOF_NORMAL_FORM_REGISTRY.csv
```

Required header:

```csv
proof_normal_form_row_id,object_id,source_artifact_path,claim_type,authority_status,status,premises,forbidden_premises,conclusion,scope,allowed_uses,non_conclusions,depends_on,eligible_next_routes,machine_checkable_fragment,created_at,notes
```

## Required Row Fields

| Field | Required meaning | Valid value rule |
| --- | --- | --- |
| `proof_normal_form_row_id` | Stable row identifier for traceability. | Unique nonblank value, preferably `PNF-<task-id>-<ordinal>`. |
| `object_id` | Source object or claim identifier being summarized. | Nonblank object, claim, theorem, obstruction, decision, or boundary id. |
| `source_artifact_path` | Repository-relative path to the canonical or task-local source artifact. | Nonblank path. Later validators may require existence unless a row is a planned placeholder. |
| `claim_type` | Kind of claim or non-claim represented. | Must be one of the allowed claim types below. |
| `authority_status` | Authority level of the represented source. | Must be one of the allowed authority statuses below. |
| `status` | Current proof-state status of the represented item. | Must be one of the allowed proof-state statuses below. |
| `premises` | Source-local premises explicitly used by the row. | Semicolon-separated list. Empty only when a definition or boundary has no premise. |
| `forbidden_premises` | Premises that must not be imported into this row. | Semicolon-separated list. Must be nonblank for high-risk rows. |
| `conclusion` | Exact conclusion or status statement. | Positive scoped statement only. |
| `scope` | Declared scope and valid regime. | Nonblank. Must not widen source authority. |
| `allowed_uses` | Uses permitted for later agents. | Semicolon-separated list. Must be nonblank. |
| `non_conclusions` | Conclusions explicitly not established. | Semicolon-separated list. Must be nonblank for high-risk rows. |
| `depends_on` | Source objects or rows needed for interpretation. | Semicolon-separated list or `none`. |
| `eligible_next_routes` | Routes that may lawfully consume the row. | Semicolon-separated list or `none`. |
| `machine_checkable_fragment` | Whether the represented fragment is machine-checkable as written. | Must be `true` or `false`. |
| `created_at` | UTC row creation timestamp. | ISO 8601 UTC timestamp. |
| `notes` | Short receipt note. | Must not promote physics claims. |

## Allowed Claim Types

```yaml
claim_types:
  - definition
  - lemma
  - theorem
  - proposition
  - obstruction
  - decision
  - boundary
  - nonconclusion
```

## Allowed Authority Statuses

```yaml
authority_statuses:
  - science_draft
  - scientific_gate
  - control
  - support_only
```

Interpretation:

- `science_draft`: the source is draft scientific or mathematical work and
  must retain its source-local status.
- `scientific_gate`: the source is a Gate Chair or other human-gated decision
  artifact and must not expand beyond its declared scope.
- `control`: the source is a project-control schema, registry, route, or
  boundary artifact.
- `support_only`: the row or source exists only to support retrieval,
  validation, traceability, or formalization tooling.

## Allowed Proof-State Statuses

```yaml
statuses:
  - draft_control
  - scoped_evidence
  - scoped_adopted
  - blocked
  - frozen_negative
  - not_started
```

Interpretation:

- `draft_control`: draft/control content exists but does not establish a
  promoted physics claim.
- `scoped_evidence`: evidence exists only inside a declared scope.
- `scoped_adopted`: a human-gated or otherwise authorized object is adopted
  only in its declared scope.
- `blocked`: a required downstream conclusion remains blocked.
- `frozen_negative`: a negative or obstruction route is frozen until a later
  authorized reopening.
- `not_started`: the row is a planned placeholder and must not be used as
  evidence.

## High-Risk Row Rule

A high-risk row is any row whose `object_id`, `conclusion`, `scope`, or
`allowed_uses` references `EqSrc`, `RetainH`, `GenH`, source-law adoption,
`MetricData(E)`, `g_eff`, matter semantics, detector semantics, coupling law,
matter coupling, stress-energy semantics, stress-energy tensor, matter action,
Einstein equations, benchmark promotion, Gate Chair verdicts, or completed
derivation.

High-risk rows must include nonblank `forbidden_premises` and
`non_conclusions`. Those fields must state the exact overreads being blocked.

## P7-T02 Population Rule

P7-T02 may populate registry rows for priority artifacts named in the v17 plan.
Every populated row must preserve source authority and non-conclusions. A row
that summarizes a theorem candidate, obstruction, or decision is still only an
index into the source artifact unless the source artifact itself carries the
relevant authority.

No proof-normal-form row may convert support-only schema work into proof authority.
