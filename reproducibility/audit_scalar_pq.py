"""Focused exact check of the published scalar action's PQ notation.

Run from the public checkout with Python 3.11+ and SymPy installed:
    python -B reproducibility/audit_scalar_pq.py

The frozen certificate and four of its fixtures are reused. The regrouped
contraction below is a separate implementation, not a new spectrum or
stability replay. Do not infer scientific acceptance from this audit.
"""
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
FROZEN = HERE / "calculations" / "canonical_so10_scalar_reconstruction"
sys.path.insert(0, str(FROZEN))
from certify_sigma_quartics import (  # noqa: E402
    add_forms, doublet_form, quartics, selfdual_form, vacuum_form,
)
from count_d5_singlets import multiset_character, singlet_multiplicity  # noqa: E402
from sympy import Matrix  # noqa: E402
from verify_action_inventory import SLOTS  # noqa: E402


def mul(a, b):
    return a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0]


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def sign(indices):
    return (-1)**sum(x > y for i, x in enumerate(indices) for y in indices[i+1:])


def conj(a):
    return a[0], -a[1]


def pairs_by_contracted_tuple(form, k):
    """Group component slices by K first, then take their outer products."""
    groups = defaultdict(list)
    for indices, value in form.items():
        for contracted in combinations(indices, k):
            rem = tuple(i for i in indices if i not in contracted)
            s = sign(contracted + rem)
            groups[contracted].append((rem, (s*value[0], s*value[1])))
    pairs = defaultdict(lambda: (0, 0))
    for rows in groups.values():
        for i, a in rows:
            for j, b in rows:
                pairs[i, j] = add(pairs[i, j], mul(a, b))
    return {ij: a for ij, a in pairs.items() if a != (0, 0)}


def printed_cross(p, conjugate_second=True):
    total = (0, 0)
    for (i, j), a in p.items():
        for excluded in i:
            left = tuple(x for x in i if x != excluded)
            for included in j:
                right = tuple(x for x in j if x != included)
                c = left + (included,)
                d = (excluded,) + right
                if len(set(c)) != 4 or len(set(d)) != 4:
                    continue
                b = p.get((tuple(sorted(c)), tuple(sorted(d))), (0, 0))
                s = sign(left + (excluded,))*sign((included,) + right)*sign(c)*sign(d)
                real, imag = mul(a, conj(b) if conjugate_second else b)
                total = add(total, (s*real, s*imag))
    return total


def printed_row(form):
    p = [pairs_by_contracted_tuple(form, k) for k in range(3)]
    q = [sum(x*x+y*y for x, y in m.values()) for m in p]
    x = printed_cross(p[1])
    assert x[1] == 0
    return (*q, x[0])


def main():
    # Charges read from the published field table, including conjugate fields.
    charge = {"Phi": 0, "Sigma": 2, "Sigma*": -2, "phi": -2,
              "phi*": 2, "S": -4, "S*": 4}
    degree_counts = {k: sum(len(v) for fields, v in SLOTS.items()
                            if len(fields) == k) for k in (2, 3, 4)}
    assert degree_counts == {2: 4, 3: 4, 4: 26}
    assert len(SLOTS) == 26
    assert all(sum(charge[f] for f in fields) == 0 for fields in SLOTS)
    # The five complex directions each contribute a conjugate pair.
    assert sum(degree_counts.values()) - 5 == 29
    assert 2*charge["Sigma"] == 4
    assert 4 - 4 == 0 and 4 + 4 == 8
    multiset = ("Sigma", "Sigma", "Sigma*", "Sigma*")
    upper = singlet_multiplicity(multiset_character(multiset))
    assert upper == 4
    v, h = vacuum_form(), doublet_form(6)
    fixtures = (v, h, add_forms(v, h), selfdual_form())
    rows = []
    for f in fixtures:
        row = printed_row(f)
        ref = quartics(f)
        assert row == (ref[0], ref[1], ref[2], ref[5])
        # Apply (3+4i)/5 exactly by clearing the common denominator 5.
        phase_numerator = {idx: mul((3, 4), z) for idx, z in f.items()}
        assert printed_row(phase_numerator) == tuple(5**4*x for x in row)
        rows.append(row)
    determinant = int(Matrix(rows).det())
    assert determinant == -1680479354880
    # Arithmetic negative control outside the self-dual fixture domain.
    # Removing conjugation changes a nonzero unconstrained contraction.
    probe = {(0, 1, 2, 3, 4): (1, 0)}
    p0 = pairs_by_contracted_tuple(probe, 1)
    p1 = pairs_by_contracted_tuple({k: mul((3, 4), z) for k, z in probe.items()}, 1)
    base = printed_cross(p0, False)
    assert base == (20, 0)
    assert printed_cross(p1) == (5**4*20, 0)
    assert printed_cross(p1, False) != (5**4*20, 0)
    print(json.dumps({
        "execution_state": "COMPLETED",
        "scope": "Published scalar charge inventory and Sigma quartic notation",
        "source_commit": "9a0cd951c49f0ca497a0c864b71af99631e5599b",
        "neutral_inventory_slots": 34, "hermitian_coefficient_groups": 29,
        "sigma_quartic_character_multiplicity": upper,
        "sigma_quartic_rank_witness_determinant": determinant,
        "sigma_quartic_fixture_rows": rows,
        "rational_phase_controls": len(rows),
        "unconstrained_missing_conjugation_control": list(printed_cross(p1, False)),
        "shared_inputs": "Frozen fixture forms, field conventions and SymPy; regrouped contraction",
        "frozen_inputs_sha256": {
            name: sha256((FROZEN/name).read_bytes()).hexdigest()
            for name in ("PARENT_ACTION_V1.md", "certify_sigma_quartics.py",
                         "count_d5_singlets.py", "test_eta1_invariant.py",
                         "verify_eta1_doublet_mixing.py", "verify_action_inventory.py")
        },
        "scientific_acceptance": "NOT_PERFORMED",
    }, indent=2))


if __name__ == "__main__":
    main()
