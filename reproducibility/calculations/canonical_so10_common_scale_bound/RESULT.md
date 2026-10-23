# CSB1: an explicit common logarithm cannot cure the frozen bosonic hierarchy

At each of the three retained diagnostic couplings, even the best common
explicit L leaves at least one two-loop kinetic correction larger than
tree. This rules out that limited adjustment of the frozen coefficient
tables. It is not a physical RG trajectory calculation, a selected scale,
a new prescription or an exclusion of the full Spin10 theory.

Evidence validation receipt `validation_receipt.json`, SHA256
`6d023c609cd577486d510fdf8b61d95cc39fa3c76b37bdacbcd852528758380c`,
QUALIFIED_FROZEN_BOSONIC_COMMON_SCALE_MINIMAX_BOUND. Exact algebra and
numerical route checks qualify; the common-log tree-control feasibility
test is negative in3/3 cases. Scientific/director acceptance NOT_PERFORMED;
state113 and scientific authority34/39 are unchanged.

For BIA1's actual complete bosonic lambda2_i=F0_i+F1_i*L, define
A_i=-x*F0_i,B_i=-x*F1_i. The two-loop kinetic correction is
k2_i=(A_i+B_i*L)/(768*pi^4). All three slopes B_i are positive in these
data. The calculated simultaneous minima are:

| x=g10^2 | Mathematical witness L | min_L max_i abs(k2_i) | Coarse lower certificate |
| --- | ---: | ---: | ---: |
| 1/2 | -1.19736170317 | 3.20228889603 | >3.19713840186 |
| 3/4 | -1.19295995891 | 4.83314882865 | >4.82537529364 |
| 1 | -1.13944593250 | 6.93237256967 | >6.92122268731 |

The witness is part of a mathematical certificate; no Q value is adopted.
The necessary simultaneous condition abs(k2_i)<=1 cannot hold for any
common L with these fixed coefficients. This is stronger than checking
only L=0, while remaining much narrower than a physical scale-independent
conclusion. Proper RG evolution moves the original parameters and cannot
be replaced by this explicit-log operation.

## Exact certificate and distinct replay

The primary uses the L-independent pairwise lower bound

 max_i abs(A_i+B_i*L) >= abs(B_j*A_i-B_i*A_j)/(B_i+B_j).

It finds the strongest pair and a saturating witness, then checks the third
component as well. The replay instead builds each allowed L interval at
trial norm t and finds the first nonnegative crossing for which all three
intervals intersect. Their optimum and witness agree within1e-28.
Identities within each route are exact Fraction arithmetic on the frozen
decimal input strings. The algebra does not convert approximate loop data
into exact physical coefficients or establish their rigorous uncertainty.

Using the elementary pi<22/7, the replay also tests the looser rational
tree threshold768*(22/7)^4. Its three L intervals already have no common
point. The displayed coarse normalized lower certificates follow without
depending on the high-precision pi evaluation. The last column certifies
the conclusion for the frozen rational tables, with inherited upstream
precision and shared-assumption limitations retained.

All57 route/L=0 comparisons and3 permutation checks pass; maximum scaled
discrepancy1.17396916907075e-49. L=0 reproduces BIA1. Allowing a different
L_i for each gauge factor would trivially give three zeros; the positive
common-scale bound exposes why that relaxation answers a different problem.
U1 and SU2 are active at each optimum. Omitting SU3 leaves the optimum
unchanged in all3 cases, so that omission control is explicitly insensitive;
the complete third component was nevertheless checked in both routes.

All three workers completed on their first executions, with no failed or
unfinished CSB run. After-import times1.8554520/1.9026608/1.8791596s.
Primary has one launch-time private sample430080bytes; replay/gate have
two samples each with maxima16,621,568/15,224,832bytes. These are not peak
measurements. Launch commit exceeded6.57GB;600s/8GiB sampled-private/
350MiB-floor/24MiB-package bounds were not exhausted. Preparations bind
6524/6531 inputs; package about2.51MB. External full captures are under
common-scale-bound-v1-2026-10-22. Source copies and frozen inputs remain.

The result does not justify changing scalar parameters, finite normalization,
gauge widths or missing fermion amplitudes to force a favorable threshold.
It does not prohibit a properly justified study of another action-permitted
region. Such a region cannot inherit these numerical loops. The original
matter/flavor pause, HB1/C5 block, physical C1/refit/E5/A5 obligations,
scalar/tree/gauge/quartet failures and custodyexit2/sevenNOTPASS remain.
Shared action, spectrum, loop assumptions, software and AI author limit
corroboration; no external physical validation or foundational change.
