<!-- authority: control -->

# P2-T04 skill obligation update review

## Scope reviewed

P2-T04 updates the validation-obligation wording in the `continue-research`,
`improve-project-system`, and `user-modified-project` skill contracts. It adds
one registered control policy that owns current compatibility recipes and one
focused parser test. It also records those three registered skill objects as
mutable preflight sources so new hashes do not invalidate historical receipts.
The active Project-Control Maintainer role contract and registry semantics were
inspected but not modified.

## Resolution

- Skills now name canonical gate obligations instead of repeating the common
  memory, documentation-impact, claim-language, and research-control recipe
  chain.
- The new policy maps each of nine named gates to one current compatibility
  recipe and states that role or skill declarations do not multiply executions.
- `research_control_diff` can satisfy `research_control_core` or
  `claim_language_changed` only under the respective registered same-scope
  predicate. The policy does not activate global planner supersedence.
- Working and staged evidence remain distinct. The governed checkpoint owns
  `checkpoint_transaction` and final staged acceptance; direct precheckpoint
  commands remain editing aids.
- Memory preflight and canonical-source inspection remain explicit retrieval
  requirements in the workflows that already own them.
- The validator's mutable-source set now includes the three edited skill object
  IDs. This preserves historical receipt identity while still requiring current
  hashes for immutable canonical sources; the coupled regression fixture proves
  both cases and the change affects no gate execution.

## Preserved role and authority boundary

The active `project-control-maintainer@0.2.0` registry row still has
`may_promote_claims=false`, `requires_human_gate=false`, and default validators
`validate_documentation_impact;validate_research_control;unittest`. No role
permission, validator implementation, Make target, CI workflow, checkpoint
behavior, ordinary research handoff, scientific source, or physics claim was
changed.

## Verification target

The focused test parses all three skill contracts and the policy table. It
rejects reintroduced direct core/diff recipe pairs, requires the named
obligation set and final staged checkpoint wording, checks memory-preflight and
checkpoint entry points, verifies one recipe per policy gate, and pins the
active role semantics. Broader project-control validation remains required
before checkpoint.
