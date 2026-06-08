---
design_record_id: "DR-20260608-001"
title: "Director-Led AgentJob Control Spine Grill Decisions"
status: "active"
created_at: "2026-06-08T00:00:00Z"
authority_status: "project_control_design"
requires_references: true
source_inputs: "user grill session;old project research-control files;Flow AGENTS.md;Director-led reset plan"
related_task_id: "RT-20260608-001"
---

# Director-Led AgentJob Control Spine Grill Decisions

## Purpose

This design record summarizes the resolved grill decisions for the Flow
research-control reset. It is project-control/design authority, not scientific
authority.

## Architecture

The control spine follows this rule:

```text
Director chooses the research path.
Roles constrain execution.
Skills provide procedures.
Scripts validate boundaries.
Gates control claim promotion.
```

The old project's deterministic router discipline is retained as validation
and advisory precedent, but Flow does not make a Python router the sovereign
research authority.

## Artifact Layout

- Versioned role contracts live under `.agents/roles/`.
- Reusable schemas live under `.agents/schemas/`.
- Tracked tasks, DDRs, jobs, completions, approvals, and handoffs live under
  `research_control/`.
- Control registries live under `registries/`.
- `.local/` is scratch/cache only.

## Execution Policy

`/continue-research` resolves tracked state, creates or uses one bounded
AgentJob, validates it, and stops after completion/handoff. It must not run a
hidden multi-step research chain.

The first bootstrap task installs control infrastructure only. It does not open
a Gate 0 science task and does not port the old router.

## Role Policy

The first registered roles are Director of Research, Process Integrity Auditor,
Ontology Formalizer, Candidate Constructor, Refuter, Smuggling Auditor, and
Gate Chair. Gate Chair is defined but human-paused.

One-job provisional roles are allowed only as least-privilege overlays embedded
in a DDR and AgentJob. They expire after the job and are not reusable until a
human-gated role registration approves them.

## Validation Policy

Validation checks registry shape, role frontmatter agreement, DDR and AgentJob
consistency, handoff pairs, human-gate approval conventions, write-path
allowlists, and simple claim-boundary phrase scanning. `--check-diff` inspects
working-tree changes against the latest active or completed AgentJob.

## Claim Boundary

- Allowed: bootstrap/control-system implementation claims.
- Allowed: open derivation status.
- Forbidden: GR derived from ontology.
- Forbidden: exact GR recovered from ontology.
- Forbidden compatibility-only token: GR_DERIVED_FROM_ANTHOLOGY.
- Human/gate required: ontology promotion, benchmark promotion, Gate Chair
  verdicts, or any GR-derived claim.

## Next Research Step

After the bootstrap validates, the logical next action is a separate
`/continue-research` invocation where the Director creates a Gate 0 Ontology
Formalizer AgentJob if validation agrees.

## Engineering Traceability

- User-supplied plan: `/Users/alex.omegapy/.codex/attachments/9174c2bb-0e05-40cd-a6fd-c531da72d195/pasted-text.txt`
- Old project guidance: `/Volumes/P-SSD/AngryOwl/The Æther GR Derivation/AGENTS.md`
- Old router script: `/Volumes/P-SSD/AngryOwl/The Æther GR Derivation/scripts/research_control/run_next_role.py`
- Old program router: `/Volumes/P-SSD/AngryOwl/The Æther GR Derivation/scripts/research_control/program_router.py`
- Flow root guidance: `AGENTS.md`

## References

AngryOwlAI. (2026). *The Æther Research Program AGENTS guidance* [Repository guidance]. The Æther Research Program.

AngryOwlAI. (2026). *Research-control router implementation* [Repository script]. The Æther Research Program.

AngryOwlAI. (2026). *The Æther-Flow Interpretation of Relativity Research Project AGENTS guidance* [Repository guidance]. The Æther-Flow Interpretation of Relativity Research Project.

Ricciardi, A. S. (2026, June 8). *Director-led sub-agent architecture reset plan* [Unpublished internal design brief]. The Æther-Flow Interpretation of Relativity Research Project.
