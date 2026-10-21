# LAC1 â€” local relative products do not determine the complete Gamma

Prospective pending complete independent evidence. This applies an established
local construction to the actual graded one-loop family. It is not a new
fundamental theory, an E5 acceptance revision or a global vacuum construction.

## 1. Local cutoff construction on the qualified family

Let S(V)=T exp(i V/hbar) with the COS1 Wick/loop conventions. All statements
mean equality at every fixed finite vertex order, retaining total loop number
L<=1. Sources, test probes and backgrounds are external coefficients. Use the
formal star inverse of S(V), which exists because its zeroth interaction term
is1. No physical adjoint or unitary operator is assumed. The graded Wick
algebra is associative; omitted higher-loop graphs cannot return to L<=1
under multiplication since adding edges cannot lower the first Betti number.

For an even compact action V define S_V(F)=S(V)^(-1) star S(V+F). If two
cutoffs agree near a causally closed compact O, split their difference into
a future part A, disjoint from J^-(O), and a past part B, disjoint from
J^+(O), with a smooth compact partition. Here V'=V+A+B. Causal factorization
gives S_V'(F)=S_(V+B)(F) for supp F in O and

    S_(V+B)(F)=U star S_V(F) star U^(-1),
    U=S(V+B)^(-1) star S(V).

These are the standard relative-S cutoff identities. The comparison is
Brunetti-Fredenhagen, section8/Proposition8.1,
https://arxiv.org/abs/math-ph/9903028v1 . Their Hilbert-space unitarity claim is
not imported; only the displayed algebraic identities and causal support
argument are used with the qualified mixed graded products. Compact cutoff
independence up to these isomorphisms defines local interacting field algebras.

For a coherent chain of past changes, U32 U21=U31 by cancellation of the
intermediate S. Different allowed splittings need not give a canonical U;
their quotient centralizes the local generators when they implement the same
map. Nested regions restrict the same generators and comparisons. For
spacelike-separated supports, the relative products graded commute by causal
factorization. This is an algebra of all retained fields, not a constructed
physical BRST cohomology or a positive observable Hilbert space.

The proof is independent of the number and degrees of local vertices. Finite
word/matrix tests diagnose inverse/order errors; they do not prove all-orders
distribution extension. The latter is the qualified COS1 tensor/core proof,
with CSP1/HMM1/MLB1 inputs, reused here. No new loop integral or overlapping
multi-loop extension is assumed. Causal composition retains the same complete
forest counterterms, not a bare whole-graph finite part.

## 2. Derivative transport includes a connection term

