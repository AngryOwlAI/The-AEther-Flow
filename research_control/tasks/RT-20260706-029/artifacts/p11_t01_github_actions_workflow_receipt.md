<!-- authority: control -->

# P11-T01 GitHub Actions Workflow Receipt

## Scope

This receipt covers only v17 `P11-T01`:

- create `.github/workflows/project-control-validation.yml`;
- run project-control validation through the existing Makefile entrypoint in a
  CI-created virtual environment;
- run a separate read-only memory validation job;
- preserve that CI and validator results are operational receipts only.

## Result

The workflow contains two required jobs:

- `validate_project_control`, which installs dependencies and runs
  `make PYTHON=.venv/bin/python validate-project-control`;
- `validate_memory_read_only`, which installs dependencies and runs
  `.venv/bin/python .codex/skills/project-memory-system/scripts/bootstrap_memory_system.py --validate-only`.

The workflow uses read-only repository permissions and does not commit
generated artifacts, write `.local/` cache outputs, or promote any physics
claim.

## Validation

The task-local validator is
`research_control/tasks/RT-20260706-029/artifacts/validate_p11_t01_github_actions_workflow.py`.

Its report path is
`research_control/tasks/RT-20260706-029/artifacts/p11_t01_github_actions_workflow_report.json`.

## Claim Boundary

No physics delta.

This packet does not authorize:

- CI or validation as physics proof authority;
- canonical ontology edit;
- source-law adoption;
- `MetricData(E)` adoption;
- `g_eff` scope expansion;
- matter-semantics adoption;
- detector-semantics adoption;
- coupling-law adoption;
- matter-coupling derivation or adoption;
- stress-energy semantics;
- stress-energy tensor;
- matter action;
- Einstein equations;
- benchmark promotion;
- Gate Chair verdict;
- completed derivation.

## Next Route

`P11-T01` is complete after this packet. The next lawful route is one bounded
v17 `P11-T02` Python environment and reproducibility documentation packet.
