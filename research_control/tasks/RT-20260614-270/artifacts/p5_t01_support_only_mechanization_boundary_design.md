<!-- authority: control -->

# P5-T01 Support-Only Mechanization Boundary Design

## Purpose

This artifact completes P5-T01 of
`implementations_plans/recommendations_implementation_plan_continue_task-v11.md`.
It defines the support-only mechanization boundary for finite/local source-side
checker work after `ParamFiniteLocalWitness_v1(E)`, `BridgeSlot_n(E)`, and
`NoTargetImport_n` were accepted only as scoped source-extension
parameterized-witness evidence/precondition.

The design is a project-control contract for P5-T02. It does not implement the
checker.

## Boundary Statement

This mechanized report is support-only scaffolding. It is not proof authority,
not source-law adoption, not `MetricData(E)` adoption, not `g_eff` adoption or
scope expansion, not matter coupling, not stress-energy semantics, not a
stress-energy tensor, not a matter action, not Einstein equations, not
benchmark promotion, and not completed derivation.

The same boundary also blocks coupling-law adoption, detector semantics,
canonical ontology edits, benchmark Gate Chair closure, downstream GR
promotion, future source-extension impossibility claims, and global theory
rejection.

## Local Precedents

P5-T02 should reuse the repository's existing conservative checker posture:

- `scripts/research_control/finite_source_cover_model_checker.py` is the
  nearest script precedent. It uses deterministic finite checks and states that
  a pass is not proof, source-law adoption, `M_src` adoption, `g_eff`
  construction, or downstream GR authority.
- `tests/test_finite_source_cover_model_checker.py` is the nearest test
  precedent. It covers clean witness pass, target-import rejection,
  bottom/failure classes, and no false promotion flags.
- `research_control/tasks/RT-20260614-163/artifacts/finite_graph_witness_checker.py`
  is the nearest task-local checker precedent. It treats mechanization as
  scaffolding only.
- `research_control/design/finite_source_cover_model_checker.md` is the
  nearest registered design-note precedent.

## P5-T02 File Contract

P5-T02 should read:

- `research_control/tasks/RT-20260614-270/artifacts/p5_t01_support_only_mechanization_boundary_design.md`
- `research_control/tasks/RT-20260614-269/artifacts/298_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_P4_PARAMETERIZED_FINITE_LOCAL_SOURCE_FAMILY_WITNESS_V1_SOURCE_EXTENSION_EVIDENCE_GATE_CHAIR_REVIEW.tex`
- `scripts/research_control/finite_source_cover_model_checker.py`
- `tests/test_finite_source_cover_model_checker.py`
- `research_control/design/finite_source_cover_model_checker.md`

P5-T02 may write:

- `scripts/research_control/mechanized_checks/check_finite_local_candidate.py`
- `tests/fixtures/research_control/finite_local_candidate/*.yaml`
- `tests/test_finite_local_candidate_checker.py`
- `research_control/tasks/<P5-T02-task-id>/artifacts/finite_local_candidate_checker_report.json`
- `research_control/tasks/<P5-T02-task-id>/artifacts/finite_local_candidate_checker_report.md`
  if a human-readable report is useful

P5-T02 must not parse TeX as independent authority. TeX may be cited for
scoped claims and fixture provenance, but checker fixtures must be YAML or JSON
records with explicit source provenance.

## Input Fixture Contract

The checker should accept JSON and the repository YAML subset. A fixture should
contain these top-level sections:

- `metadata`: fixture id, source task ids, source artifact paths, scope,
  declared boundary statement, and fixture version.
- `source_family`: parameter set, sector names, finite/local scope marker, and
  declared bottom behavior.
- `source_objects`: finite token set, finite state set, object references, and
  declared source-side carriers.
- `relations`: balance predicate rows, flux ledger rows, restriction maps,
  morphism or relabeling maps, and bottom result rows.
- `boundary_markers`: no-target-import marker, bridge compatibility marker,
  scoped `g_eff` boundary marker, evidence-not-adoption marker, and
  process-authority-not-proof marker.
- `candidate`: candidate map, certificate object, obstruction labels, and
  controlled status vocabulary.
- `variation_relabeling`: finite variations, relabelings, expected invariant
  fields, and allowed fail-closed cases.
- `forbidden_imports`: explicit false values for target metric, target atlas,
  target topology, Lorentzian signature, proper time, stress-energy semantics,
  stress-energy tensor, matter action, detector semantics, Einstein equations,
  benchmark success, source-law adoption, `MetricData(E)` adoption, and
  `g_eff` adoption.

## Exact Predicates To Mechanize

P5-T02 should implement these predicates with deterministic result ordering:

- `fixture_is_finite`: every declared token, state, sector, map, relation, and
  variation has finite explicit support.
- `sectors_nonempty_or_bottom`: each required sector is nonempty unless a
  declared bottom branch explains the absence.
- `token_state_references_resolve`: every token and state reference resolves to
  a declared finite object.
