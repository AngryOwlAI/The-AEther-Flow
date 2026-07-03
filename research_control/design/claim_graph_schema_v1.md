<!-- authority: control -->

# Claim Graph Schema v1

## Purpose

`claim_graph_schema_v1` is the v15 control schema for a machine-readable
claim graph. It defines node and edge records that future tooling can use to
connect source objects, source-extension objects, evidence, theorem targets,
obstructions, generated derivatives, validator receipts, and next routes.

The schema is project-control metadata only. It is not proof authority, not a physics source,
not an ontology edit, not a Gate Chair verdict, not a route
freeze verdict, and not authority to promote source laws, matter semantics,
detector semantics, coupling laws, matter coupling, `MetricData(E)`, `g_eff`,
stress-energy semantics, a stress-energy tensor, a matter action, a variation
principle, Einstein equations, benchmark status, a completed derivation, a
program-wide no-go conclusion, or future source-extension impossibility.

## Authority Boundary

Every graph record must preserve a distinction between three layers:

| Layer | Allowed use | Forbidden use |
| --- | --- | --- |
| Authority source | A canonical file or registry row that states the claim, status, receipt, or relation. | Inferring a stronger claim than the authority source states. |
| Graph node or edge | Machine-readable pointer to an authority-backed claim boundary. | Treating the graph as independent scientific authority. |
| Generated derivative | Human or machine reading surface derived from canonical sources. | Treating derivative content as canonical when the source or registry differs. |

The graph may make a blocked overread visible. It must not remove the block.
When a graph record has incomplete authority evidence, the valid state is a
scoped missing-evidence record, not an inferred positive claim.

## Graph Envelope

Every graph artifact that claims conformance to this schema must include the
following envelope fields:

```yaml
claim_graph_schema_id: "claim_graph_schema_v1"
graph_id: "claim_graph_v1"
generated_at: "YYYY-MM-DDTHH:MM:SSZ"
generator:
  name: "script-or-agent-name"
  version: "version-or-commit"
source_authority:
  canonical_sources:
    - "registries/DISTANCE_TO_GR_LEDGER.csv"
    - "research_control/current_frontier.md"
  derivative_sources_allowed: false
nodes: []
edges: []
validation:
  validator_name: ""
  validator_version: ""
  status: "not_validated"
claim_boundary:
  graph_is_proof_authority: false
  graph_changes_scientific_claims: false
  graph_promotes_status: false
```

The envelope must be valid even when `nodes` and `edges` are empty. Future
P12-T02 generator work may add non-normative fields, but it must preserve
these required fields.

## Required Node Record

Every node must include these fields:

```yaml
node_id: "stable-local-node-id"
node_type: "source_object"
label: "Human-readable label"
status: "active"
authority_path: "canonical/source/path"
authority_registry: "registries/RELEVANT_REGISTRY.csv"
authority_object_id: "registry-object-id-or-empty"
promotion_status: "not_promoted"
overread_guards: []
validator_receipt_only: false
scientific_proof_authority: false
source_hash: ""
metadata: {}
```

### Node Field Rules

| Field | Rule |
| --- | --- |
| `node_id` | Stable identifier unique inside the graph. It should be deterministic across generator runs when the authority source is unchanged. |
| `node_type` | One of the controlled node types listed below. |
| `label` | Human-readable label. It must not contain a stronger claim than the authority source. |
| `status` | Source-backed state such as `active`, `blocked`, `conditional`, `proved`, `frozen`, `human_gated`, `generated`, or `receipt`. |
| `authority_path` | Canonical source path for the claim boundary. Generated derivatives may appear only when the node type is `generated_derivative` and the node has `is_derivative_of` evidence through an edge. |
| `authority_registry` | Registry path that names the canonical object when a registry row exists; empty only when no registry surface exists yet. |
| `authority_object_id` | Registry object ID, task ID, job ID, claim boundary ID, or empty string when unavailable. |
| `promotion_status` | Controlled promotion state. It must not be inferred from graph connectivity. |
| `overread_guards` | Nonempty for high-risk positive or support-looking records. Guards state what the node does not establish. |
| `validator_receipt_only` | `true` only for validator receipt nodes and receipt-like operational evidence. Receipt nodes cannot be proof authority. |
| `scientific_proof_authority` | `true` only when the canonical source is itself an authorized proof artifact with appropriate gate context. Validator receipts and generated derivatives must set this to `false`. |
| `source_hash` | Hash of the source authority when available. Empty is allowed only when the generator cannot lawfully compute it. |
| `metadata` | Optional map for provenance, line anchors, timestamps, route labels, or controlled-domain fields. |

