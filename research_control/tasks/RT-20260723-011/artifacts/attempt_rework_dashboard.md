---
authority: control
status: draft/control
task_id: RT-20260723-011
plan_task_id: P12-T06
generated_from: attempt_rework_dashboard.json
---

# Attempt, rework, and PASS-saturation dashboard

This dashboard is a deterministic projection of the sealed P10-T04 attempt-event ledger. It describes a bounded operational sample, not complete project history or physics evidence.

## Bounded event mix

| Measure | Count |
|---|---:|
| Observed attempt starts | 1 |
| Validation catches | 1 |
| Audit objections | 1 |
| Repair events | 2 |
| Explicit abandoned events | 0 |
| Completed event types | 2 |
| Superseded events | 1 |

## Failure categories

| Typed category | Count |
|---|---:|
| Syntax | 0 |
| Validation | 1 |
| Proof | 0 |
| Interpretation | 1 |
| Physics | 0 |

Categories use typed event fields only; no summary prose is mined. A validation catch or audit objection is not a physics refutation.

## Repair and saturation context

- Repair-event share: 2/8 = 0.2500.
- Repair events per recorded issue: 2/2 = 1.0000; this is a count ratio, not causal closure.
- Median repairs per represented task: 0.0.
- Median repairs per task with a repair: 1.0.
- Abandonment rate: `not_measured`. The ledger records one explicit bounded absence but does not define a complete closed-attempt population; zero observed abandoned events must not be overread as a zero abandonment rate.
- PASS-like disposition share: 4/8 = 0.5000. This is operational saturation context only.

## Final dispositions

| Disposition | Count |
|---|---:|
| `active` | 1 |
| `blocked` | 1 |
| `completed` | 4 |
| `finding_recorded` | 1 |
| `superseded` | 1 |

## By task

| Task | Events | Starts | Validation | Audit | Repairs | Completed |
|---|---:|---:|---:|---:|---:|---:|
| `RT-20260712-005` | 1 | 0 | 0 | 0 | 0 | 0 |
| `RT-20260712-007` | 1 | 0 | 0 | 0 | 0 | 1 |
| `RT-20260720-001` | 2 | 1 | 1 | 0 | 0 | 0 |
| `RT-20260720-002` | 1 | 0 | 0 | 0 | 1 | 0 |
| `RT-20260720-003` | 1 | 0 | 0 | 0 | 0 | 1 |
| `RT-20260720-004` | 1 | 0 | 0 | 0 | 1 | 0 |
| `RT-20260720-009` | 1 | 0 | 0 | 1 | 0 | 0 |

## By role

| Role | Events | Starts | Validation | Audit | Repairs | Completed |
|---|---:|---:|---:|---:|---:|---:|
| `project-control-maintainer` | 6 | 1 | 1 | 0 | 1 | 2 |
| `smuggling-auditor` | 1 | 0 | 0 | 1 | 0 | 0 |
| `validator-engineer` | 1 | 0 | 0 | 0 | 1 | 0 |

## By work kind

| Work Kind | Events | Starts | Validation | Audit | Repairs | Completed |
|---|---:|---:|---:|---:|---:|---:|
| `audit_or_refutation` | 1 | 0 | 0 | 1 | 0 | 0 |
| `construction_or_implementation` | 2 | 0 | 0 | 0 | 2 | 0 |
| `integration_or_selection` | 5 | 1 | 1 | 0 | 0 | 2 |

## By candidate family

| Candidate Family | Events | Starts | Validation | Audit | Repairs | Completed |
|---|---:|---:|---:|---:|---:|---:|
| `EQSRC-CANONICAL-CHOICE-GRADED-ORBIT-ROOT` | 1 | 0 | 0 | 1 | 0 | 0 |
| `not_applicable` | 7 | 1 | 1 | 0 | 2 | 2 |

## Authority and privacy

The projection excludes event summary text, prompt text, private reasoning, credentials, and personal data. Source hashes and deterministic freshness metadata permit drift detection. No count or PASS-like share changes scientific status, Distance-to-GR, ontology, proof, benchmark, publication, or promotion authority.
