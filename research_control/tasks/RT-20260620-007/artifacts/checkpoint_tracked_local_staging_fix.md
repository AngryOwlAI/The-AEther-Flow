<!-- authority: control -->

# Checkpoint Tracked Local Staging Fix

## Analysis

The uncommitted file was:

`.local/content_semantics/markdown/md-schema-agent-job-schema.txt`

The file is a generated noncanonical content-semantic extract for
`MD-SCHEMA-AGENT-JOB-SCHEMA`. It is also already tracked by Git. The prior
checkpoint did not commit it because
`scripts/research_control/checkpoint_research_transaction.py` filtered every
path beginning with `.local/` out of `stageable_paths`.

That filter was too coarse. It correctly protected untracked `.local` scratch
output from accidental commits, but it also skipped tracked local generated
derivatives that the repository already manages. After the path-selection fix,
the checkpoint attempted to stage the tracked derivative but Git rejected the
normal `git add` because `.local/` is ignored. The staging operation therefore
also needed to force-add only the tracked `.local` subset.

## Fix

Checkpoint staging now:

- collects `.local/` paths from the changed path set;
- asks Git which of those `.local/` paths are tracked with `git ls-files`;
- stages tracked `.local/` paths;
- uses `git add -f` only for the tracked `.local` subset so ignored-directory
  rules do not leave tracked generated derivatives behind;
- continues to skip untracked `.local/` scratch caches.

The regression tests now distinguish a tracked local derivative from an
untracked local scratch file and verify the forced-add command is scoped to
the tracked local derivative path.

## Boundary

This repair does not make `.local` authoritative. `.local` remains retrieval
support and generated local state. The repair only makes checkpoint behavior
consistent with Git tracking: if a generated `.local` path is already tracked
and changed by the transaction, checkpoint should not leave it behind.

## Verification

Focused research-control tests passed. Full validation is recorded in the
completion receipt.

## Source Materials

The AEther-Flow Research Project. (2026, June 20). *AGENTS.md* [Internal
control guidance]. `AGENTS.md`

The AEther-Flow Research Project. (2026, June 20). *Research-control AGENTS.md*
[Internal control guidance]. `research_control/AGENTS.md`

The AEther-Flow Research Project. (2026, June 20). *AgentJob schema* [Internal
schema contract]. `.agents/schemas/AGENT_JOB_SCHEMA.md`
