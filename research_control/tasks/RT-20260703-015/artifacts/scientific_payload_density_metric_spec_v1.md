<!-- authority: control -->

# Scientific Payload Density Metric Spec v1

## Purpose

This specification defines operational diagnostics only for distinguishing
mathematical payload from process-only work in tracked research-control
completions. The metric is an AI-system governance measure. It is not physics
proof, benchmark promotion, claim-promotion authority, Gate Chair authority, or
completed-derivation evidence.

## Payload Classes

The controlled class vocabulary is:

| Class ID | Label | Process-only |
|---|---|---|
| `new_definition` | new definition | no |
| `new_theorem_statement` | new theorem statement | no |
| `proof_attempt` | proof attempt | no |
| `proved_theorem` | proved theorem | no |
| `conditional_theorem` | conditional theorem | no |
| `countermodel` | countermodel | no |
| `obstruction` | obstruction | no |
| `finite_witness` | finite witness | no |
| `dependency_map_update` | dependency-map update | no |
| `source_extension_classification` | source-extension classification | no |
| `route_selector_only` | route selector only | yes |
| `validator_tooling_only` | validator/tooling only | yes |
| `documentation_only` | documentation only | yes |

## Counting Rule

The reporter reads completed AgentJob rows from
`registries/AGENT_JOB_REGISTRY.csv`, resolves their completion YAML records,
and prefers `mathematical_payload_manifest` as the payload source. If that
manifest is absent, it falls back to `new_mathematical_payload`. If no explicit
payload list exists, it classifies the task by role, task type, route label,
and implementation receipt as one process-only or controlled support class.

The main density values are:

- `payload_density`: mathematical payload items divided by all classified
  items.
- `task_payload_density`: tasks with at least one mathematical payload item
  divided by all completed tasks in the group.

## Required Grouping Dimensions

The report must group by:

- phase;
- task family;
- role;
- milestone.

The milestone field is read from `physics_progress_status`,
`distance_to_gr_delta`, or the AgentJob target milestone. Non-physics control
packets use `none` when no derivation milestone is applicable.

## Authority Boundary

Every machine-readable report must state that the metric is operational
diagnostics only and that it does not authorize physics proof, source-law
adoption, benchmark promotion, or completed-derivation claims. A high density
does not make a theorem true. A low density does not make a research route
false. The metric only helps operators see when work is mathematical payload,
route selection, validation/tooling, or documentation.

## Limitations

This metric is conservative. Payloads inherit the claim status already present
in their completion record. Draft/control payload remains draft/control, and
source-extension classifications remain status classifications unless a
separate protected gate authorizes adoption.
