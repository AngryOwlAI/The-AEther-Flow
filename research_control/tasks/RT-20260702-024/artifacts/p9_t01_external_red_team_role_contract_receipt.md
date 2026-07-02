<!-- authority: control -->

# P9-T01 External Red-Team Role Contract Receipt

## Summary

RT-20260702-024 updates `external-red-team-reviewer@0.1.0` for the v14 P9-T01
role-contract packet. The update makes the role explicitly able to challenge
process-authority laundering, evidence-as-adoption laundering, no-target
certificate overread, `RR_E` separation collapse, and authorized literature
comparison.

The update is non-promotional. The role remains critique and routing evidence
only, with `may_promote_claims=false`, `may_modify_sources=false`, and ordinary
execution `requires_human_gate=false`.

## Boundary

The packet does not authorize:

- physics object adoption or rejection;
- Gate Chair verdicts;
- canonical source override;
- source-law adoption;
- `MetricData(E)` adoption;
- `g_eff` adoption or scope expansion;
- matter-coupling derivation or adoption;
- stress-energy semantics, stress-energy tensor, detector semantics, or matter
  action;
- Einstein equations;
- benchmark promotion;
- completed derivation;
- global no-go claims without a precise routed theorem artifact.

## Validation

Task-local validator:

```text
.venv/bin/python research_control/tasks/RT-20260702-024/artifacts/validate_p9_t01_external_red_team_role_contract.py --output research_control/tasks/RT-20260702-024/artifacts/p9_t01_external_red_team_role_contract_report.json --json
```

Result: `PASS`.

Receipt hashes:

- role contract:
  `b49de89caa4cb4f98f959e0ba7168a8223797679e5d0ab3c4700c14a5de9ace7`
- role design:
  `7d8ab21c7a31d7e69aaafd5cc3ac74146d919cfa62ab936a8e6dc496321177c7`
- approval:
  `da5a2e9df5a353aa1e396b4d3d3112ff77a9ad1f575760cbd8bd08ad8cded74c`
- role registry:
  `b38dc3350abb4ca060b93ac19983f596fd1d3f7c12e00635a68ed60915014df6`
- validator script:
  `67383ee38ecca8f3c0fa374532b522b154fb35fec37f4552e7bcdafd03d150a6`
- validator report:
  `2fdf3cc4f131eb3f4fc132bae3711b165d0a8d63adb25697c5a7f80853749c72`

## Next Route

The logical next packet is P9-T02: update the red-team review template before
any pilot review, selector, literature comparison, or downstream physics route.