## Controlled Node Types

The following node types are normative:

- `source_object`
- `source_extension_object`
- `evidence_precondition`
- `theorem_target`
- `theorem_candidate`
- `proved_theorem`
- `conditional_theorem`
- `obstruction`
- `frozen_route`
- `human_gated_decision`
- `blocked_physical_target`
- `generated_derivative`
- `validator_receipt`

### Node Type Semantics

| Node type | Meaning | Required guard |
| --- | --- | --- |
| `source_object` | Canonical or registered source-side object. | Must not imply downstream adoption unless the authority source explicitly states adoption. |
| `source_extension_object` | Draft/control, scoped evidence, or candidate source-extension object. | Must preserve scope and adoption status. |
| `evidence_precondition` | Required certificate, witness, datum, or condition. | Must include `does_not_establish` edges to downstream physical targets when it is support-like. |
| `theorem_target` | Desired theorem or derivation target not yet proved. | Must remain distinct from theorem candidates and proved theorems. |
| `theorem_candidate` | Draft or candidate theorem package. | Must not be presented as proved without a source-backed proof status. |
| `proved_theorem` | Authorized theorem result under declared assumptions. | Must preserve assumptions and scope. |
| `conditional_theorem` | Theorem valid only under explicit conditions or certificates. | Must link to the conditions and forbid unconditional overread. |
| `obstruction` | Scoped failure, certificate gap, missing law, countermodel, or route obstruction. | Must not imply program-wide no-go or future source-extension impossibility without separate authority. |
| `frozen_route` | Route pause or freeze state. | Must cite a tracked freeze record or policy outcome. |
| `human_gated_decision` | Human-gated or Gate Chair decision record. | Must not expand beyond the exact decision scope. |
| `blocked_physical_target` | Downstream physical target that remains blocked. | Must state the missing burden or blocking edge. |
| `generated_derivative` | Output derived from canonical sources. | Must have an `is_derivative_of` edge to canonical authority and cannot exceed source promotion status. |
| `validator_receipt` | Operational validation, CI, linter, or bootstrap receipt. | Must set `validator_receipt_only: true` and `scientific_proof_authority: false`. |

## Promotion Status Vocabulary

Allowed `promotion_status` values:

- `not_promoted`
- `none`
- `draft_control`
- `scoped_evidence_precondition`
- `scoped_source_object_only`
- `source_extension_data_only`
- `conditional_under_explicit_assumptions`
- `proved_under_declared_assumptions`
- `human_gated`
- `blocked`
- `frozen`
- `generated_only`
- `validator_receipt_only`

Promotion status is a recorded claim boundary, not a graph-computed property.
No node or edge may infer adoption of a source law, `RR_E` source law,
`RR_ETransportCompletenessOrInvarianceLaw_v1`, `PositiveMSProfile_v1`,
`SourceMatterSemanticsAdoptionReadinessLaw_v1`, matter semantics, detector
semantics, a coupling law, matter coupling, `MetricData(E)`, `g_eff`,
stress-energy semantics, a stress-energy tensor, a matter action, a variation
principle, Einstein equations, benchmark promotion, Gate Chair verdict,
completed derivation, program-wide no-go conclusion, or future
source-extension impossibility unless the cited authority source explicitly
and lawfully states that promotion.

## Required Edge Record

Every edge must include these fields:

```yaml
edge_id: "stable-local-edge-id"
edge_type: "supports"
source_node_id: "node-a"
target_node_id: "node-b"
authority_path: "canonical/source/path"
authority_registry: "registries/RELEVANT_REGISTRY.csv"
authority_object_id: "registry-object-id-or-empty"
does_not_establish: []
overread_guards: []
requires_human_gate: false
metadata: {}
```

