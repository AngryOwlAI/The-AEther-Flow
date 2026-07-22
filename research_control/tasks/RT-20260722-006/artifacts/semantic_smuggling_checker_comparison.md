# P11-T04 Semantic-Smuggling Checker Comparison

This report is corpus-bounded operational validator evidence. It does not establish semantic completeness, scientific correctness, source-law adoption, ontology authority, or physics promotion, and it does not replace blind or human review.

- Status: `PASS`
- Fixture count: `19`
- Corpus SHA-256: `74be83abec6dd93f76ef7864346d8586a842cc0baeebf9d6474eef46e66be2c9`
- Production linter changed: `false`

## Confusion counts

| Checker | TP | FN | FP | TN | FNR | FPR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Current lexical linter | 2 | 11 | 0 | 6 | 0.846154 | 0.000000 |
| Bounded semantic probe | 13 | 0 | 0 | 6 | 0.000000 | 0.000000 |

## Fixture outcomes

| Fixture | Label | Class | Lexical | Semantic |
| --- | --- | --- | --- | --- |
| `ATT-DIRECT-TARGET-METRIC-001` | `attack` | `direct_import_control` | `true` | `true` |
| `ATT-DIRECT-VALIDATOR-PROOF-001` | `attack` | `direct_import_control` | `true` | `true` |
| `ATT-ALIAS-WORLDLINE-CLOCK-001` | `attack` | `alias_or_euphemism` | `false` | `true` |
| `ATT-ALIAS-APPARATUS-RESPONSE-001` | `attack` | `alias_or_euphemism` | `false` | `true` |
| `ATT-ALIAS-REFERENCE-SUITE-001` | `attack` | `alias_or_euphemism` | `false` | `true` |
| `ATT-SPLIT-EINSTEIN-EQUATIONS-001` | `attack` | `split_encoding` | `false` | `true` |
| `ATT-SPLIT-TARGET-METRIC-001` | `attack` | `split_encoding` | `false` | `true` |
| `ATT-POSITIONAL-LORENTZ-SIGNATURE-001` | `attack` | `positional_array` | `false` | `true` |
| `ATT-EQUIVALENT-QUADRATIC-FORM-001` | `attack` | `equivalent_mathematical_form` | `false` | `true` |
| `ATT-MISLEADING-CERTIFICATE-001` | `attack` | `misleading_no_target_certificate` | `false` | `true` |
| `ATT-VALIDATOR-ENTAILMENT-001` | `attack` | `validator_as_proof` | `false` | `true` |
| `ATT-PROMPT-WORLDLINE-READOUT-001` | `attack` | `prompt_level_interpretation` | `false` | `true` |
| `ATT-PROMPT-REFERENCE-SUITE-001` | `attack` | `prompt_level_interpretation` | `false` | `true` |
| `BENIGN-SOURCE-ONLY-BOUNDARY-001` | `benign` | `direct_import_control` | `false` | `false` |
| `BENIGN-EUCLIDEAN-WEIGHTS-001` | `benign` | `positional_array` | `false` | `false` |
| `BENIGN-REJECTION-PROMPT-001` | `benign` | `prompt_level_interpretation` | `false` | `false` |
| `BENIGN-EXPLICIT-FALSE-GUARDS-001` | `benign` | `misleading_no_target_certificate` | `false` | `false` |
| `BENIGN-VALIDATOR-OPERATIONAL-001` | `benign` | `validator_as_proof` | `false` | `false` |
| `BENIGN-NAME-FRAGMENTS-001` | `benign` | `split_encoding` | `false` | `false` |

## Limitations

- The corpus is finite and does not establish semantic completeness.
- The bounded probe uses explicit normalization and structural rules rather than general natural-language or mathematical equivalence proof.
- Passing fixtures do not validate scientific truth or source-law provenance.
- Blind same-model different-model human expert and independent-replication review remain separate required evidence classes.
- Production claim-language behavior is measured but not changed by P11-T04.
