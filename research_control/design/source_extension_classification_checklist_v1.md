<!-- authority: control -->

# Source-Extension Classification Checklist v1

## Status

This checklist implements v15 P6-T01. It is a project-control classification
surface for source-extension objects and source-extension evidence.

It does not prove a physics claim, adopt canonical ontology, adopt a source
law, authorize matter semantics, authorize detector semantics, authorize a
coupling law, derive matter coupling, adopt `MetricData(E)`, change the scope
of `g_eff`, import stress-energy semantics, construct a stress-energy tensor,
import a matter action, derive Einstein equations, promote benchmark status,
issue a Gate Chair verdict, or complete a derivation.

## Scope

Use this checklist whenever a research-control task, handoff, completion, or
validator describes a source-extension object, source-extension datum,
source-extension evidence/precondition, proposed source-side primitive, or
candidate route whose status might otherwise be overread as derivation.

The checklist is subordinate to registered science/control sources, the active
claim-boundary registry row, `registries/DISTANCE_TO_GR_LEDGER.csv`, and the
latest tracked handoff. Generated wiki notes, generated graphs, semantic
extracts, validators, approvals, commits, and local caches do not classify or
promote source-extension objects by themselves.

## Classification Record

Every classified item must record:

- item identifier and source path;
- item kind: object, datum, law target, theorem target, evidence/precondition,
  obstruction, or route;
- proposed classification from the allowed vocabulary below;
- exact repository evidence for the classification;
- relation to current ontology;
- relation to target-side structures;
- required protected authority, if any;
- allowed conclusion language;
- forbidden conclusion language;
- downstream promotion status;
- next lawful route if the classification is ambiguous or blocked.

Missing classification records fail closed: the item may not be used as
derivation support, adoption support, benchmark support, or completed
derivation support.

## Allowed Classifications

| Classification | Required evidence | Allowed conclusion language | Forbidden conclusion language | Next route |
| --- | --- | --- | --- | --- |
| `derived_from_current_ontology` | A tracked proof or derivation shows that the item follows from current registered ontology and already-authorized source-side definitions, without adding a primitive, changing a source law, importing target-side data, or relying on generated artifacts as authority. The proof must name all premises, source paths, scope limits, and fail-closed branches. | "derived from current ontology within the declared source-side scope" | Bare new-law adoption wording, bare matter-coupling promotion wording, bare Einstein-equation promotion wording, bare benchmark-promotion wording, or bare completion wording. | Use as scoped source-side support only inside the named scope. |
| `conservative_definitional_extension` | An eliminability or definitional-expansion argument shows the item is only an abbreviation, packaging convention, schema, or presentation layer over existing authorized source-side material. The record must show how to eliminate the item without changing admissible models, source-side consequences, physical claims, or claim boundaries. | "conservative definitional extension for control or notation" | "new ontology primitive adopted", "new source law adopted", "downstream physics follows" | Keep as project-control or notation support; route to audit if eliminability is uncertain. |
| `new_ontology_primitive_candidate` | The current ontology does not derive the item and no conservative definitional elimination is known. The record must name the missing source-side law, selector, discriminator, transition rule, robustness rule, or equivalent primitive and preserve exact-GR recovery obligations. | "proposal-only new ontology primitive candidate" or "human-gated candidate" | Bare adoption wording, canonical-ontology-change wording, source-law-holds wording, or future-source-extension closure wording. | Route to bounded ontology-law research, smuggling audit, refuter stress, or protected human gate. |
| `forbidden_target_import` | The item relies on target manifold structure, target metric, target topology, target atlas, proper time, detector semantics, stress-energy semantics, stress-energy tensor, matter action, Einstein equations, benchmark behavior, empirical fit, or Gate Chair closure as source-side construction data. | "forbidden target import; fail closed" | "source-side derivation", "certificate support", "matter coupling support", "benchmark support" | Reject for current source-extension support; route only to repair or smuggling audit. |
| `status_boundary_evidence_only` | A tracked result accepts or uses the item only as scoped evidence/precondition, status boundary, route evidence, diagnostic evidence, or control support. The record must name the exact accepted scope and blocked overreads. | "accepted only as scoped evidence/precondition" or "status-boundary evidence only" | Bare object-adoption wording, bare law-adoption wording, bare matter-semantics-adoption wording, bare coupling-adoption wording, or bare benchmark-promotion wording. | May support later bounded routing; cannot discharge derivation burdens by itself. |
| `blocked_adoption_open_continuation` | Current adoption is blocked because required proof, source-side law, classification evidence, audit, stress result, or protected authority is absent, while a conservative extension, repair, or same-milestone continuation remains possible. | "blocked adoption with open continuation" | Global no-go wording, future-source-extension closure wording, or program-wide rejection wording. | Route to the narrow next continuation packet named by the blocker. |

