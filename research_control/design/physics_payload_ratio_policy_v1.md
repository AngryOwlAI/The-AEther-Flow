<!-- authority: control -->

# Physics Payload Ratio Policy v1

## Purpose

`physics_payload_ratio_policy_v1` implements the v18 P8-T01 control policy
for preventing long runs of process-only project-system work from displacing
the physics program. It requires the continuation system to prefer a
physics-bearing packet after a bounded run of project-system packets unless a
tracked exception applies.

This is a project-control policy. It is not a physics proof, not a canonical
ontology edit, not source-law adoption, not detector-semantics adoption, not
matter-coupling derivation or adoption, not an Einstein-equation derivation,
not benchmark promotion, not a Gate Chair verdict, and not completed
derivation evidence.

## Policy Values

```yaml
physics_payload_ratio_policy:
  policy_id: "physics_payload_ratio_policy_v1"
  recommendation_id: "V18-R07"
  after_project_system_tasks: 3
  require_next_task_type_one_of:
    - theorem_candidate
    - countermodel
    - finite_witness
    - obstruction_with_proof_sketch
    - source_primitive_requirement
    - candidate_construction
  exceptions:
    - failing_ci
    - registry_corruption
    - claim_boundary_hard_failure
    - human_gate_required
    - security_or_integrity_repair
  initial_enforcement: "advisory"
  physics_promotion_authorized: false
  proof_authority: false
```

`after_project_system_tasks: 3` means that after three consecutive bounded
project-system packets, the Director should route the next non-exempt packet
toward a physics-bearing task class. The threshold is intentionally advisory
in v1. P8-T02 must add metrics before this policy can be measured, and P8-T03
must pilot validator behavior before any standing enforcement exists.

## Definitions

`project-system task` means a bounded packet whose primary output is workflow,
schema, registry, validator, renderer, dashboard, publication, memory, or
documentation machinery. These tasks can be necessary. They do not by
themselves discharge a derivation burden unless they also contain a qualifying
physics payload.

`physics-bearing task` means a bounded packet whose primary output is one of
the required next-task classes in this policy or a compatible payload class
from `minimum_physics_payload_schema_v1`.

`process orbit` means a repeated sequence of project-system packets that
keeps improving control surfaces while postponing theorem, witness,
countermodel, obstruction, source-primitive, or candidate-construction work.
Process orbit is about task type and continuation behavior, not about whether
the support work was useful.

`route orbit` means a repeated route pattern around the same derivation
milestone or burden without new mathematical payload, finite/local evidence,
countermodel, precise obstruction, source model, source primitive, candidate
construction, or required protected gate. Route orbit is evaluated together
with `route_orbit_gating_policy_v16` and
`route_orbit_freeze_threshold_policy_v1`.

`helpful support work` means project-system work that removes a concrete
blocker, creates required validation machinery, preserves claim boundaries,
repairs registry or memory integrity, documents a required authority surface,
or prepares an explicitly named next physics-bearing packet.

`avoidance behavior` means project-system work that is not tied to a concrete
blocker, not required by validation, not required by a protected gate, and not
linked to a named next physics-bearing packet after the threshold is reached.

## Required Next-Task Classes

After three consecutive project-system tasks, the next non-exempt packet
should use one of these task classes:

| Task class | Required payload shape |
| --- | --- |
| `theorem_candidate` | A theorem target with premises, conclusion, valid regime, and failure branch. |
| `countermodel` | A minimal or bounded model showing a stronger claim fails under stated assumptions. |
| `finite_witness` | Explicit finite or locally finite source-side objects, maps, guards, tables, or records. |
| `obstruction_with_proof_sketch` | A precise obstruction plus the failed premise or proof branch. |
| `source_primitive_requirement` | A specific source-side law, selector, discriminator, transition rule, robustness rule, or equivalent primitive needed by a named derivation milestone. |
| `candidate_construction` | A bounded candidate object, bridge map, witness family, source model, or certificate instance with declared assumptions and blocked overreads. |

The selected packet may still remain `draft/control`, `proposal-only`,
`support-only`, `scoped evidence`, `negative result`, or `human-gated`. The
task class requirement does not promote the payload.

## Exceptions

The policy does not require a physics-bearing next packet when any tracked
exception is active:

- `failing_ci`: validation or test failures block honest continuation.
- `registry_corruption`: canonical routing, source, or role registries are
  inconsistent or unreadable.
- `claim_boundary_hard_failure`: a hard overclaim, target import, or protected
  authority leak must be repaired first.