- `balance_flux_closed_or_bottom`: balance rows and flux ledger rows close
  over declared finite supports or fail closed to bottom.
- `bottom_result_totality`: every bottom result has a controlled label,
  triggering input, and blocked overread.
- `no_target_import_keys_absent`: forbidden target-facing fields are absent or
  explicitly false.
- `bridge_compatibility_marker_declared`: bridge compatibility is marked as
  scoped source-extension evidence/precondition only.
- `scoped_geff_boundary_marker_blocks_adoption`: any `g_eff` marker states
  no adoption and no scope expansion.
- `evidence_not_adoption_marker_present`: accepted evidence cannot be read as
  source-law, `MetricData(E)`, `g_eff`, coupling-law, or matter-coupling
  adoption.
- `process_authority_not_proof_marker_present`: role, validator, registry,
  approval, handoff, commit, and local cache status cannot be read as proof.
- `relabeling_maps_are_bijections_on_declared_finite_sets`: each relabeling is
  a bijection on its declared finite domain and codomain.
- `restriction_maps_preserve_declared_references`: restriction maps preserve
  declared token and state references or fail closed.
- `finite_variations_have_allowed_results`: each finite variation either
  preserves required predicates or returns a controlled obstruction.
- `candidate_map_domain_codomain_declared`: candidate maps use declared finite
  domain and codomain objects only.
- `certificate_object_references_declared`: certificate objects reference only
  declared fixture objects and source artifacts.
- `obstruction_labels_from_controlled_vocabulary`: obstruction labels are
  controlled and do not invent scientific status.
- `report_disclaimer_exact_match`: every JSON and Markdown report carries the
  P5-T01 boundary statement exactly.
- `deterministic_output_order`: equivalent fixture input produces byte-stable
  JSON modulo path and timestamp fields if timestamps are included.

## Output Report Contract

The JSON report should include:

- `checker_id`
- `checker_version`
- `fixture_id`
- `fixture_hash`
- `status`
- `predicate_results`
- `obstruction_labels`
- `forbidden_overread_flags`
- `boundary_statement`
- `source_artifact_refs`
- `tooling_error`
- `physics_obstruction`

Controlled statuses:

- `pass_support_only`
- `fail_malformed_fixture`
- `fail_target_import`
- `fail_evidence_as_adoption`
- `fail_geff_overread`
- `fail_process_authority_overread`
- `fail_relabeling_invariance`
- `fail_variation_stability`
- `bottom`
- `tooling_error`

`tooling_error` means parser, schema, IO, dependency, or runtime failure. It is
not a physics obstruction. `physics_obstruction` may be nonblank only when a
well-formed fixture reaches a controlled source-side obstruction label. Even
then, it is a fixture-local support result and not a global theorem or
scientific stop.

## Fail-Closed Rules

The checker must reject:

- hidden target metric, target atlas, target topology, Lorentzian signature,
  proper-time, detector, matter-action, stress-energy, Einstein-equation, or
  benchmark fields;
- any report text that treats accepted evidence as adoption;
- any report text that treats a checker pass as proof authority;
- any report text that treats project-control authority as mathematical proof;
- any `g_eff` marker that claims adoption or scope expansion; and
- malformed fixtures whose unresolved references could hide target imports.

Failure of the checker or fixture schema is a tooling/data-quality failure.
Only a later bounded physics packet may decide whether a checked fixture result
is useful evidence, obstruction evidence, repair guidance, or irrelevant.

## P5-T02 Acceptance Criteria

P5-T02 is complete only if it:

- implements `scripts/research_control/mechanized_checks/check_finite_local_candidate.py`;
- adds YAML fixtures under
  `tests/fixtures/research_control/finite_local_candidate/`;
- adds tests covering bottom completeness, nonempty output, no-target-import
  rejection, evidence-as-adoption rejection, scoped `g_eff` overread
  rejection, process-authority-as-proof rejection, relabeling invariance,
  finite variation stability, malformed fixture failure, and deterministic
  output;
- emits at least one deterministic JSON report from a valid fixture;
- confirms all report outputs contain the exact boundary statement; and
- preserves all no-adoption and no-downstream-GR claim fences.

## Handoff

The logical next continue-research packet is P5-T02 with
`validator-engineer@0.2.0`, scoped only to implementing the checker model,
fixtures, tests, and one support-only report. P5-T02 must not implement P5-T03
as a separate test-hardening packet beyond the tests needed to verify its own
implementation.

## References

The AEther-Flow Research Project. (2026, June 23). *Finite source-cover model
checker* [Internal control note].

The AEther-Flow Research Project. (2026, June 28). *Handoff 0302* [Internal
control handoff].

The AEther-Flow Research Project. (2026, June 28). *P4 parameterized
finite/local source-family witness v1 source-extension evidence Gate Chair
review* [Internal research-control artifact].

The AEther-Flow Research Project. (2026, June 28). *Recommendations
implementation plan continue task v11* [Internal implementation plan].
