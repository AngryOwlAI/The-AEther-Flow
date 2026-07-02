<!-- authority: science_draft -->

# P2-T01 Theorem Packet Setup

## Packet Identity

- Plan: `recommendations_implementation_plan_continue_task-v15`
- Plan tasks: `P2-T01` and `P2-T02`
- Task: `RT-20260702-057`
- AgentJob: `AJ-RT-20260702-057-001`
- Role: `ontology-formalizer@0.2.0`
- Theorem candidate name: `NarrowMSCertEq_v1`
- Theorem target: source-side matter-semantics equivalence under explicit
  source certificates.
- Target derivation milestone: `matter_coupling`
- Milestone burden: source-side matter-semantics equivalence theorem under
  explicit source certificates only; no matter-semantics adoption and no
  coupling-law adoption.

This setup is draft/control theorem scaffolding. It is not a proof and not an
adoption packet.

## Allowed Source-Side Inputs

The P2-T03 theorem attempt may use only tracked source-side evidence and
preconditions within their exact scopes:

| Input | Allowed use | Authority path |
| --- | --- | --- |
| `MSStableMatterSemanticsBridge_v1` | scoped stable matter-semantics bridge evidence/precondition | `research_control/tasks/RT-20260630-056/artifacts/ms_stable_matter_semantics_bridge_source_extension_evidence_gate_chair_review_v1.tex` |
| `SourceMatterSemanticsAdoptionReadinessLaw_v1` | scoped adoption-readiness evidence/precondition, not adopted law | `research_control/tasks/RT-20260701-009/artifacts/source_matter_semantics_adoption_readiness_law_evidence_gate_chair_review_v1.tex` |
| `PositiveMSProfile_v1` | scoped positive source-matter-semantics profile evidence/precondition, not adopted profile | `research_control/tasks/RT-20260701-020/artifacts/positive_source_matter_semantics_profile_gate_chair_review_v1.tex` |
| `RR_ETransportCompletenessOrInvarianceLaw_v1` | scoped certificate-indexed `RR_E` transport/invariance evidence/precondition, not source law | `research_control/tasks/RT-20260701-030/artifacts/rr_e_transport_law_gate_chair_review_v1.tex` |
| MCPA evidence/precondition | scoped matter-coupling precondition evidence only | `research_control/tasks/RT-20260630-013/artifacts/matter_coupling_precondition_assembly_source_extension_evidence_gate_chair_review_v1.tex` |
| Source-coupling-law candidate evidence | scoped source-extension coupling-law-candidate evidence only | `research_control/tasks/RT-20260630-020/artifacts/source_coupling_law_candidate_source_extension_evidence_gate_chair_review_v1.tex` |
| no-target-import hygiene | negative source-purity guard only | `research_control/design/no_target_import_guard_map.md` |

Generated wiki notes, current-frontier rendering, dependency graphs, registry
rows, validator PASS, role identity, handoff status, approval status, local
caches, file order, and commit state are not theorem premises.

## Theorem Candidate Shape

P2-T03 should attempt a theorem with the following controlled form:

```text
Given declared source-side matter-semantics objects A_src and B_src,
and given explicit source certificates C_transport, C_invariance,
or C_factorization satisfying no-target-import and RR_E separation guards,
A_src and B_src are equivalent under Eq_MS_src only within the declared
source-side scope.

If required certificates are absent, malformed, object-mismatched,
target-importing, detector-semantic, benchmark-dependent, or process-authority
dependent, the equivalence fails closed and preserves RR_E separation or the
named obstruction.
```

Task-local symbols and definitions are fixed in
`source_side_matter_semantics_object_certificate_manifest_v1.tex`.

## Certificate Classes

The theorem attempt may use only these certificate classes:

- `SourceTransportCertificate`
- `SourceInvarianceCertificate`
- `SourceFactorizationCertificate`
- `NoTargetImportCertificate`
- `DeclaredObjectCertificate`
- `FailClosedCertificateMissing`

Certificate assertions must be explicit. A citation to an accepted scoped
evidence/precondition object is not by itself a certificate.

## Equivalence Relation Target

The relation target is `Eq_MS_src^cert`, a certificate-indexed source-side
equivalence relation. It is not detector equivalence, stress-energy
equivalence, matter-action equivalence, empirical equivalence, benchmark
equivalence, or coupling-law equivalence.

## Fail-Closed Branches

P2-T03 must fail closed under at least these branches:

| Branch | Required effect |
| --- | --- |
| missing certificate | no equivalence; preserve `RR_E` separation or name certificate-gap obstruction |
| malformed certificate | no equivalence; name malformed certificate class |
| declared-object mismatch | no equivalence; preserve object-indexed separation |
| target import | no equivalence; route to smuggling audit or fail-closed obstruction |
| detector-semantics import | no equivalence; detector semantics remain blocked |
| benchmark behavior import | no equivalence; benchmark promotion remains blocked |
| process-authority import | no equivalence; validator/registry/handoff/approval status remains non-proof |
| scoped evidence as adoption | no equivalence; evidence/precondition remains scoped |

## Expected Output Statuses

P2-T03 may return exactly one of:

- `conditional_or_scoped_source_side_equivalence_theorem_candidate`
- `certificate_gap_obstruction`
- `finite_countermodel_obstruction`
- `source_equivalence_under_current_premises_not_derived`
- `route_freeze_candidate`

No output may be rendered as bare `accepted`.

## Forbidden Target Imports

The theorem attempt must not import:

- target manifold, target topology, target atlas, target coordinate charts, or
  differentiability class;
- target Lorentzian metric, metric signature, proper time, or metric data;
- empirical detectors, clocks, rods, calibration procedures, or detector
  semantics;
- stress-energy tensor, stress-energy semantics, conservation law, or matter
  action;
- coupling-law adoption or universal matter-coupling conclusion;
- Einstein equations, exact-GR benchmark behavior, benchmark fit, or completed
  derivation;
- generated derivatives, registry rows, validation success, role identity,
  handoff status, approval status, local caches, file order, or commit state
  as proof authority.

## Validators To Run

Minimum validators after P2-T03:

```zsh
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py
.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only
.venv/bin/python scripts/project_control/validate_documentation_impact.py --json
.venv/bin/python scripts/project_control/validate_claim_language.py --changed --json
.venv/bin/python scripts/research_control/validate_research_control.py
.venv/bin/python scripts/research_control/validate_research_control.py --check-diff
.venv/bin/python scripts/research_control/render_current_frontier.py --check
.venv/bin/python scripts/research_control/render_dependency_graph.py --check
git diff --check
```

## Completion Handoff Shape

The P2-T03 completion should include:

- theorem or obstruction status;
- `physics_progress_status`;
- `distance_to_gr_delta`;
- `distance_to_gr_status`;
- `mathematical_payload_manifest`;
- `forbidden_conclusion_summary`;
- `parent_child_synthesis`;
- `no_target_import_audit_scope`;
- exact next route to P2-T04, P2-T05, P2-T06, repair, or obstruction path.

## Boundary Conclusion

This setup fixes the theorem packet boundary and source vocabulary. It does
not prove `NarrowMSCertEq_v1`, does not identify `RR_E` records without
certificates, does not adopt source law, does not adopt matter semantics, does
not define detector semantics, does not adopt a coupling law, does not derive
or adopt matter coupling, does not import stress-energy semantics or matter
action, does not derive Einstein equations, does not promote benchmark status,
and does not claim completed derivation.
