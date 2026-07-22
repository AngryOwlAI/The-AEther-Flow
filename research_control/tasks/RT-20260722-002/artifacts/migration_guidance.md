<!-- authority: control -->

# Non-destructive artifact-path migration guidance

## Governing rule

Historical paths remain in place. `P10-T07` authorizes no bulk rename, move,
redirect, registry rewrite, citation rewrite, history rewrite, or deletion.
Content-addressed references are introduced only for new task-local copies and
manifest aliases. Existing paths remain provenance inputs and remain readable.

## Prospective adoption sequence

1. Choose an authorized output root and a short stable leaf name.
2. Run the task-local linter on every proposed path as one candidate set so
   casefold collisions are visible.
3. Put the human title in metadata, not in the filename.
4. Write bytes atomically, compute the full SHA-256 digest, and store the full
   digest in both identity and reference fields.
5. Add one unique stable alias to a deterministic manifest.
6. Resolve the alias by reading the referenced bytes and recomputing the full
   digest.
7. Preserve the original source path and hash as provenance.
8. Run focused tests, research-control validation, documentation impact,
   memory synchronization, and the governed checkpoint.

## Existing long or nonportable paths

An existing path that violates the prospective policy is a historical finding,
not permission to alter it. Record the exact path, owning registry row, source
hash, inbound references, and platform limitation. A later migration needs a
separate tracked AgentJob that owns every affected registry and citation,
provides an explicit alias or compatibility map, proves byte identity, tests
all readers, and supplies rollback. Until that transaction checkpoints, the
old path remains canonical.

## Rollback

Before activation, discard only the new unreferenced candidate files through
the owning transaction. After activation, append a superseding manifest event
or tracked correction; do not mutate a finalized identity record in place.
Rollback never changes scientific status, ontology, benchmark authority, Gate
Chair authority, proof authority, or publication authority.

## Pilot boundary

The accompanying pilot copies three immutable `P10-T05` control artifacts into
task-local full-digest paths and records stable aliases. It does not replace the
source files, update their registries, switch a reader, activate the event
store, or establish a repository-wide migration.
