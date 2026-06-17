<!-- authority: control -->

# HTML Teaching Loop Recommendation Audit

Task: `RT-20260617-004`

Source recommendation:
`implementations_plans/recommendations_HTML_improvement_teaching_loop.md`

## Coverage Matrix

| Recommendation | Implementation evidence | Verification |
| --- | --- | --- |
| Keep Documentation Curator as the only documentation writer while adding Student and Teacher support roles. | `.agents/roles/research_ops/documentation-curator.v0.8.0.md`, `.agents/roles/research_ops/documentation-student.v0.1.0.md`, `.agents/roles/research_ops/documentation-teacher.v0.1.0.md`, and `registries/AGENT_ROLE_REGISTRY.csv`. | `scripts/research_control/validate_research_control.py` checks role registry and frontmatter consistency. |
| Add project custom-agent files for Student and Teacher. | `.codex/agents/documentation-student.toml` and `.codex/agents/documentation-teacher.toml`. | File presence plus check-diff allowlist coverage. |
| Add a Teaching Q&A packet schema. | `.agents/schemas/TEACHING_QA_PACKET_SCHEMA.md`. | `scripts/validate_teaching_qa.py --root .`. |
| Treat Teaching Q&A packets as explanatory support only. | `markdown/teaching-packets/role-routing.teaching-qa.md`, bootstrap registration for `teaching_qa_packet`, and README authority notes. | `tests/test_memory_system.py` and bootstrap validation. |
| Extend HTML source specs with optional `teaching_loop` metadata and Teaching Q&A Basis. | `markdown/html-explainer-specs/role-routing-explainer.md`. | `scripts/validate_teaching_qa.py --root .` and `scripts/spec_depth_lint.py --root .`. |
| Add richer teaching blocks for HTML and GitHub-facing outputs. | `html/role-routing-explainer.html` and `github-facing/role-routing-explainer.md` include glossary, guided walkthrough, common questions, examples, misconceptions, boundaries, understanding checks, and next steps. | `scripts/spec_depth_lint.py --root .`, bootstrap validation, and unit tests. |
| Add a teaching validator. | `scripts/validate_teaching_qa.py` and `tests/test_validate_teaching_qa.py`. | Unit tests and direct validator run. |
| Extend `spec_depth_lint.py` for teaching-enabled explainers. | `scripts/spec_depth_lint.py` and `tests/test_spec_depth_lint.py`. | Unit tests and direct lint run. |
| Add a repo-scoped `aether-teaching-explainer` skill. | `.codex/skills/aether-teaching-explainer/SKILL.md`. | Bootstrap registration and check-diff allowlist coverage. |
| Use role routing as the exemplar. | `markdown/teaching-packets/role-routing.teaching-qa.md`, `markdown/html-explainer-specs/role-routing-explainer.md`, `html/role-routing-explainer.html`, and `github-facing/role-routing-explainer.md`. | Teaching validator, depth lint, bootstrap validation, and generated derivative registry updates. |
| Route phase one through Project-Control Maintainer or Project-System Director. | `DDR-20260617-004.md`, `AJ-RT-20260617-004-001.yaml`, and `ROLE_EXECUTION_REGISTRY.csv`. | Research-control validation and check-diff. |
| Do not batch-roll out every explainer cluster in this transaction. | Only the role-routing exemplar is migrated. | Audit of changed spec and generated HTML paths. |

## Boundary Confirmation

This task does not alter canonical science sources, ontology files, physics
benchmark status, or Gate Chair authority. The teaching packet is explanatory
support for future Documentation Curator work and is not canonical authority.
