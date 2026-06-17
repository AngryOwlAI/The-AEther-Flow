# Parent-Child Research Roles Implementation Audit

## Recommendation Coverage

- Preserve one outer AgentJob instead of creating child AgentJobs: implemented in `AGENT_JOB_SCHEMA.md`, `EXECUTION_ROLE_SCHEMA.md`, `continue-research`, `continue_research.py`, and validator tests.
- Add optional `role_decomposition`: implemented as `parent_child_parallel_synthesis` version `0.1.0`.
- Require one parent and exactly two children: enforced by `validate_parent_child_decomposition`.
- Fix perspectives: parent `physicist_mathematician_philosopher`, children `physicist_mathematician` and `physicist_philosopher`.
- Keep decomposition non-authority-expanding: enforced by recursive rejection of role, source-class, allowlist, permission, claim-boundary, and human-gate authority keys inside `role_decomposition`.
- Require child output, conflict review, fusion notes, and fused output paths under the outer AgentJob allowlist: enforced by path validation.
- Require fused final output in old-style outputs: enforced against AgentJob `expected_outputs`, `AGENT_JOB_REGISTRY.csv` `output_paths`, and completion `output_paths`.
- Add machine-checkable conflict review format: implemented as `PARENT_CHILD_CONFLICT_REVIEW_TEMPLATE.yaml`.
- Add completion contract extension: implemented as `parent_child_synthesis` in `COMPLETION_TEMPLATE.yaml`.
- Reject PASS completions with unresolved blocking conflicts: enforced by `validate_parent_child_completion`.
- Preserve existing role-specific physics completion requirements: unchanged; parent-child validation composes with existing distance-to-GR, Refuter loop-risk, Ontology Formalizer payload, and Candidate Constructor bridge checks.
- Surface continuation policy: `continue_research.py` emits `parent_child_decomposition_policy`; the continue-research skill describes the mode.
- Add tests: `tests/test_research_control.py` covers valid decomposition, wrong child perspective, output outside allowlist, missing fused expected output, authority expansion, valid parent-child PASS completion, missing fused completion output, unresolved blocking conflict rejection, and continuation policy exposure.

## Verification Logic

The implementation keeps parent-child synthesis internal to one AgentJob. It
therefore preserves registry, checkpoint, handoff, and validator assumptions
that each AgentJob has exactly one execution-role record.

The validator treats the final fused artifact as the old-style output. Child
outputs and parent review artifacts remain supporting draft/control evidence
under the same task boundary.

## Citation

Anonymous. (2026). *Implementation plan: New parent-child research roles system*
[Implementation plan].
`implementations_plans/implementation_plan_new_parent_child_research_roles_system.md`.
