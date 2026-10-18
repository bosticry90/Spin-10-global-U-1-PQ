# Local perturbative fermion gauge-anomaly screen

The declared three left-handed16s have vanishing four-dimensional local
Spin10 cubic gauge-anomaly coefficients and mixed gauge-gravity linear
coefficients. The explicit representation calculation reproduces an
established result; it is not a new anomaly-cancellation mechanism.
No numerical Yukawa input or scalar benchmark change is needed for this test.

Read the [prospective contract](RECORD.md), [native output](original_result.json),
fresh pair, [independent receipt](validation_receipt.json), preparations and
complete captures. Final qualification requires the actual receipt and raw
Git custody, not this report alone.

## Scientific question and answer

A chiral gauge anomaly would obstruct the gauge symmetry needed to define a
consistent quantum theory. Its standard four-dimensional local representation
test uses symmetric cubic generator traces; the mixed gauge-gravity test uses
linear traces. Bilal's [Lectures on Anomalies](https://arxiv.org/pdf/0802.0634),
sections7.2,7.3,11.3.2, derives these criteria and explicitly includes
SO(4n+2) among the groups with zero cubic coefficients even for complex
representations. This is inherited scientific knowledge, not AI discovery.

The primary route calculates the complete cubic Cartan polynomial for the
16 even-minus weights(+-1/2)^5. All35 degree-three coefficient slots and
the linear polynomial vanish exactly. Real skew-matrix normal form conjugates
any compact so10 element into the Cartan; the SO10 conjugation lifts to
Spin10. Trace invariance and polarization then imply the full symmetric
cubic tensor vanishes. A Cartan check without that argument would be weaker.

The independent route constructs10 Euclidean Clifford matrices, restricts the
spin generators to the16-dimensional chiral subspace and verifies their Lie
brackets against the45 real vector-plane generators. It explicitly evaluates
every symmetric triple, including predicted zeros:

| Exact check | Coverage | Result |
| --- | ---: | --- |
| Symmetric cubic gauge tensor | 16,215 slots | Every slot zero |
| Linear gauge traces | 45 generators | Every trace zero |
| Independent quadratic trace entries | 1,035 | Tr16(H_A H_B)=4delta_AB |
| Lie brackets | 990 distinct generator pairs | Exact vector/spin relation |

The slot count is the number of entries in one symmetric tensor, not16,215
physical loop amplitudes. No triangle integral or matter determinant was
computed. With H_ab=gamma_a gamma_b/(2i), the vector trace is2delta_AB;
the relative conventional Dynkin indices are1 for10 and2 for16.
The nonzero fifth moment Tr16(C^5)=60, C=sum of five Cartan generators,
checks that the chiral16 was not silently doubled into16+bar16.

Independent Clifford branching reproduces the actual left SM fields
Q,uc,dc,L,ec,nc, including conjugate color characters and hypercharges.
The SU3^3,SU3^2Y,SU2^2Y,Y^3 and mixed Y-gravity coefficients vanish per
generation. The full Spin10 tensor result also restricts to every embedded
subalgebra; this is not a proof of global anomalies or all low-energy matching.

## Global PQ is a different question

The same declared matter has nonzero global-current coefficients:

| Global PQ trace convention | Three-family value |
| --- | ---: |
| Mixed Spin10 plane trace, sum_f q Tr16(H_A H_B) | 12delta_AB |
| N_color=2sum(q T_color) | 12 |
| N_weak=2sum(q T_weak) | 12 |
| Hypercharge2sum(q Y^2) | 20 |
| GUT-normalized hypercharge coefficient | 12 |
| Electromagnetic E | 32 |
| Linear and cubic PQ charge traces | 48 each |

The color and electromagnetic values agree with the qualified
[PQ screen](../canonical_so10_pq_anomaly_screen/RESULT.md). A nonzero anomalous
global PQ current is not a nonzero Spin10 cubic gauge anomaly. This does not
authorize gauging PQ, adding a new vector field or claiming all source/measure
conditions have been constructed. No axion mass or cosmology is predicted.

## Controls, authority and next action

A single SU3 fundamental comparator has nonzero symmetric cubic trace-12
along diag(1,1,-2). Omitting uc from the SM inventory leaves Y^3=8/9 per
generation. Removing one spinor weight leaves a nonzero Cartan cubic moment
and an invalid Spin10 inventory. A vectorlike16+bar16 has vanishing fifth
moment, unlike the declared chiral16. These controls distinguish a real test
from an implementation that merely returns zero.

Original/fresh native SHA256
`d77a2bfe28d547afac754a5f04c544e7ebd4e30d29cda9a0e6705b16d5bdae48`
agrees. The full-matrix verifier, actual standard preflight and exact raw Git
checks are required. No new failed runs. Immediate350MiB available-commit
observations, sampled8GiB private limits and900seconds after imports apply;
sampling is not proof of an instantaneous memory peak.

This removes one representation-level local anomaly obstruction for the
declared field content and is reusable if scalar parameters change. It does
not settle global anomalies, non-spin backgrounds/bundle completion, the
regulated continuum measure, nonlinear Ward/Slavnov restoration, insertion
and contact normalization, or quantum canonical equivalence. The earlier
quartet-normalization failure and every E5 obligation retain their scopes.
An E1 'gauge-fixing fermion' is an odd gauge-fixing functional, distinct from
the physical16 matter; its qualification is not a computed matter determinant.

No viability verdict, new parameter domain, flavor fit or gauge input was
selected. The [scalar feasibility proposal](../../docs/RESEARCH_DIRECTION_PROPOSAL_V1.md)
remains pending. Full physical matching at the frozen failed point remains
deferred; do not interpret this expected consistency check as repairing it.

AI capability demonstrated: recover a standard necessary criterion, calculate
the actual declared representation through different methods and distinguish
anomalous global symmetry from gauge inconsistency. Shared field assumptions,
Python/SymPy and analyst limit corroboration; this is not external endorsement
or general AI reliability. Physics/AI objectives equal; education voluntary
and nonblocking. Preserve34/39,quartetFAIL3960/648,E5/A5unqualified,HB1/C5blocked,
C1_GSuncalculated,full328BFB/naturalness,matter/flavorpause,custodyexit2/seven.
No blocked activation, branch/worktree/reset, remote action/publication/outreach.
The overall investigation remains incomplete.