## Decision Procedure

Classify in this order:

1. If any target-side construction data are used as source-side premises,
   classify as `forbidden_target_import`.
2. If tracked proof derives the item from current ontology without new
   primitive, classify as `derived_from_current_ontology`.
3. If eliminability is explicit and model-conservative, classify as
   `conservative_definitional_extension`.
4. If a prior scoped result only supports routing or precondition status,
   classify as `status_boundary_evidence_only`.
5. If adoption is blocked while bounded continuation remains possible,
   classify as `blocked_adoption_open_continuation`.
6. If a genuinely new source-side primitive appears necessary, classify as
   `new_ontology_primitive_candidate` and route through the protected or
   bounded continuation path named by tracked state.

Ambiguous items must not be upgraded by default. If two classifications are
plausible, choose the more restrictive status and route a later bounded audit.

## Allowed Language

Allowed phrases:

- "derived from current ontology within the declared source-side scope";
- "conservative definitional extension";
- "proposal-only new ontology primitive candidate";
- "forbidden target import; fail closed";
- "accepted only as scoped evidence/precondition";
- "status-boundary evidence only";
- "blocked adoption with open continuation";
- "same-milestone continuation remains open";
- "no physics delta";
- "no downstream promotion authorized".

## Forbidden Language

Forbidden without separate tracked proof and protected authority:

- "therefore the source law is adopted";
- "therefore matter semantics are adopted";
- "therefore detector semantics are adopted";
- "therefore the coupling law is adopted";
- "therefore matter coupling is derived";
- "therefore `MetricData(E)` is adopted";
- "therefore `g_eff` scope expands";
- "therefore stress-energy semantics are available";
- "therefore a stress-energy tensor is constructed";
- "therefore a matter action is imported";
- "therefore Einstein equations are derived";
- "therefore the exact-GR benchmark is promoted";
- "therefore the derivation is complete";
- "therefore future source-extension is impossible";
- "therefore the program is globally refuted".

## Required Receipt Fields

Any future source-extension AgentJob, completion, handoff, or retrofit report
that uses this checklist should include:

```yaml
source_extension_classification:
  checklist_id: "source_extension_classification_checklist_v1"
  item_id: "<object or route id>"
  item_source_path: "<repo-relative path>"
  classification: "<one allowed classification>"
  evidence_paths:
    - "<repo-relative source path>"
  relation_to_current_ontology: "<derived | conservative | missing_primitive | target_import | evidence_only | blocked_open>"
  protected_authority_required: false
  physics_promotion_authorized: false
  downstream_promotion_authorized: false
  allowed_conclusion: "<scoped allowed wording>"
  forbidden_overreads:
    - "source-law adoption"
    - "matter-coupling derivation"
    - "Einstein equations"
    - "benchmark promotion"
    - "completed derivation"
  next_route_if_blocked: "<bounded route or not_applicable>"
```

## Non-Conclusions

Passing this checklist is classification evidence only. It is not source-law
adoption, ontology adoption, matter-semantics adoption, detector-semantics
adoption, coupling-law adoption, matter-coupling derivation, stress-energy
semantics, matter-action authority, Einstein-equation derivation, benchmark
promotion, Gate Chair closure, or completed derivation.

Exact non-conclusions:

- source-law adoption;
- ontology adoption;
- matter-semantics adoption;
- detector-semantics adoption;
- coupling-law adoption;
- matter-coupling derivation;
- Einstein-equation derivation;
- benchmark promotion;
- completed derivation.

## Machine-Readable Checklist

```yaml
source_extension_classification_checklist:
  schema_id: "source_extension_classification_checklist_v1"
  status: "draft/control"
  required_classifications:
    - "derived_from_current_ontology"
    - "conservative_definitional_extension"
    - "new_ontology_primitive_candidate"
    - "forbidden_target_import"
    - "status_boundary_evidence_only"
    - "blocked_adoption_open_continuation"
  missing_classification_fails_closed: true
  requires_evidence_paths: true
  requires_relation_to_current_ontology: true
  requires_allowed_conclusion_language: true
  requires_forbidden_conclusion_language: true
  physics_promotion_authorized: false
  downstream_promotion_authorized: false
  proof_authority: false
```