### Edge Field Rules

| Field | Rule |
| --- | --- |
| `edge_id` | Stable identifier unique inside the graph. |
| `edge_type` | One of the controlled edge types listed below. |
| `source_node_id` | Existing node ID. |
| `target_node_id` | Existing node ID. |
| `authority_path` | Canonical path that supports the relation. |
| `authority_registry` | Registry path when available. |
| `authority_object_id` | Registry object ID, task ID, job ID, claim boundary ID, or empty string. |
| `does_not_establish` | Required for validator receipts, generated derivatives, scoped evidence, and high-risk positive-looking support. |
| `overread_guards` | Required when an edge could be misread as downstream proof, adoption, or promotion. |
| `requires_human_gate` | `true` when traversing the relation would require protected human authority. |
| `metadata` | Optional map for route labels, source line anchors, validation status, or generator evidence. |

## Controlled Edge Types

The following edge types are normative:

- `supports`
- `depends_on`
- `blocks`
- `forbids_overread`
- `requires_certificate`
- `requires_human_gate`
- `supersedes`
- `is_derivative_of`
- `does_not_establish`
- `next_route`

### Edge Type Semantics

| Edge type | Meaning | Required guard |
| --- | --- | --- |
| `supports` | Source-backed support relation under declared scope. | Add `does_not_establish` when support is not proof or adoption. |
| `depends_on` | Target requires source, condition, certificate, or prior route. | Must preserve missing or blocked dependency status. |
| `blocks` | Source node blocks target node under stated scope. | Must state whether same-milestone continuation remains open. |
| `forbids_overread` | Explicit negative edge preventing a stronger claim. | Must name the forbidden overread. |
| `requires_certificate` | Target requires a certificate, witness, or receipt. | Must name required certificate class. |
| `requires_human_gate` | Target transition requires protected human authority. | Must set `requires_human_gate: true`. |
| `supersedes` | New authority supersedes older control record within scope. | Must not erase historical provenance. |
| `is_derivative_of` | Generated derivative depends on canonical source. | Required for every `generated_derivative` node. |
| `does_not_establish` | Negative relation naming what is not established. | Required from validator receipt nodes to physical targets. |
| `next_route` | Completion or handoff routes to the next bounded packet. | Must not execute or authorize the next packet by itself. |

## Validator Receipts Versus Scientific Proof

Validator receipt nodes record operational checks. They can show that a file,
registry, generated derivative, or local validation pipeline passed a
configured check. They do not prove a physical theorem and do not promote
scientific status.

Every `validator_receipt` node must satisfy:

```yaml
node_type: "validator_receipt"
promotion_status: "validator_receipt_only"
validator_receipt_only: true
scientific_proof_authority: false
overread_guards:
  - "Validation receipt is operational evidence only."
```

Every outgoing edge from a `validator_receipt` node to a theorem, physical
target, source-extension object, or promotion target must include
`does_not_establish`. A validator receipt may support operational confidence;
it does not establish source-law adoption, matter-coupling derivation,
Einstein equations, benchmark promotion, or completed derivation.

## Generated Derivative Rule

Every `generated_derivative` node must have at least one incoming or outgoing
`is_derivative_of` edge linking it to a canonical source object. A generated
derivative cannot have a stronger `promotion_status` than the canonical source
it derives from. If the canonical source is blocked, draft/control, or
validator-receipt-only, the derivative remains blocked, draft/control, or
validator-receipt-only for that claim.

## Minimal Valid Example