- `human_gate_required`: the next honest step needs protected authority, such
  as ontology adoption, benchmark authority, Gate Chair verdict authority, or
  another explicit human gate.
- `security_or_integrity_repair`: repository integrity, checkpoint safety,
  credential safety, or security repair must precede research continuation.

Exceptions must be recorded in the task, completion, or handoff that invokes
them. An exception is not a permanent waiver. Once the exception is resolved,
the Director should re-evaluate the project-system run length and route
toward a physics-bearing packet when the threshold still applies.

## Helpful Support Versus Avoidance

Support work is helpful when it satisfies at least one of these conditions:

1. It repairs a failing validator, registry, memory, or checkpoint condition.
2. It adds a missing control contract required by the active plan.
3. It preserves a claim boundary that was at risk of overread.
4. It creates a measurement or diagnostic needed by the next packet.
5. It explicitly names the next physics-bearing packet and why it is lawful.
6. It prepares a protected human gate that cannot lawfully be skipped.

Support work becomes avoidance behavior when all of these are true:

1. Three consecutive project-system tasks have completed.
2. No tracked exception is active.
3. No next physics-bearing packet is named.
4. The proposed next packet mainly adds another process surface.
5. The packet does not repair a failing validator, registry, claim boundary,
   security, or checkpoint condition.

Avoidance classification is procedural. It does not mean the project has no
physics route, no candidate construction, no theorem path, or no future
source-extension possibility.

## Advisory Evaluation Record

P8-T02 metrics and P8-T03 validator pilot should be able to emit records in
this shape:

```yaml
physics_payload_ratio_policy_record:
  policy_id: "physics_payload_ratio_policy_v1"
  evaluated_window_task_ids:
    - "RT-YYYYMMDD-NNN"
  consecutive_project_system_task_count: 3
  threshold_met: true
  active_exception: ""
  exception_source_path: ""
  required_next_task_type_one_of:
    - theorem_candidate
    - countermodel
    - finite_witness
    - obstruction_with_proof_sketch
    - source_primitive_requirement
    - candidate_construction
  selected_next_task_type: "candidate_construction"
  decision: "advise_physics_bearing_next_packet"
  initial_enforcement: "advisory"
  physics_promotion_authorized: false
  proof_authority: false
```

Allowed advisory decisions are:

| Decision | Meaning |
| --- | --- |
| `not_applicable` | Fewer than three consecutive project-system tasks are in scope. |
| `advise_physics_bearing_next_packet` | The threshold is met and no exception is active. |
| `exception_active` | A tracked exception lawfully precedes physics-bearing work. |
| `satisfied_by_selected_packet` | The selected next packet is physics-bearing under this policy. |

## Relationship To Existing Policies

`minimum_physics_payload_schema_v1` defines payload classes for physics
completions. This policy defines when a long project-system sequence should
return to those payload classes or to a compatible theorem, witness,
countermodel, obstruction, source-primitive, or candidate-construction packet.

`route_orbit_gating_policy_v16` and
`route_orbit_freeze_threshold_policy_v1` evaluate repeated route behavior
inside physics continuation. This policy evaluates project-system run length
before the route can keep orbiting process surfaces.

The three policies are complementary:

- minimum-payload schema: "What counts as payload?"
- route-orbit policy: "When is a repeated route suspect?"
- physics-payload ratio policy: "When should process support hand back to
  physics-bearing continuation?"

## Enforcement Boundary

Initial enforcement is advisory. P8-T01 defines the policy only. P8-T02 may
extend metrics to compute project-system run length and physics-payload ratio.
P8-T03 may add an advisory validator pilot. No standing hard gate exists until
a later bounded packet explicitly creates and validates one.

The policy cannot be used as:

- proof authority;
- source-law adoption;
- detector/readout semantics adoption;
- matter-coupling derivation or adoption;
- stress-energy semantics;
- matter-action authority;
- Einstein-equation derivation;
- benchmark promotion;
- Gate Chair verdict;
- completed derivation claim;
- program-wide no-go conclusion;
- future source-extension impossibility claim.

## Done Criteria

- Process orbit is defined.
- Route orbit is defined and related to existing route-orbit policies.
- Helpful support work is distinguished from avoidance behavior.
- The three-project-system-task advisory threshold is stated.
- Required next-task classes and exceptions are listed.
- Initial enforcement is advisory.
- P8-T02 is the next route.
- No physics delta, proof authority, adoption, benchmark promotion, or
  completed derivation authority is created.
