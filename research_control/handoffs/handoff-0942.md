<!-- authority: control -->

# Handoff 0942 — P15-T06 reproducibility packages

Status: `ready_after_checkpoint`.

`handoff-0942` records one bounded P15-T06 project-system packet controlled by
`handoff-0941` and immutable generation 225.

## Result

Four internal release-candidate archives now cover P15-T01 through P15-T04.
They bind 160 tracked members to exact Git commits and SHA-256 values, include
environment and license/notice instructions, and reproduce all four candidate
validators from clean extraction. The P15-T06 validator passes 47 of 47 checks.

P15-T01 and P15-T03 intentionally use their qualifying historical source
snapshots where later canonical files evolved. No historical evidence or
canonical science source was rewritten. Archive copies and generated manifests
remain noncanonical.

The tracked `LICENSE` grants CC-BY-4.0 for research/documentation and
Apache-2.0 for code/tooling, with attribution and third-party limits in
`NOTICES`. Its referenced standalone `LICENSES` texts are not tracked, so the
packages record that limitation, carry stable identifiers and official text
URLs, and remain internal until the protected release decision.

## Next action

Run the single governed checkpoint for `AJ-RT-20260802-009-001`. Then stop at
P15-T07. The user must explicitly identify each manuscript or package version
and each allowed submission, public-release, reviewer-contact, or outreach
action, together with authorship, embargo, reviewer-identity, and report-
publication limits. No P15-T07 AgentJob or external action is authorized now.

## Prohibited conclusions

- Validator PASS is operational reproducibility evidence, not theorem proof or physics evidence.
- The archives do not promote ontology, source laws, benchmarks, or completed derivation.
- No submission, public release, reviewer contact, outreach, publication, push, or hosted workflow is authorized.