Give the interaction family an external probe theta of parity r and
differentiate its SAME U(theta). For homogeneous X of parity p and X'=U X U^-1,
left differentiation at theta=0 gives

    d_theta X'=Ad_U(d_theta X)+[A_theta,X']_graded,
    A_theta=(d_theta U) U^-1,
    [A_theta,X']_graded=A_theta X'-(-1)^(r*p)X' A_theta.

U is even, so its inverse differentiates as -U^-1(d_theta U)U^-1. This proves
the formula including odd source probes. It also follows by the coefficient
of theta in products with theta placed on the left. The correction is not
optional even if a selected projection happens to vanish. This is a derivative
of one generating functional, not an assumption that nonlinear Q is a
derivation of the fixed free star product or of Tn.

The actual source density includes JB14_0 partial0 C14 with coefficient1.
At lowest interaction order, a past action difference therefore makes the
JB14_0 derivative of U proportional to partial0 C14. The actual massless
reference G_C14,ub14=1/P is nonzero. Its ordered positive-frequency pair has
W_C14,ub14=+2pi theta(p0)delta(P) and the reverse odd entry has the opposite
sign. Consequently the graded anticommutator spectral kernel of
partial0 C14 with ub14 contains 2pi*i*p0*sgn(p0)*delta(P), nonzero. This is
a reference/source control, not a calculated full interacting amplitude.
No source is propagated. Source omission is thus detectable with an actual
field pair; it is not a generic Gaussian example labelled as model evidence.

Ordinary source, BV source and background derivatives obey their respective
parities and the same product rule. Parameters and insertions must be
transported together. For a derivative acting on local jets, keep its full
Frechet action and currents. A local Ward equation, when derived from the
same completed products, transports as an equation with these terms. It is
not justified by differentiating U as a fixed numerical matrix.

## 3. Classical switching breaking remains an insertion

For S_u=S0+V(u), the master functional need not vanish. Even if u=1 near O,
the connected insertion [S(S_u)]_Gamma can communicate from its transition
region. One cannot erase it by arguing that derivatives of u have support
outside O. The GQAP1 identity keeps this insertion and its currents. The
cutoff comparison transports that identity and its first probe products by
section2; it does not replace it by a homogeneous global Slavnov equation.

For example a term u B partial omega integrates by parts into the full
current and -omega[u partial B+(partial u)B]. Omitting the second term changes
the functional. More generally, a local identity modulo divergences can be
localized only with its corresponding current/probe terms. Algebraic cutoff
independence is a comparison of local algebras, not a pointwise assertion
that the cutoff action is the uncut classical master solution everywhere.

## 4. Actual source-only counterexample to a stronger implication

Write the45 antighost fields as a, with real physical coordinates
a_phys=T_a a_raw. Their evaluation-dual sources are
J_a,phys=T_a^(-t) J_a,raw. All these sources have standard/project dimension2,
ghost number0 and even parity. Define the typed local candidate

    N_J=(g10^2/2) integral J_a,raw^t G_Ja J_a,raw,
    G_Ja=T_a^(-1) T_a^(-t).

It is a real dimension-four, ghost-zero, even polynomial in the permitted
variables, with no inverse physical coupling/mass/width. g10^2 makes it vanish
at zero gauge coupling. It is a candidate NEGATIVE CONTROL, not an adopted
finite normalization or a claimed Ward-restored prescription.

The actual twelve E3 source carrier matrices obey
sigma_Ja,h^t G_Ja+G_Ja sigma_Ja,h=0. Thus this example even satisfies local
background covariance; no sources or parameter derivatives are suppressed.
It nevertheless has a nonzero Slavnov image. Since QJ_a=EL_a^L S,

    QN_J=g10^2 integral J_a^t G_Ja EL_a^L S.

Recover the COMPLETE two-derivative ghost bilinear from the actual GF density
by graded Euler/IBP and independently from the frozen raw Hessian. At field
degree1/source degree1, its Fourier coefficient is

    g10^2 J_a^t G_Ja K_aC C.

The matrix and zero complement are computed. In particular the actual
Jbar0--C0 two-jet entry is nonzero, while Jub14--C14 is zero. The complete
source image has rank45; see FRAME_CORRECTION_V2.md. Its field/source degree and derivative
order exclude cancellation by nonlinear fields or terms quadratic in sources.
This suffices to prove QN_J!=0; no claim about every nonlinear coefficient
of QN_J is made. Source restriction J=0 would hide precisely this control.
The38-class theorem concerns measured logarithmic poles and is unaffected
by this hypothetical finite normalization.

In the fixed free star product, every field-independent N[J,A] is central.
Adding it to the action multiplies BOTH S(V) and S(V+F) by exp(i N/hbar)
for field-local F, so their relative S cancels this factor identically. The
same local field algebra therefore cannot distinguish Gamma from Gamma+N.
But the order-hbar Slavnov difference is QN. The constructed N_J shows the
distinction on the actual source alphabet, not merely in abstract notation.

Likewise a background-only N is invisible to these relative field products.
N proportional to the known L_div has zero Slavnov variation because QA=0,
but a nonzero background Ward variation. In the actual A0_0/omega0 affine
slice, the divergence-square variation contains partial0 A0_0*partial0^2 omega0;
its Euler_omega has the nonzero third derivative of A. L_bg, in contrast,
is an allowed invariant direction but changes pure-background responses.
W4 explicitly retains that distinction. BCR1's reference functional must
remain alongside the local field comparison; it cannot be reconstructed
from a relative S-matrix that has divided out its central factor.

Thus local cutoff independence proves neither strict global 1PI restoration
nor source/background normalization equivalence. The missing implication is
false, rather than a slow calculation that needs more coefficient tables.

## 5. What the original requirements actually demand

W1 specifies the formal Minkowski functional and graded Legendre identities,
including external sources before restriction. W2/A1 explicitly requires a
declared IR/boundary prescription; the compact local construction supplies a
valid part of that domain. W3 retains classical master and measure/contact
insertions. W4 preserves Gamma_ref and background-only responses. W5/W6 require
whole connected products and correlated source/operator normalization. Their
complete Gamma target cannot be replaced by a local-field-algebra isomorphism.
No original clause supplies a preferred global interacting vacuum, asymptotic
scattering state or proof of a strict switching limit. These remain unproved
where physically needed; their absence is not an anomaly finding.

Moving a quadratic term from interaction to free reference is a different
comparison. Drago-Hack-Pinamonti, https://arxiv.org/abs/1502.02705 , develops
PPA for scalar non-derivative quadratic perturbations with explicit propagator
and contraction maps. That result is not a certificate for this mixed weighted
reference, derivative couplings or its global constant-vacuum limit. No such
resummation or new mass prescription is used in the present local comparison.

The proper next decision is therefore to preserve the completed compact
one-loop construction and its explicit source/reference functional, while
separating any indispensable global/PPA question from physical calculations.
Do not keep accumulating easy local cutoff identities as if they supplied a
physical state or fixed all finite source contacts. Read the active C1_GS and
scalar/matching contracts before selecting new physical inputs. Do not resume
human-paused matter/flavor or promote authority. A framework that organizes
existing calculations is not independent scientific validation of their premises.
