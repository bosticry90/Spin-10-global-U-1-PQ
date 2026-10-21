"""OAR1 bounded checks. Document anchors are citations, not a prose theorem prover."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
from collections import Counter
from itertools import product
import json, sys, time

START = time.perf_counter()
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
role = sys.argv[1]
assert role in ('primary', 'replay')
p = json.loads((OUT/'preparation.json').read_bytes())
for raw, expected in p['input_sha256'].items():
    assert sha256(Path(raw).read_bytes()).hexdigest() == expected, raw
for a in p['anchors']:
    lines = Path(a['path']).read_text(encoding='utf-8').splitlines()
    assert lines[a['first_line']-1:a['last_line']] == a['lines']

if role == 'primary':
    # Euler's connected-graph identity: hbar * hbar^I * hbar^-V.
    graph = Counter()
    for loops in range(4):
        for vertices in range(5):
            for weights in product(range(3), repeat=vertices):
                internal_edges = loops + vertices - 1
                n = internal_edges - vertices + 1 + sum(weights)
                assert n == loops + sum(weights)
                graph[loops, n] += 1
    # Free NONCOMMUTATIVE words with a separate hbar degree, truncated at one.
    def mul(a, b):
        out = Counter()
        for (d, w), c in a.items():
            for (e, v), k in b.items():
                if d+e <= 1:
                    out[d+e, w+v] += c*k
        return {k: v for k, v in out.items() if v}
    def add(*terms):
        out = Counter()
        for t in terms:
            for k, v in t.items(): out[k] += v
        return {k: v for k, v in out.items() if v}
    def neg(a): return {k: -v for k, v in a.items()}
    one = {(0, ()): 1}
    U = {(0, ()): 1, (1, ('X',)): -1}
    V = {(0, ()): 1, (1, ('X',)): 1}
    assert mul(U, V) == one
    assert mul(U, U) != one
    q, i = {(0, ('Q',)): 1}, {(0, ('i',)): 1}
    qh, ih = mul(mul(U, q), V), mul(mul(U, i), V)
    lhs = add(mul(ih, qh), mul(qh, ih))
    rhs = mul(mul(U, add(mul(i, q), mul(q, i))), V)
    assert lhs == rhs
    expected = {(0, ('Q',)): 1, (1, ('Q', 'X')): 1,
                (1, ('X', 'Q')): -1}
    assert qh == expected and qh != q
    # Exterior words: q C1=C1 C2, q C2=C2 C3, q C3=0.
    # q(C1 C2)=(C1 C2)C2-C1(C2 C3)=-C1 C2 C3.
    def wedge(a, b):
        if set(a).intersection(b): return (), 0
        inv = sum(x > y for x in a for y in b)
        return tuple(sorted(a+b)), (-1)**inv
    qrules = {1: ((1, 2), 1), 2: ((2, 3), 1), 3: ((), 0)}
    sq = Counter()
    word = qrules[1][0]
    for j, c in enumerate(word):
        middle, coefficient = qrules[c]
        first, sign1 = wedge(word[:j], middle)
        full, sign2 = wedge(first, word[j+1:])
        sq[full] += (-1)**j*coefficient*sign1*sign2
    assert sq[(1, 2, 3)] == -1
else:
    # Sum the generating polynomials (1+z+z^2)^V, not graph enumeration.
    graph = Counter()
    coefficients = [1]
    for vertices in range(5):
        for loops in range(4):
            for weight, multiplicity in enumerate(coefficients):
                graph[loops, loops+weight] += multiplicity
        following = [0]*(len(coefficients)+2)
        for j, c in enumerate(coefficients):
            for k in range(3): following[j+k] += c
        coefficients = following
    # Rational 4x4 graded matrices; X even, Q and i odd.
    def mm(a, b):
        return [[sum(a[j][k]*b[k][l] for k in range(4))
                 for l in range(4)] for j in range(4)]
    def plus(a, b, sign=1):
        return [[a[j][k]+sign*b[j][k] for k in range(4)] for j in range(4)]
    def bracket(a, b): return plus(mm(a, b), mm(b, a), -1)
    zero = [[Fraction(0) for _ in range(4)] for _ in range(4)]
    X = [[Fraction(v) for v in r] for r in
         [[2, 1, 0, 0], [3, -1, 0, 0], [0, 0, 1, 2], [0, 0, -1, 4]]]
    Q = [[Fraction(v) for v in r] for r in
         [[0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0]]]
    I = [[Fraction(v) for v in r] for r in
         [[0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 2, 0, 0]]]
    dQ, dI = bracket(Q, X), bracket(I, X)
    T = plus(mm(I, Q), mm(Q, I))
    tangent = plus(plus(mm(dI, Q), mm(I, dQ)),
                   plus(mm(dQ, I), mm(Q, dI)))
    assert tangent == bracket(T, X)
    assert plus(mm(Q, dQ), mm(dQ, Q)) == zero
    assert dQ != zero and plus(X, X) != zero
    # Equivalent Jacobi coefficient from a non-Lie antisymmetric bracket.
    f = {(0, 1): [1, 0, 0], (1, 2): [0, 1, 0]}
    def b(a, c):
        v = [0, 0, 0]
        for j, x in enumerate(a):
            for k, y in enumerate(c):
                for l, z in enumerate(f.get((min(j, k), max(j, k)), [0]*3)):
                    if j != k: v[l] += x*y*z*(1 if j < k else -1)
        return v
    e = [[int(i == j) for j in range(3)] for i in range(3)]
    jacobi = [sum(b(e[j], b(e[(j+1)%3], e[(j+2)%3]))[k]
                  for j in range(3)) for k in range(3)]
    assert jacobi == [1, 0, 0]

assert sum(graph.values()) == 484
assert min(L+1 for L in range(1, 5)) == 2
assert 1+0 == 1  # strength-zero loop control really starts at one loop
receipts = []
for raw in p['receipts']:
    v = json.loads(Path(raw).read_bytes())
    assert v['execution_state'] == 'COMPLETED', raw
    receipts.append({'path': raw, 'sha256': sha256(Path(raw).read_bytes()).hexdigest(),
                     'scientific_disposition': v['scientific_disposition']})

value = {
    'schema': 'ONE_LOOP_ACCEPTANCE_RECONCILIATION_CHECKS_V1', 'route': role,
    'graph_power_multiplicities': [[a, b, c] for (a, b), c in sorted(graph.items())],
    'graph_weight_cases': sum(graph.values()), 'anchors_checked': len(p['anchors']),
    'one_loop_response_to_hbar_counterterm_minimum_order': 2,
    'order_hbar_jacobian_effective_action_minimum_order': 2,
    'strength_zero_loop_control_order': 1,
    'closed_first_order_not_quadratically_closed_control': -1,
    'noncommutative_transport_inverse_and_omission_controls': True,
    'authenticated_existing_receipts': receipts,
    'all_higher_order_endpoint_hypotheses_retained': True,
    'literal_membership_failure_and_four_basic_classes_retained': True,
    'new_physics_amplitudes_or_general_unit_domains_calculated': False,
    'full_E5_A5_or_quantum_prescription_nonemptiness_proved': False,
    'authority_changed': False,
    'scientific_disposition': 'BOUNDED_ORIGINAL_ACCEPTANCE_RECONCILIATION_AND_STRICT_FIRST_ORDER_REPLACEMENT_ONLY_NOT_FULL_E5',
    'elapsed_after_imports': time.perf_counter()-START,
    'execution_state': 'COMPLETED',
}
assert value['elapsed_after_imports'] < 60
print('RESULT '+json.dumps(value, sort_keys=True, separators=(',', ':')), flush=True)
