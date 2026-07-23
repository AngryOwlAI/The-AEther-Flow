<!-- authority: control -->

---
authority: control
status: blocked_validation
handoff_id: handoff-0833
task_id: RT-20260722-024
job_id: AJ-RT-20260722-024-001
---

# Handoff 0833: classifier recovery complete; repository shard blocked

`RT-20260722-024` adds one literal classifier predicate for repository-root
`.gitattributes`. That exact path now belongs to the existing
`ci_orchestration` family and selects an affected `READY` validation plan. No
prefix, suffix, general dotfile, or Git-policy wildcard was added.

The focused classifier and planner regressions pass, as does the broader
102-test classifier, planner, and checkpoint integration suite. An unrelated
governed path remains `unknown_governed_path` and falls back to the full
validation profile. The four literal Git whitespace rules and every protected
P15-T01 hash remain unchanged. The P15-T01 package still passes all 161
task-local checks.

The one normal generation-65 governed checkpoint was invoked exactly once.
It reached the full 1,172-test repository shard and stopped safely with two
failures and one cascading setup error. `RT-20260722-022` through
`RT-20260722-024` use invalid v21 task-taxonomy vocabulary, and the P10-T05
event-store receipts seal an older
`scripts/research_control/report_physics_progress_metrics.py` source hash.
Nothing was staged or committed, the index was restored, and legacy
validation was not used.

The next lawful execution is one fresh bounded `improve-project-system`
recovery. It must normalize only those three recovery-task taxonomies to valid
existing vocabulary, inspect and repair the P10-T05 sealed source-hash
receipts under their existing authority, preserve the classifier repair and
protected P15-T01 bytes, and invoke one future normal checkpoint. The
ordinary-route selection of P15-T03 remains conditional on that future
checkpoint commit.

This blocked result changes no scientific claim, ontology, ledger,
Distance-to-GR status, event-store cutover authority, external-review status,
publication authority, proof authority, or completed-derivation status.

- Handoff ID: `handoff-0833`
- Source task: `RT-20260722-024`
- Source job: `AJ-RT-20260722-024-001`
- Completion: `AJC-AJ-RT-20260722-024-001`
- Recovered plan task: `P15-T01`
- Immediate recovery work item: `P15-T01`
- Immediate recovery worker skill: `improve-project-system`
- Immediate recovery strategy: `normalize_recovery_task_taxonomy_and_reseal_p10_t05_source_hash_v1`
- Conditional ordinary-route selection after recovery: `P15-T03`
