# QIR1: the quartic class now has a complete infrared subtraction

The actual mixed and all-light contributions of the regulated VVVV graph
have been constructed and removed using independently derived kernels and
the restricted tree EFT action. Every inverse-regulator, logarithmic and
vanishing d log term cancels before the infrared limit. The remaining bare
coefficient is independent of the auxiliary infrared mass.

This closes the infrared accounting of this complete primitive class. Its
ultraviolet subdivergences and UV poles remain; this is not yet a renormalized
finite hard contribution, the full EFT construction or C1_GS.

Final validation_receipt_v2.json SHA256:
`c0f72f4fd5f17011d1fbcdb7e2c291c47189f237b45b0858b28d1ff8ce46d734`.
The completed V1 receipt is retained at
`79b822cfc2e7543743d47c662533af191383b90b6775e75f6dde8e74c6ba01f3`.
Scientific acceptance NOT_PERFORMED; state113 and authority34/39 unchanged.

## The missing quantum kernels were derived from the action

Opening the actual gauge quartic at two field slots gives, for a covariance
component M_ab L_munu with M^T=sigma M and L^T=sigma L,

    Sigma[M,L]/g10^2 = K(M) delta_munu trL
                                   +[J(M)-sigma K(M)]L_munu,
    K(M)=-sum_e F_e M F_e,
    J(M)=sum_e F_e sum_ab f_abe M_ab.

The antisymmetric curvature component uses J+K. Replacing it by J-K changes
actual non-Abelian coefficients. This sign and the vector trace orientation
were derived from all six unordered slots and their source transpose, not
chosen from the wanted IR cancellation.

All35 full45x45 mass/first-curvature/second-curvature matrices are recorded,
including their implicit zero complement. They contain1541 nonzero positions
in a70875-position operator domain; these are algebraic entries, not independent
loop measurements. Primary uses color matrices. Replay directly differentiates
the original density and performs explicit Lorentz sums at D4 and6 with the
degree bound. Every operator and the exact closed coefficient agrees.

Their light-loop closure reproduces the complete mixed class, not just its
previously qualified inverse-d projection. The first-curvature part supplies
the mixed B0*Bs logs; the second-curvature part supplies the d log terms.
Those latter terms vanish at d0 but were retained until the positive-d
identity was established. D=4-2epsilon and the dimensional finite terms remain.

## The pure-light EFT partner is an actual tree restriction

A normalized45x12 light embedding V was constructed in the physical10-plane
basis. Exact checks give V^T V=I, VV^T=P0 and O V=0. Every one of144 light
brackets has zero heavy projection. The full12^3 restricted bracket domain
contains60 nonzero entries; the zero complement is included in the comparison.
A separate fundamental10-plane reconstruction agrees with those brackets.

The parent gauge kinetic metric and quartic vertex therefore restrict
isometrically to the actual light gauge action. The heavy-light-light gauge
cubic vanishes, and O_H=0 eliminates the scalar VVH linear vertex needed
for a tree heavy exchange to alter this leading four-light-vector coupling.
The12-dimensional EFT quartic was computed from these restricted brackets,
rather than copying VQP1's all-light answer. Its Gaussian uses the same
tree coupling, source-zero xi1 gauge, auxiliary mass and dimensional measure.

This is a concrete tree/EFT construction for this class. Other tree vertices,
the other eight primitive families and beyond-tree field/coupling normalization
are not proved by this restriction.

## The resulting subtraction is exact and finite in the infrared

For G=Gh+Gs and the actual symmetric quartic tensor C4,

    Vfull -(1/2)Tr Gs Sigma_h -VEFT,quartic = C4 Gh Gh/8,
    Sigma_h=C4 Gh/2.

The two removed objects were constructed independently from the action before
comparison. Their equality follows in the actual scalar-master basis before
Laurent or IR limits. Mellin evaluations and derivatives separately test that
analytic identity. No unknown coefficient, finite condition or scaleless value
was assigned to obtain cancellation. OSF1 retains the correlated UV/EFT CT
relations; their physical finite conditions are not selected here.

In VQP1's units, Lambda2=-12 Gamma2_Fphys2/(ell^2*g10^2), the remainder is

    Lambda_hard,bare2 = g10^2 [p2/epsilon^2+p1(z)/epsilon+f0(z)],
    z=log(Q^2/60)-log(g10^2).

Logs of the actual four heavy mass ratios remain symbolic. No d or log d
appears. The complete p1 and f0 polynomials are in the new native tables.
The double-pole vector is(-1152,-648,-450) for(U1,SU2,SU3). These are
bare UV poles of one graph family, not beta coefficients or predictions.

