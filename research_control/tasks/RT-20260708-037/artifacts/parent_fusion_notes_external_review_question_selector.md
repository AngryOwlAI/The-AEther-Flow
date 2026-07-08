<!-- authority: science_draft -->

# External-Review Question Selector Parent Fusion Notes

## Control Status

```yaml
artifact_id: "parent_fusion_notes_external_review_question_selector"
artifact_type: "parent_child_synthesis"
task_id: "RT-20260708-037"
job_id: "AJ-RT-20260708-037-001"
plan_task_id: "P10-T01"
created_at: "2026-07-08T21:31:55Z"
target_derivation_milestone: "source_equivalence_eqsrc"
milestone_burden: "Select one focused external-review question from v18 theorem/countermodel results."
```

## Parent Resolution

Both child checks select `EqSrc_family_closure`. The selected question is:

```text
Does the conditional source-only EqSrc_T family-closure theorem candidate have
a valid path from record-local EqSrc witnesses to family-level closure without
adding or assuming a primitive equivalent to the supplied H1-H7 closure and
ledger structure, especially inverse closure, composition closure, RetainH for
H-retention, or GenH for H-generated families?
```

This is one question. It is not an external outreach event, not a request for
endorsement, and not a request for broad project review.

## Reasoning

The mathematical child emphasizes that P3-T02 supplies a conditional
family-closure theorem candidate only under H1-H7, while P3-T05 supplies
finite missing-inverse and missing-composition pressure plus ledger weakening
and extension pressure. The philosophical child emphasizes that an external
review question should be narrow, should not ask a reviewer to inspect the
whole project, and should not frame RetainH or GenH as adopted primitives.

The common resolution is to ask about the path from record-local EqSrc witness
data to family-level closure without smuggling in a primitive equivalent to the
missing closure or ledger structure.

## Alternatives Rejected

| Question family | Disposition | Reason |
| --- | --- | --- |
| `EqSrc_family_closure` | selected | It directly targets the P3 theorem/countermodel result and matches the required P10-T02 packet source path. |
| `RetainH_primitive_requirement` | not selected standalone | It is included as extension pressure, but standalone review risks premature primitive-adoption framing. |
| `GenH_primitive_requirement` | not selected standalone | It is included as extension pressure, but standalone review risks premature source-generation adoption framing. |
| `source_detector_readout_semantics` | deferred | Downstream readout semantics should not precede review of the source-equivalence family-closure gap. |
| `finite_toy_response_v2_tag_independence` | deferred | It is useful support evidence but not the most direct external-review target for P10. |

## Claim Boundary

The selected question does not discharge general `EqSrc`, adopt `RetainH`,
adopt `GenH`, adopt a source law, derive matter coupling, derive Einstein
equations, promote a benchmark, issue a Gate Chair verdict, authorize external
outreach, claim future source-extension impossibility, or claim completed
derivation.

## Next Route

The next route is P10-T02: write the external-review packet source spec at
`markdown/external-review-specs/eqsrc_family_closure_review_packet_spec_v1.md`.

## References

The AEther-Flow Research Project. (2026a). *Recommendations implementation
plan continue task v18* [Internal implementation plan].

The AEther-Flow Research Project. (2026b). *EqSrc family-closure Refuter
stress v1* [Research-control TeX artifact].
