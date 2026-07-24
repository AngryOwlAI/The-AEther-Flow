---
authority: "control"
schema_id: "p13_t05_security_scan_policy_v1"
status: "PASS"
task_id: "RT-20260724-002"
job_id: "AJ-RT-20260724-002-001"
claim_boundary_id: "CB-V21-P13-T05-ASSURANCE-001"
---

# P13-T05 security scan policy and disposition

## Scope

The dependency audit covers the exact hash-locked development environment in
`quality-assurance-requirements.lock`. The code scan covers the new assurance
evaluator, path-portability validator, governed checkpoint, and recursive goal
state helper.

pip-audit reported 50 dependencies and zero known vulnerabilities. Bandit
reported five low-severity findings, zero medium-severity findings, and zero
high-severity findings across 5,223 lines of selected code. Every reported
finding has an exact-key disposition in `security_dispositions.json`.

## Gate policy

Any dependency vulnerability requires an explicit disposition. Any
undispositioned high-severity Bandit finding blocks the gate. Lower-severity
Bandit findings remain visible and require task-local review even though they
do not independently block the reusable high-severity CI gate.

The scan is a current metadata and static-analysis observation. It does not
prove the absence of vulnerabilities and creates no scientific, proof,
publication, or promotion authority.

## Commands and raw evidence

```text
.venv/bin/python -m pip_audit --require-hashes -r requirements-dev.txt -f json -o .local/assurance/pip-audit.json
.venv/bin/python -m bandit -q -f json -o .local/assurance/bandit-full.json scripts/validation/assurance.py scripts/validation/portability.py scripts/research_control/checkpoint_research_transaction.py .codex/skills/continue-research-goal/scripts/goal_state.py
```

- pip-audit raw SHA-256:
  `a75f90066bf8a9c2b9524e27868bd491b0fef6a4c1488788dd34b37b0acba2d7`
- Bandit raw SHA-256:
  `c95feb24fe7b52043918ded623d0c86315755f7503bb229ff3a16e8dd0faa513`
- pip-audit version: `2.10.1`
- Bandit version: `1.9.4`

## Finding dispositions

| Finding | Location | Disposition |
| --- | --- | --- |
| `B105` | `goal_state.py:115` | False positive: a finite-state phase label, not a credential. |
| `B105` | `goal_state.py:1629` | False positive: absent-token initialization, not a credential. |
| `B404` | `checkpoint_research_transaction.py:13` | Required module for governed command execution. |
| `B603` | `checkpoint_research_transaction.py:138` | Accepted bounded execution: argument vector, no shell, fixed working directory, captured output, and separate transaction controls. |
| `B101` | `checkpoint_research_transaction.py:1166` | Accepted low operational risk: internal compare-mode invariant, not a security boundary. |
