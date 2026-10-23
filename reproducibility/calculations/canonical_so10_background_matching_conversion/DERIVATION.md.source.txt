# BMC1: additive kinetic coefficient versus nonlinear coupling ratio

Use hbar=1 in the physical coupling conversion and ell=1/(16pi²), with
formal loop bookkeeping restored by powers of ell. Let F_g(A)=dA+g[A,A].
Define renormalized hard coefficients in the ACTUAL
BFT/FCI/G2B convention by

 Gamma_F2=-(ell*g²*lambda1+ell²*g²*lambda2)*F_g(A)^2/12.

Here lambda2 carries its own actual coupling powers; do not divide out g²
twice. The effective background kinetic normalization is therefore

 K=1-ell*g²*lambda1/3-ell²*g²*lambda2/3.

For each unbroken simple ideal (and the single U1), A_i=sqrt(K_i)A and
g_i=g/sqrt(K_i) give F_gi(A_i)=sqrt(K_i)F_g(A). All quadratic/cubic/quartic
terms agree, not only the transverse propagator. Equivalently the bare
background Ward relations imply zeta_g0²*zeta_A0=1. With ZA*Zg²=1 in both
theories, the RENORMALIZED relation also is zeta_g²*K=1. This statement is
algebraic BEFORE taking epsilon to zero; pole/evanescent terms must already
be correctly handled in the renormalized coefficients. It does not license
taking a finite part of separate divergent products.

With alpha=g²/(4pi), a=alpha/pi=4ell*g², one obtains

 zeta_alpha=alpha_i/alpha=1/K
  =1+a*lambda1/12
    +a²*(lambda1²/144+lambda2/(48g²))+O(a³).

In the original reference convention zeta_alpha=1-a*C0+a²*C1 at zero
explicit reference logarithm, so

 C0=-lambda1/12,
 C1=lambda1²/144+lambda2/(48g²).

These are conversion FORMULAS, not numerical C1 values. In inverse coupling
the square cancels:

 alpha_i^-1=alpha^-1-lambda1/(12pi)-lambda2/(192pi³),
 g_i^-2=g^-2-ell*lambda1/3-ell²*lambda2/3.

Adding a one-loop square to this additive inverse-coupling formula double
counts it. Omitting the square from zeta_alpha has the opposite error.
This recovers the original direct1loop inverse-alpha threshold exactly.
No numerical partial threshold or target comparison is performed.

## The RG derivative must include running parent coordinates

Write tau=log(Q/omega_ref), with a FIXED reference unit omega_ref, not a
running VEV. Let beta_g=ell*b*g³+ell²*c*g5, and let the light two-loop gauge
row sum at tree equal couplings be r_i. Set db_i=b_i-b, dc_i=r_i-c.
Denote by D1 the one-loop RG vector on all input coordinates (including the
implicit dependence of the heavy masses/reference VEV on those inputs).
Use an admissible fixed-gap heavy/light subtraction domain. Neither a
stationary tangent nor D1 is supplied by solving the desired RG cancellation.

Differentiate the inverse-coupling relation, or independently the derived
g_i relation, and compare beta functions. This gives

 partial_tau lambda1_i=6*db_i,
 partial_tau lambda2_i=6*g²*dc_i-W_i,
 W_i=D1(lambda1_i).

For L=log(Q²/omega_ref²)=2tau, the second equation is
 2*partial_L lambda2_i=6*g²*dc_i-W_i.

With autonomous MSbar one-loop running and the constant group-theory
one-loop jump, W has no explicit tau at fixed inputs. Integration gives the
coupling-ratio quadratic coefficient db²/4 and linear coefficient

 dc/8-C0*db-W/(48g²).

The stored Martens-form dc/8-C0*db is recovered when the masses entering
lambda1 are held in its on-shell convention (W=0). In the current MSbar
parent parameter coordinates W cannot simply be declared zero. The public
source explicitly specifies on-shell masses in section2.2 and its eq44
states C0,C1 as functions of those heavy masses. This is an applicability
condition, not withdrawal of the historical fixed-mass identity.

For an actual sensitive witness, the tree vector masses are g²*lambda_r,
while potential scalar masses at fixed parent coefficients have no explicitg.
Hence the explicit gauge-coupling component is

 W_g=beta_g^(1)*partial_g lambda1=-21*b*g²*sum_r T_r.

At b_GS=-46/3 and actual vector indices sum(8,6,5), this component is
g²*(2576,1932,1610), nonzero in every gauge channel. The scalar-parameter,
VEV and any correlated reference pieces of W remain independently needed;
they may combine with this component. This witness is NOT a full nonzero-W
theorem or evidence that the existing amplitudes fail RG invariance.

## Bosonic subset and original full-matter ledger

All9 current primitive families contain gauge/scalar/ghost lines only.
G2B explicitly derives b_GS=-46/3,c_GS=4520/3 and the light gauge+Higgs+PQ
matrix. The original older Yukawa-vertex-independent ledger includes gauge
interactions of the fermions as well. Its b=-34/3 and two-loop coefficient
10405/6 are different. These are not interchangeable beta targets.
The one-loop discontinuities coincide because the same charged light fermion
content cancels between parent and EFT at that order; the two-loop jumps do
not coincide. A zero heavy one-loop fermion threshold does not prove that
two-loop mixed light-fermion/heavy-vector amplitudes vanish. No such amplitude
is calculated here and no paused matter/flavor work is activated.

The finite inventory still requires explicit applicability/normalization
and RG checks for the complete BFT coefficient: G2P common original forests,
CBR soft cancellation, HPR pole remainder/overallMS subtraction, HTB/MTA
bridge once and any genuine remaining conversion. This increment does not
assume that their numerical sum has passed those gates. It identifies the
precise independent one-loop directional RG input W as the next useful test,
without a new large diagram expansion or fitting W to an observed slope.

Primary comparator (definition only): W.Martens,
[arXiv:1011.2927v2](https://arxiv.org/pdf/1011.2927),section2.2 and eq26,44.
Retrieved2026-10-21. No finite SU5 result is imported into Spin10.