The result is the complete regulated UV-minus-actual-partners remainder for
this factorized quartic graph. It coincides with summing its16 positive-heavy
ordered pairs only AFTER the eight mixed and one all-light assignments have
been explicitly accounted for. This earns that reduction for this class;
it is not a generic identification of mass type with momentum region.

Native tables:31109 raw/6444 gzip bytes, identical across routes. Raw SHA
`5df713fe35560d8f12830225292b59c8aad80fd79864c5c2cbf9c3287513dd34`;
gzip SHA `a79428e73a2e892735d1496303a016fb9ef05f347f30c797f2d9b9fd481d5b66`.
All open operators, tree maps, mixed/EFT/hard polynomials and zeros are retained.

## Verification and its sensitive/insensitive controls

The separate verifier rebuilds the fundamental-plane brackets and checks all
actual operators, tree identities, contractions and coefficient partitions.
Entire Mellin evaluations at two diagnostic d values and two epsilon values,
and derivatives extracting the three Laurent coefficients, agree within
maximum scaled1.80004190566e-73, versus1e-40 requirement at80digits. These
diagnostics do not select a physical g,Q or finite normalization.

The first validation passed the mathematical comparison. A post-run coverage
review added a separately frozen V2 supplement for explicit mutant receipts
of the new normalized frame, trace orientation and hard dimensional finite
term. Completed native/V1 validation work was reused. Scaling a light column
by2 gives kinetic defect3. Reversing the antisymmetric trace gives actual
nonzero weak/color residuals. Premature D4 changes the hard finite coefficients
by(755546827/37950,25998627/63250,573300877/94875); lost positive-epsilon
B terms remove nonzero zeta2 coefficients(-1152,-648,-450). Missing first/
second curvature, half mixed closure and omitted pure-light graph are also
detected where nonzero.

An important limitation is explicit: testing ONLY the final hard answer is
INSENSITIVE to prematurely deleting light assignments, because a legitimate
subtraction removes them too. The actual full-UV/partner comparisons are
sensitive and nonzero. The neutral U1 first-curvature and pure-light channels
are also insensitive. No source-normalization, arbitrary-width or global
gauge-independence control is claimed in this source-zero xi1 calculation.

No failed scientific worker/verifier in QIR1. Native times after imports
1.5915039/2.5213710s, verifier3.1395108s, V2 controls.2123472s. Sample counts
2/2/2/1, maximum51,744,768 bytes, NOTpeak; the supplement's single startup
sample does not bound its unobserved peak. Limits180s native/240s verifier/
120s supplement, sampled8GiB,350MiB launch floor and2MiB package retained.
Bindings2168/2175 plus13 V2 direct bindings and its authenticated nested
manifest. Frozen sources and complete owned captures are preserved.

Track B demonstrates removing a real matching dependency using actual lower-
order kernels and tree structure, while recognizing that a plausible final
number alone cannot test every invalid route. Shared action/projectors,
masters, software and AI analyst remain; no outside/Lean/empirical validation.

## The ultraviolet problem remains distinct

The bare finite coefficient must not be integrated into EAT1 as if its UV
forests and overall background CT were already supplied. Hard-region external
loops can receive CT insertions whose UV subgraph contains light fields.
Discarding light internal poles solely because the primitive's IR terms have
canceled is unjustified. The next task is to derive that full subgraph-pole
split and its actual heavy-loop insertions, then reconcile graph-local poles
with the complete parent CT action and the other eight primitive families.

No graph-local gauge mass is adopted as a physical mass or an independently
permitted counterterm. HTB1 finite-tadpole freedom, extra quadratic CTs, the
local2loop background CT, full field/gauge/EFT normalization and nonlinear C1
conversion remain. State113/34of39,E5/A5unqualified,HB1/C5blocked,flavorpaused,
C1_GSnull,quartetFAIL3960/648,custodyexit2/seven,scalar140%/1.94%/20.27%,
mismatch.745476 and missing Yukawas remain distinct and unchanged.

The delegated research_check.py e4 completed all six checks with their declared
exits. It authenticated historical E4 evidence and the authority/structure/
read-only contracts without a fresh scientific replay. Full output is retained
in external readiness.jsonl. Historical custody still returns exit2 with seven
unresolved references; this is not an overall PASS. Local byte sealing covers
all25393 preexisting tracked blobs and the new raw/index/HEAD bytes.
