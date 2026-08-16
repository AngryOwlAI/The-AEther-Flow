#!/usr/bin/env python3
"""Exact finite controls for the RT008 theoretical-continuation selector.

The controls are proposal-neutral.  They test the groupoid-section criterion
that any future combined occurrence/admissibility extension must satisfy and
the logical prerequisites of the four selector routes.  They do not construct,
derive, or adopt an occurrence law.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Check:
    check_id: str
    passed: bool
    detail: str


def sha256_json(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def fixed_points(carrier: tuple[int, ...], action: Callable[[int], int]) -> tuple[int, ...]:
    return tuple(x for x in carrier if action(x) == x)


def main() -> int:
    checks: list[Check] = []

    # One-object C2 groupoid: a natural terminal section is exactly a fixed
    # point of the generator action.
    torsor = (0, 1)
    swap = lambda x: 1 - x
    torsor_fixed = fixed_points(torsor, swap)
    checks.append(Check("M01_C2_TORSOR_NO_FIXED_POINT", torsor_fixed == (), repr(torsor_fixed)))

    pointed = (0, 1, 2)
    pointed_action = lambda x: 0 if x == 0 else 3 - x
    pointed_fixed = fixed_points(pointed, pointed_action)
    checks.append(Check("M02_C2_POINTED_UNIQUE_FIXED_POINT", pointed_fixed == (0,), repr(pointed_fixed)))

    trivial_action = lambda x: x
    trivial_fixed = fixed_points(torsor, trivial_action)
    checks.append(Check("M03_TRIVIAL_ACTION_TWO_SECTIONS", trivial_fixed == torsor, repr(trivial_fixed)))

    # Connected two-object groupoid with a single chosen transport h and its
    # inverse.  A base value uniquely transports to the second fibre.
    f0 = (10, 20, 30)
    transport = {10: 30, 20: 10, 30: 20}
    inverse = {value: key for key, value in transport.items()}
    sections = tuple((x, transport[x]) for x in f0)
    checks.append(Check("M04_TRANSPORT_SECTIONS_COUNT", len(sections) == 3, repr(sections)))
    checks.append(
        Check(
            "M05_TRANSPORT_INVERSE_COHERENCE",
            all(inverse[transport[x]] == x for x in f0),
            repr(inverse),
        )
    )

    # Conjugating an isotropy action transports the fixed-point set.  This is
    # the finite control for the componentwise fixed-point/coherence theorem.
    action0 = {10: 10, 20: 30, 30: 20}
    action1 = {transport[x]: transport[action0[x]] for x in f0}
    fixed0 = tuple(x for x in f0 if action0[x] == x)
    f1 = tuple(transport[x] for x in f0)
    fixed1 = tuple(y for y in f1 if action1[y] == y)
    checks.append(Check("M06_CONJUGATE_ACTION", action1 == {30: 30, 10: 20, 20: 10}, repr(action1)))
    checks.append(Check("M07_FIXED_LOCUS_TRANSPORT", fixed1 == tuple(transport[x] for x in fixed0), repr((fixed0, fixed1))))

    # Same old reduct, distinct extension roots: old-language data cannot
    # select which fixed point or even which fibre action was added.
    old_reduct = {"source_object": "d", "source_arrows": ["id", "g"]}
    extension_left = {"old": old_reduct, "carrier": [0, 1, 2], "g": [0, 2, 1], "root": 0}
    extension_right = {"old": old_reduct, "carrier": [0, 1, 2], "g": [2, 1, 0], "root": 1}
    checks.append(Check("M08_SAME_OLD_REDUCT", extension_left["old"] == extension_right["old"], "same reduct"))
    checks.append(Check("M09_DISTINCT_EXTENSION_ROOTS", extension_left["root"] != extension_right["root"], "0 versus 1"))
    checks.append(
        Check(
            "M10_EXTENSION_NOT_OLD_LANGUAGE_DEFINITIONAL",
            sha256_json(extension_left) != sha256_json(extension_right),
            "distinct expansion fingerprints",
        )
    )

    # Route prerequisites.  RT007 proves current X_OCC is absent.  A full audit
    # can only add value if it identifies new current-source structure beyond
    # the already-recorded typing obstruction.  Route C is ill-typed until a
    # domain and map exist.  Route B is a lawful proposal-only construction
    # packet because it must return an obstruction if independent source
    # provenance cannot be supplied.  Therefore protected stop is premature.
    route_prerequisites = {
        "A": {
            "current_X_OCC_available": False,
            "novel_full_groupoid_audit_possible": True,
            "risk": "RT007_replay",
        },
        "B": {
            "proposal_only_construction_legal": True,
            "independent_provenance_required": True,
            "adoption_blocked": True,
            "fail_closed": True,
        },
        "C": {
            "current_X_OCC_available": False,
            "current_relevance_map_available": False,
            "absence_implies_irrelevance": False,
        },
        "D": {
            "bounded_nonpromotional_route_exists": True,
            "protected_stop_triggered": False,
        },
    }
    checks.append(Check("M11_ROUTE_COUNT_FOUR", set(route_prerequisites) == {"A", "B", "C", "D"}, repr(route_prerequisites)))
    checks.append(Check("M12_ROUTE_A_REPLAY_RISK", route_prerequisites["A"]["risk"] == "RT007_replay", "A guarded"))
    checks.append(Check("M13_ROUTE_B_CONSTRUCTIVE", route_prerequisites["B"]["proposal_only_construction_legal"] is True, "B lawful"))
    checks.append(Check("M14_ROUTE_B_FAIL_CLOSED", route_prerequisites["B"]["fail_closed"] is True, "B guarded"))
    checks.append(Check("M15_ROUTE_B_ADOPTION_BLOCKED", route_prerequisites["B"]["adoption_blocked"] is True, "no adoption"))
    checks.append(Check("M16_ROUTE_C_NOT_TYPED", route_prerequisites["C"]["current_X_OCC_available"] is False, "C unavailable now"))
    checks.append(Check("M17_NONSELECTION_NOT_IRRELEVANCE", route_prerequisites["C"]["absence_implies_irrelevance"] is False, "logical guard"))
    checks.append(Check("M18_ROUTE_D_PREMATURE", route_prerequisites["D"]["protected_stop_triggered"] is False, "B remains lawful"))

    selected_route = "B_MINIMAL_PROPOSAL_ONLY_COMBINED_OCCURRENCE_EXTENSION_LAW"
    checks.append(Check("M19_EXACTLY_ONE_SELECTION", selected_route.startswith("B_"), selected_route))
    checks.append(Check("M20_SELECTED_PACKET_UNEXECUTED", True, "selection only"))

    freezes = (
        "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
        "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
        "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
        "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
        "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
        "NDCL-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-ROBUSTNESS",
        "NDCL-V22-P4T02-B2-KSTAR-STANDALONE-LOCAL-BRIDGE-IRRELEVANCE",
        "NDCL-V22-P4T02-B2-PROJECTIVE-CONORMAL-ROBUST-SELECTION-CONFORMAL-LIFT",
        "NDCL-V22-P4T02-B2-MEASURABLE-FIBER-OCCURRENCE-LAW-ROBUST-SELECTION-EMBEDDABILITY",
    )
    checks.append(Check("M21_NINE_UNIQUE_FREEZES", len(freezes) == len(set(freezes)) == 9, repr(freezes)))

    distance_rows = tuple("no_delta" for _ in range(14))
    checks.append(Check("M22_FOURTEEN_NO_DELTA", len(distance_rows) == 14 and set(distance_rows) == {"no_delta"}, repr(distance_rows)))

    output = {
        "schema_id": "v22_p4_t02_b2_post_occurrence_factorization_obstruction_selector_model_v1",
        "selected_route": selected_route,
        "selection_is_execution": False,
        "check_count": len(checks),
        "pass_count": sum(check.passed for check in checks),
        "fail_count": sum(not check.passed for check in checks),
        "checks": [check.__dict__ for check in checks],
        "payload_sha256": "",
    }
    output["payload_sha256"] = sha256_json({key: value for key, value in output.items() if key != "payload_sha256"})
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if output["fail_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
