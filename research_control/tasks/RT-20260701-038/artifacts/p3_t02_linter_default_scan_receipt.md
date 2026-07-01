# P3-T02 Default Scan Receipt

## Command

```text
.venv/bin/python -c 'from scripts.project_control import validate_claim_language as v; r=v.validate_paths(); print(r["status"], r["hard_fail_count"], r["warning_count"])'
```

## Result

The default repository scan reported:

- status: `FAIL`
- hard-fail findings: `129`
- warning findings: `2879`
- total findings: `3008`
- scanned paths: `2332`
- `research_control/current_frontier.md`: `PASS`

## Interpretation

This is an implementation receipt, not remediation. The hard-fail backlog is concentrated in older implementation plans and current design or public explanatory surfaces. The v14 plan already assigns integration to P3-T03 and remediation to P3-T04. This packet therefore records the backlog and routes to P3-T03 without widening into remediation.

## Boundary

No public status propagation, current-public remediation, source-law adoption, matter-coupling promotion, Einstein-equation claim, benchmark promotion, or completed-derivation claim is made by this scan.