```yaml
claim_graph_schema_id: "claim_graph_schema_v1"
graph_id: "claim_graph_v1_example"
generated_at: "2026-07-03T19:34:50Z"
generator:
  name: "manual-example"
  version: "v1"
source_authority:
  canonical_sources:
    - "research_control/current_frontier.md"
    - "registries/DISTANCE_TO_GR_LEDGER.csv"
  derivative_sources_allowed: false
nodes:
  - node_id: "node-validator-local-ci"
    node_type: "validator_receipt"
    label: "Local CI-equivalent validation receipt"
    status: "receipt"
    authority_path: "research_control/tasks/RT-EXAMPLE/artifacts/local_ci_report.json"
    authority_registry: "registries/AGENT_JOB_REGISTRY.csv"
    authority_object_id: "AJ-RT-EXAMPLE-001"
    promotion_status: "validator_receipt_only"
    overread_guards:
      - "The receipt is operational evidence only."
      - "The receipt does not establish Einstein equations or benchmark promotion."
    validator_receipt_only: true
    scientific_proof_authority: false
    source_hash: ""
    metadata: {}
  - node_id: "node-einstein-equations"
    node_type: "blocked_physical_target"
    label: "Einstein equations"
    status: "blocked"
    authority_path: "research_control/current_frontier.md"
    authority_registry: "registries/DISTANCE_TO_GR_LEDGER.csv"
    authority_object_id: "BURDEN-EINSTEIN-EQUATIONS"
    promotion_status: "blocked"
    overread_guards:
      - "No Einstein-equation derivation follows from validation receipts."
    validator_receipt_only: false
    scientific_proof_authority: false
    source_hash: ""
    metadata: {}
edges:
  - edge_id: "edge-local-ci-does-not-establish-einstein"
    edge_type: "does_not_establish"
    source_node_id: "node-validator-local-ci"
    target_node_id: "node-einstein-equations"
    authority_path: "research_control/design/claim_graph_schema_v1.md"
    authority_registry: "registries/MARKDOWN_SOURCE_REGISTRY.csv"
    authority_object_id: "MD-RESEARCH-CONTROL-DESIGN-CLAIM-GRAPH-SCHEMA-V1"
    does_not_establish:
      - "Einstein equations"
      - "benchmark promotion"
      - "completed derivation"
    overread_guards:
      - "Operational validation is not proof authority."
    requires_human_gate: false
    metadata: {}
validation:
  validator_name: ""
  validator_version: ""
  status: "not_validated"
claim_boundary:
  graph_is_proof_authority: false
  graph_changes_scientific_claims: false
  graph_promotes_status: false
```

## Validation Expectations

A future P12-T03 validator should fail a claim graph when:

- the graph omits the required envelope fields;
- any node omits a required node field;
- any edge omits a required edge field;
- an unknown `node_type`, `edge_type`, or `promotion_status` appears;
- a `validator_receipt` node has `validator_receipt_only: false` or
  `scientific_proof_authority: true`;
- a validator receipt has a support-like edge to a physical target without a
  `does_not_establish` edge or field;
- a `generated_derivative` node lacks an `is_derivative_of` edge;
- a derivative node claims stronger promotion status than its canonical source;
- a high-risk positive node has no `overread_guards`;
- an edge requiring a protected transition has `requires_human_gate: false`;
- graph metadata treats a generated derivative or validator receipt as
  scientific proof authority; or
- the graph states adoption, derivation, benchmark promotion, completed
  derivation, program-wide no-go, or future source-extension impossibility
  without explicit canonical authority and required human gate evidence.

## Next Route

The logical next P12 packet is P12-T02, a claim graph generator pilot. That
future packet should generate `output/claim_graph_v1.json`,
`output/claim_graph_v1.dot`, and `wiki/indexes/claim_graph_v1.md` from the
Distance-to-GR ledger and frontier theorem inventory. It must use this schema
as an input contract and must preserve no physics delta.

## Source Materials

The AEther-Flow Research Project. (2026, July 3). *Recommendations
implementation plan continue task v15* [Internal implementation plan].
`implementations_plans/recommendations_implementation_plan_continue_task-v15.md`

The AEther-Flow Research Project. (2026, July 3). *Current frontier*
[Research-control frontier]. `research_control/current_frontier.md`

The AEther-Flow Research Project. (2026, July 3). *Matter-coupling dependency
DAG v1* [Internal project-control note].
`research_control/design/matter_coupling_dependency_dag_v1.md`

The AEther-Flow Research Project. (2026, July 3). *Route signature schema v1*
[Internal project-control schema].
`research_control/design/route_signature_schema_v1.md`
