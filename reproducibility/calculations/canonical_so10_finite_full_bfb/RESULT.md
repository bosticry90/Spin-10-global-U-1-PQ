# Strict full-field quartic positivity at the finite exploratory point

The [unchanged finite point](../canonical_so10_coherent_joint_witness/POINT.json)
admits a GLOBAL quartic lower bound in all328 canonical real scalar fields:

\[
 V_4\ge c\,[\operatorname{tr}\Phi^2+N+2\phi^\dagger\phi+2|S|^2]^2,
 \qquad
 c=\frac{824404010711173266247333949}
 {1720579893948342670590110120750}
 \simeq0.000479143115418>0.
\]

Qualification requires the completed independent receipt, full native captures
and raw Git checks. This is a sufficient global proof, not a collection of
positive sampled directions. It concerns THIS exploratory point only; no
benchmark is adopted and no protected machine authority is promoted.

## Global lower bound with every mixed interaction retained

Put x=trPhi², n=N, u=phi^dagger phi, v=|S|². Reuse the qualified GLOBAL
invariant identities Q2=Q1+Q4, R=4Q1-X131, Q4>=0 and X131>=-2Q1,
and |E.phi|²<=R*n*u. Their applicability is independent of the scalar
coefficient values, whereas the old point's positivity certificate is not.

The auxiliary proof weight tau=(s-2p8)/6=1/12000 is positive. Completing
the eta square gives

\[
 V_{\Sigma,4}+2\Re(\eta E\cdot\phi)
 \ge p_5 n^2+p_7Q_4-\frac{|\eta|^2}{\tau}nu.
\]

Indeed V_Sigma-tau*R, rewritten in Q1,Q4,X131, has discarded Q1
coefficient s-2p8-6tau=0 and positive Q4 coefficient p7=1/600.
The penalty |eta|²/tau=3/25000 is retained. A larger inadmissible proof
weight is explicitly rejected; a positive auxiliary matrix alone is not proof.

The existing correlated identity A=L+x*n/4>=0 and |Phi:T|²<=2*n*A,
with t>0 and Delta=0, gives

\[
 tA+2\Re[z_4(\Phi:T)S]\ge-\frac{2|z_4|^2}{t}nv.
\]

For ANY complex five-form, its interior-product Gram obeys 0<=K<=n I.
The exterior creation/annihilation anticommutation relation proves this
without assuming a particular Sigma shape: contraction by a unit complex
vector has norm at most one. All25200 basis/operator-index cases check the
normalization. A distinct exterior wedge Gram verifies K^T+H=nI on
complex controls; H is positive semidefinite. Hence the negative fixed
lambdaSigmaphi2 portal is bounded below by
(lambdaSigmaphi1+lambdaSigmaphi2)*n*u.

For arbitrary complex phi and real symmetric Phi,
|phi^T Phi phi|<=u*sqrt(x). The complete zK interaction consequently obeys

\[
 2\Re[z_K\phi^T\Phi\phi S^*]
 \ge-2|z_K|u\sqrt{xv}\ge-|z_K|(x+v)u.
\]

This retains the Hermitian factor and all phases. It uses a Frobenius bound,
so the separately nonnegative lambdaPhiphi2 term can be dropped without
double-counting the same positive term. Drop only that term and nonnegative
lambdaPhiVector2*|phi.phi|²; use trPhi4>=x²/10. Keep the vector/singlet
portal. All22 quartics, including three fixed zeros, are now covered.

Thus V4>=r^T M r for r=(x,n,u,v), with

\[
M=\begin{pmatrix}
3/250&0&-2/125&0\\
0&3/200&-832563/50000000&-690273291761/7360000000000\\
-2/125&-832563/50000000&1/10&-1450107/100000000\\
0&-690273291761/7360000000000&-1450107/100000000&1
\end{pmatrix}.
\]

Its leading principal minors are exactly

```text
3/250
9/50000
6770516553093/625000000000000000
824404010711173266247333949/423200000000000000000000000000000
```

All are positive. Exact Fraction LDL and a separately implemented Gaussian
solver check the SymPy minor/inverse route. With w=(1,1,2,2), Cauchy–Schwarz
in the positive M metric gives r^T M r>=(w^T r)²/(w^T M^-1 w), yielding
the stated canonical margin. All15 principal minors of M-c*w*w^T are also
nonnegative, with zero determinant, checking that residual globally.

Literal full-parent evaluations with every field species and all three
complex interactions active verify the lower inequality and phase factors.
They are implementation controls, not the source of global coverage. The
global invariant theorems and old eta/z4 inequalities are authenticated
dependencies, not newly repeated8001-pair proofs. An invalid negative pure-S
sign, ineligible tau and missing Hermitian/eta factors supply negative controls.

## What this changes

This SAME finite point now has a strict full328 quartic certificate, the
[complete scalar-contact norm bound below0.5](../canonical_so10_complete_contact_bound/RESULT.md),
the qualified listed local scalar-mass pattern and positive heavy-relaxed
Higgs quartic. This establishes a substantially stronger classical scalar
feasibility example than any earlier closed asymptotic curve. It does not
reopen or repair those failed curves or the original benchmark.

Strict quartic positivity ensures growth at large fields. It does not prove
that the chosen stationary vacuum is the deepest one, cosmologically
reachable, metastable for a required lifetime, or stable under loops. Neither
the chosen light-Higgs tuning nor technical naturalness has been explained.
Full gauge/IR scattering, quantum control, physical matching, matter/flavor,
PQ phenomenology and empirical predictions remain separate obligations.

Next prioritize a bounded perturbative-control/input assessment at this point,
using the existing12 spectral types and radial mass data before any full
quantum-matching expansion. A tree contact pass alone is not proof that
multiplicity-enhanced loop slopes or soft modes are controlled. Do not carry
over old-point loop values or promote an exploratory point through this report.

Track A gains a global scalar theorem at one fixed point. Track B records
reuse of inexpensive structural bounds after the complete contact test,
with independent rational verification. Shared action, invariant theorems,
data, Python/SymPy and analyst remain limits; this is not external endorsement.
Authority34/39, statev113, custodyexit2/seven, blocked quantum stages and
human-paused flavor stay unchanged. Education remains voluntary/nonblocking.
