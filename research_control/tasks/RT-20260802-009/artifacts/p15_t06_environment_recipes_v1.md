---
authority: control
artifact_id: P15-T06-ENVIRONMENT-RECIPES-V1
status: internal_release_candidate
plan_task_id: P15-T06
created_at: 2026-08-02T14:32:33Z
publication_authorized: false
physics_promotion_authorized: false
---

# P15-T06 environment and clean-room recipes

These recipes reproduce four internal publication candidates from exact source
snapshots. They do not edit canonical sources or authorize external release.

## Bound archives

| Candidate | Archive | Source snapshot |
| --- | --- | --- |
| P15-T01 | `research_control/tasks/RT-20260802-009/artifacts/p15_t01_exact_gr_interpretive_source_bundle_v1.tar` | `ef41c569efd01f3a5182f114c20dd6edb3ee9973` |
| P15-T02 | `research_control/tasks/RT-20260802-009/artifacts/p15_t02_ai_methodology_source_bundle_v1.tar` | `9be11e9cc77a8ab30776fd5598b682b37c42a6e3` |
| P15-T03 | `research_control/tasks/RT-20260802-009/artifacts/p15_t03_selector_theorem_source_bundle_v1.tar` | `1136e88b329fa9215017a20dd030607a98168503` |
| P15-T04 | `research_control/tasks/RT-20260802-009/artifacts/p15_t04_source_dynamics_source_bundle_v1.tar` | `832f9cf9ba98061df40cdda2799d5a46661260bc` |

## Runtime

Use CPython 3.12. The project metadata requires `>=3.12,<3.13`. Exact runtime
and quality dependencies are recorded in the two bundled hash locks:

- `research_control/tasks/RT-20260723-019/artifacts/requirements.lock`
- `research_control/tasks/RT-20260724-002/artifacts/quality-assurance-requirements.lock`

From a clean directory, extract one archive and run:

```sh
tar -xf <archive>.tar
python3.12 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements-dev.txt
```

Then run the exact command in the archive's `REPRODUCE.md`. P15-T02 uses only
the Python standard library; the other candidate validators require PyYAML.
TeX compilation is outside this task: the packages validate tracked source and
evidence bytes, not generated PDF derivatives.

## Determinism and authority

Archive members are sorted and use fixed metadata (`mtime=0`, uid/gid zero,
mode `0644`). `PACKAGE_MANIFEST.json` binds every tracked member to a SHA-256
and exact Git commit. Later canonical-source evolution is not substituted into
older packages. Validator PASS remains operational evidence only.
