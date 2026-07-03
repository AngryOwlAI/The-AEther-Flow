<!-- authority: control -->

# P12-T01 Claim Graph Schema Receipt

## Result

`RT-20260703-023` completed v15 P12-T01 by defining
`research_control/design/claim_graph_schema_v1.md`.

## Required Coverage

- Required node types: complete.
- Required edge types: complete.
- Promotion status field: present.
- Overread guard field: present.
- Validator receipt boundary: present.
- Generated derivative boundary: present.
- Validator receipt versus scientific proof distinction: explicit.
- Next route: P12-T02 claim graph generator pilot.

## Validation

Task-local validator:
`.venv/bin/python research_control/tasks/RT-20260703-023/artifacts/validate_p12_t01_claim_graph_schema.py --output research_control/tasks/RT-20260703-023/artifacts/p12_t01_claim_graph_schema_report.json --json`

Status: `PASS`.

## Claim Boundary

This receipt is operational project-control evidence only. It does not make
the schema a physics source, proof authority, source-law adoption, matter
semantics, detector semantics, coupling-law adoption, matter coupling,
`MetricData(E)`, `g_eff`, stress-energy semantics, a stress-energy tensor, a
matter action, a variation principle, Einstein equations, benchmark promotion,
Gate Chair verdict, completed derivation, program-wide no-go conclusion, or
future source-extension impossibility.
