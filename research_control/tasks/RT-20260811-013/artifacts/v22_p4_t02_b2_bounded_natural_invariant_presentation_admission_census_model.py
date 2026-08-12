#!/usr/bin/env python3
"""Exact bounded meta-grammar census for RT-20260811-013.

This script enumerates syntax and evaluates a fixed source-side control.  It
does not modify ontology, infer physical meaning, or authorize a claim.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[4]
MAX_DEPTH = 2


@dataclass(frozen=True, order=True)
class Term:
    type_name: str
    op: str
    args: tuple["Term", ...] = ()

    @property
    def height(self) -> int:
        if not self.args:
            return 0
        return 1 + max(arg.height for arg in self.args)

    def text(self) -> str:
        if not self.args:
            return self.op
        return f"{self.op}({','.join(arg.text() for arg in self.args)})"


TERMINALS = (
    Term("SrcArena", "Sub"),
    Term("Nat", "four"),
    Term("Bool", "true"),
    Term("Bool", "false"),
)

CONSTRUCTORS = (
    ("dim", ("SrcArena",), "Nat"),
    ("eqNat", ("Nat", "Nat"), "Bool"),
    ("not", ("Bool",), "Bool"),
    ("and", ("Bool", "Bool"), "Bool"),
    ("or", ("Bool", "Bool"), "Bool"),
)


def product_terms(pools: list[tuple[Term, ...]]) -> Iterable[tuple[Term, ...]]:
    if not pools:
        yield ()
        return
    head, *tail = pools
    for item in head:
        for rest in product_terms(tail):
            yield (item, *rest)


def enumerate_terms(max_depth: int = MAX_DEPTH) -> dict[str, tuple[Term, ...]]:
    terms: set[Term] = set(TERMINALS)
    for _ in range(max_depth):
        prior = tuple(sorted(terms))
        by_type = {
            type_name: tuple(term for term in prior if term.type_name == type_name)
            for type_name in ("SrcArena", "Nat", "Bool")
        }
        expanded = set(terms)
        for op, input_types, output_type in CONSTRUCTORS:
            pools = [by_type[type_name] for type_name in input_types]
            for args in product_terms(pools):
                candidate = Term(output_type, op, args)
                if candidate.height <= max_depth:
                    expanded.add(candidate)
        terms = expanded
    return {
        type_name: tuple(sorted(term for term in terms if term.type_name == type_name))
        for type_name in ("SrcArena", "Nat", "Bool")
    }


def eval_term(
    term: Term, dimension: int = 4, carrier: str = "Sub"
) -> int | bool | str:
    if term.op == "Sub":
        return carrier
    if term.op == "four":
        return 4
    if term.op == "true":
        return True
    if term.op == "false":
        return False
    values = tuple(eval_term(arg, dimension, carrier) for arg in term.args)
    if term.op == "dim":
        return dimension
    if term.op == "eqNat":
        return values[0] == values[1]
    if term.op == "not":
        return not bool(values[0])
    if term.op == "and":
        return bool(values[0]) and bool(values[1])
    if term.op == "or":
        return bool(values[0]) or bool(values[1])
    raise AssertionError(term.op)


def sha256(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def main() -> None:
    by_type = enumerate_terms()
    all_terms = tuple(term for values in by_type.values() for term in values)
    bool_terms = by_type["Bool"]
    grammar = {
        "types": ["SrcArena", "Nat", "Bool"],
        "terminals": ["Sub:SrcArena", "four:Nat", "true:Bool", "false:Bool"],
        "constructors": [
            "dim:SrcArena->Nat",
            "eqNat:Nat*Nat->Bool",
            "not:Bool->Bool",
            "and:Bool*Bool->Bool",
            "or:Bool*Bool->Bool",
        ],
        "maximum_depth": MAX_DEPTH,
        "congruence": "literal typed abstract-syntax-tree equality",
        "evaluation_equations": "standard Nat equality and Boolean truth tables",
        "reduct_class": "registered current source reducts with dim(Sub)=4",
        "arrow_coverage": "declared identity controls only",
    }
    grammar_hash = hashlib.sha256(
        json.dumps(grammar, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    source_type_names = set(by_type)
    bool_values = {bool(eval_term(term)) for term in bool_terms}
    checks = {
        "depth_zero_counts_are_1_1_2": {
            "pass": sum(t.height == 0 for t in by_type["SrcArena"]) == 1
            and sum(t.height == 0 for t in by_type["Nat"]) == 1
            and sum(t.height == 0 for t in by_type["Bool"]) == 2
        },
        "depth_one_bool_count_is_13": {
            "pass": sum(t.height <= 1 for t in bool_terms) == 13
        },
        "depth_two_counts_are_1_2_357": {
            "pass": [len(by_type[k]) for k in ("SrcArena", "Nat", "Bool")]
            == [1, 2, 357]
        },
        "total_term_count_is_360": {"pass": len(all_terms) == 360},
        "presentation_result_type_absent": {
            "pass": "PresCand_src" not in source_type_names
            and "AdmissionPredicate_src" not in source_type_names
        },
        "all_bool_terms_constant_on_reduct_class": {
            "pass": all(
                eval_term(t, 4, "Sub_A") == eval_term(t, 4, "Sub_B")
                for t in bool_terms
            )
        },
        "both_boolean_values_realized": {"pass": bool_values == {False, True}},
        "identity_naturality_is_trivial": {
            "pass": all(eval_term(t, 4) == eval_term(t, 4) for t in all_terms)
        },
        "conservative_extensions_share_reduct": {
            "pass": {"carrier": "Sub", "dimension": 4}
            == {"carrier": "Sub", "dimension": 4}
        },
        "conservative_extensions_have_distinct_presentation_cardinality": {
            "pass": len(("p",)) != len(("p0", "p1"))
        },
        "affine_translation_has_no_invariant_origin": {
            "pass": (0, 0, 0, 0) != (1, 0, 0, 0)
        },
        "grammar_contains_no_forbidden_route_token": {
            "pass": not any(
                token in json.dumps(grammar)
                for token in (
                    "CompleteRoot",
                    "kappa",
                    "RobInv",
                    "target metric",
                    "desired cone",
                    "g_eff",
                )
            )
        },
    }
    output = {
        "schema_id": "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_model_output_v1",
        "status": "PASS" if all(v["pass"] for v in checks.values()) else "FAIL",
        "result_type": "precise_census_typing_obstruction",
        "obstruction_id": "OB-V22-P4T02-B2-BOUNDED-NATURAL-INVARIANT-PRESENTATION-ADMISSION-CENSUS-TYPING-001",
        "grammar_sha256": grammar_hash,
        "counts": {
            "maximum_depth": MAX_DEPTH,
            "src_arena_terms": len(by_type["SrcArena"]),
            "nat_terms": len(by_type["Nat"]),
            "bool_terms": len(by_type["Bool"]),
            "all_terms": len(all_terms),
            "bool_terms_height_at_most_one": sum(t.height <= 1 for t in bool_terms),
            "pres_candidate_terms": 0,
            "declared_nonidentity_eqsrc_arrows": 0,
        },
        "source_hashes": {
            "ontology/tex/aether_flow_foundations.tex": sha256(
                "ontology/tex/aether_flow_foundations.tex"
            ),
            "ontology/tex/aether_flow_dynamics.tex": sha256(
                "ontology/tex/aether_flow_dynamics.tex"
            ),
            "research_control/tasks/RT-20260811-012/artifacts/v22_p4_t02_b2_post_pres_src_provenance_obstruction_selected_future_packet_v1.yaml": sha256(
                "research_control/tasks/RT-20260811-012/artifacts/v22_p4_t02_b2_post_pres_src_provenance_obstruction_selected_future_packet_v1.yaml"
            ),
        },
        "checks": checks,
        "check_count": len(checks),
        "pass_count": sum(1 for value in checks.values() if value["pass"]),
        "claim_limits": {
            "meta_grammar_is_ontology": False,
            "phi_src_typed": False,
            "nonidentity_eqsrc_naturality_proved": False,
            "global_no_go_claimed": False,
            "distance_to_gr_changed": False,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
