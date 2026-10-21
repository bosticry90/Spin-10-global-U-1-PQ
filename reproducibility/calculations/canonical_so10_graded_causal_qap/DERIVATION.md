# GQAP1 — a graded causal insertion principle and its finite chart conversion

Prospective pending completed native routes and separate verification. The
proof is through one loop, at arbitrary fixed finite local vertex order, in
the explicitly constructed compact/off-shell domain. It is not a measure,
physical-vacuum or all-loop equivalence theorem.

## 1. Actual free prerequisites and graded variation convention

Let p_i be the parity and d_i the standard dimension of z_i. The actual free
quadratic S0 has E_i=EL_i^L S0, of parity p_i and dimension4-d_i. CWB1/FCR1
qualify K C_F=C_F K=i delta I, K W=W K=0 in the actual graded dual frames.
No scalar positive metric or normally-hyperbolic assumption replaces these
mixed gauge/auxiliary/ghost identities. Sources and backgrounds are external.

For a homogeneous variation of parity r, put delta z_i=epsilon R_i with
epsilon on the LEFT and p(R_i)=p_i+r. Then

 delta_R F=sum_i R_i EL_i^L F.

This fixes ordering; it is not a right derivative formula. A source-left even
action word has a left Euler sign (-1)^(p_i*prefix_parity+jet_order). Right
differentiation gives the suffix sign and converts by (-1)^p_i because the
action is even. Every source monomial J_i R_i is even and has its original
J first. Its left J derivative is R_i with the PLUS sign.

The homogeneous free bisolution implies E_i star F=E_i F and F star E_i=F E_i.
In particular (F star G)E_i=F star(G E_i), with no reordering of the final E_i.
The Feynman product is different: contracting E_i in T yields i delta contacts.
Keep both identities. Quotienting E_i=0 would destroy the off-shell proof.

## 2. Anomaly construction on the same actual causal products

Write Gamma_V for the vertex functional insertion map, with tree value
Gamma_V(O)=O and Gamma_total=S0+Gamma_vert(V). For an even interaction V,
the anomalous ordered vector MWI is

 sum_i Gamma_V(R_i) EL_i^L Gamma_total
   =Gamma_V(sum_i R_i EL_i^L(S0+V)+Delta_R(V)).                 (1)

All products retain their displayed order. Arbitrary homogeneous interaction
arguments are polarized by external coefficients making each total vertex
even; the resulting Koszul signs give the general graded multilinear version.
These coefficients do not create integrated fields or canonical pairs.

Here Delta_R is DEFINED recursively, not assumed zero. In T language, multiply
the time-ordered insertion of R_i by the free E_i outside T and subtract:
the T insertion of R_i E_i; all contractions with interaction vertices, giving
the left local Euler variation R_i EL_i V including derivative delta currents;
and T insertions of the anomalies already determined at smaller vertex order.
The leading coefficient multiplying the new anomaly is T1=id, so this triangular
recursion uniquely determines it. Delta_R,0=0. No unknown number is fitted to a
desired Slavnov cancellation. The factors (i/hbar)^n are those fixed by W1 and
the COS1 cycle check. The same construction applies after projecting onto
one total graph loop; adding contractions cannot reduce the loop count.

Away from the total diagonal of the n interaction vertices and the R insertion,
choose a strict causal partition separating at least one vertex from the
insertion block. COS1 factorization pulls out the separated T product. Terms
with the same lower anomaly regroup with the SAME source-left signs into the
lower-order recursion, which vanishes by construction. Moving the final E_i
through that star factor is legitimate by section1, not by setting E_i to zero.
The other causal order uses the corresponding graded order. Thus Delta_n is
supported only on the total diagonal, including all proper collisions.

The Wick expansion is field independent: every uncontracted field of each
term remains at one of the insertion vertices. Therefore, when the vertices
coincide, all residual fields and their finite jets also lie there. Translation
covariance and finite scaling degree imply

 Delta_n(...;R)=sum_alpha partial^alpha delta(x1-y,...,xn-y)
                         P_alpha(z,J,A,jets)(y),              (2)

with a FINITE set of local polynomial coefficients at each specified order.
This is stronger than merely local support of a nonlocal field functional.
Classical tree contractions obey the ordinary graded chain rule and the actual
K C_F contact identity; tree peeling gives the classical MWI. Consequently
Delta_R starts at hbar, not at tree order. This is a local insertion principle,
not the assertion that its one-loop coefficient vanishes or is cohomologically
trivial. The QAP comparator is Brennecke–Dütsch, arXiv0801.1408, Theorem5.2;
the actual multiplet, parity, normalization and dimension arguments are explicit
here instead of substituting the scalar formula unchanged.

## 3. Heterogeneous power counting and all actual Euler directions

A component R_i E_i has dimension dim(R_i)+4-d_i. For arbitrary insertions
L_j the coefficient bound replacing the scalar theorem is

 |alpha|+dim P_alpha <= sum_j dim L_j + dim R_i +4-d_i -4n.    (3)

It follows by the actual free-edge scaling bound d_a+d_b, the vertex jet
degrees and local diagonal subtraction. For dim L_j<=4 this is at most
dim R_i+4-d_i. The actual BRST component has dim R_i=d_i, so its breaking
has standard dimension4, ghost1 and odd parity. Its project dimension is5,
as the ORIGINAL W1-W7 contract requires. A uniform scalar dim(R)+3 bound
would be wrong for ghost and auxiliary directions.

The actual35162 field-rule words give dim(R_i)=d_i, gh(R_i)=gh_i+1 and parity
1-p_i, for all643 outputs with their empty complement retained. Source words
J_i R_i have standard dimension4/ghost0/even. The full source Euler derivatives
have dimension4-d_i/ghost -gh_i/parity p_i, as required for QJ_i. All ordinary
GF rows obey the same renormalizable bound. All34 physical densities have
dimension4 from their literal AST and independently from their polarized
Hessian graphs. Their physical Euler terms therefore have dimension4-d_i;
they are not discarded because a field-rule output happens to be zero.
For example the singlet field rules are zero, while its quartic Euler derivative
is nonzero. The classical full master proof is a qualified dependency, not a
newly rerun dense polynomial calculation here.

## 4. Source insertions, Legendre signs and classical cutoff breakings

The contraction/extension map is independent of ordinary Legendre sources and
of the uncontracted BV coefficients. Differentiate before restricting sources.
The original convention j_i z_i gives EL_i^L(j_i z_i)=(-1)^p_i j_i, hence
EL_phi_i Gamma=-(-1)^p_i j_i. Differentiating the same vertex functional with
respect to J_i gives the insertion of EL_J_i S=R_i. No mean-field replacement
of nonlinear products is made.

For the odd BRST variation, p(R_i)=1-p_i, while p(EL_i Gamma)=p_i. Their
interchange sign is (-1)^[p_i(1-p_i)]=+1. Consequently the left hand side of(1)
is exactly the W1 source-left Slavnov functional sum(EL_i Gamma)(EL_J_i Gamma).
Its right hand side includes the renormalized insertion of the CLASSICAL
master breaking as well as Delta_R. If the bare full master functional vanishes
in the applicable integrated domain, the latter is the one-loop local breaking.
Jacobi gives its consistency condition; locality does not establish exactness.

Compact switching MUST be kept in this statement. S_g=S0+V(g) need not satisfy
the strict uncut master equation: derivatives of g and the associated currents
appear in S(S_g). Keep [S(S_g)]_Gamma in(1). No global g->1 limit, constant
nonlinear probe or unlabelled two-tangent extension follows. A first local QAP
is thereby constructed, but strict restoration for the original uncut heat
functional still requires the exact domain/current comparison. It is not a
license to drop regulator, measure or background-only contributions.

## 5. The T1 dictionary transports the finite primitive

Let H1[S] be the existing heat finite coefficient and b[S]=beta1(S). CWB1's
initial normalization and COS1 forest prescription give, on their common
fixed-reference coefficient domain,

 Gamma_T,1[S]=H1[S]-b[S],
 Gamma_T[S+hbar b[S]]=S+hbar H1[S] modulo hbar^2.              (4)

This comparison uses the COMPLETE physical action, not just GF/source terms.
The latter have qualified beta1 projections zero, including all643 source
outputs; the physical b[S] is generally nonzero. Neither the beta map nor a
heat reference change is assumed to be a global quantum field redefinition.

The finite tadpole jets are consistent with the free E_i module: for a scalar
reference mass squared M>0,

 FP integral Q^k e^-2tQ/(Q+M)=(-M)^k d_M,
 d_M=M[gamma_E+log(2M/mu^2)-kappa]/(16pi^2).                  (5)

Polynomial heat moments have zero finite constant; hence I_(k+1)+M I_k=0 for
every finite k. More generally K times the regulated covariance is i times
the pure heat identity; every finite pure-polynomial heat jet has zero finite
constant. Thus the local beta contraction has Kd=0 in both slots and
beta1(F E_i)=beta1(F) E_i. This proves compatibility of the local normalization
jets used in the QAP recursion; it does not assert a global positive Hadamard
state or quotient away E_i.

If the qualified heat primitive obeys Q C_heat=-Q H1 on that SAME uncut
coefficient domain, the primitive in the T1=id chart is

                  C_T=C_heat+b[S],
 Q(Gamma_T,1+C_T)=0 modulo the retained currents.             (6)

Using C_heat alone instead leaves -Q b[S]. No loop response of the order-hbar
action addition is required at this order; its tree source/operator/current
transport remains. This is the original strict first-order comparison, not
an arbitrary-strength or all-order equivalence theorem. For compact S_g retain
the classical switching insertion from section4; do not claim(6) abolishes it.

## 6. Nonzero physical control for the normalization sign

Use the actual physical Phi kinetic Hessian, whose scalar-scalar seagull is
g10^2 B_mu^a B^{b,mu} rho_a^t rho_b. Unit real kinetic coordinates and the actual
Phi generator matrices give

 b[S]_Phi,seagull=(g10^2 d_Phi/2) B_mu^a B^{b,mu}
                                       Tr(rho_a^t rho_b).     (7)

The direct quadratic scalar Hessian and an independent Frobenius trace compute
its actual coefficient. Transform the actual180 derivative B<-C rows to the
physical field/ghost frames before contracting this Gram row with the BRST
tangent. This yields the complete coefficient vector of
g10^2 d_Phi B0_0 partial0 C^k in Q b[S]; a nonzero component is an action-based
control against omitting beta1 or choosing the opposite sign in(6).

The reference-sector d_Phi is retained symbolically. A specially chosen kappa
could make it zero, which would make this isolated control insensitive; no
such normalization is selected. GF/source beta projections are zero by the
completed CWB1 census. Phi potential terms contain no B, scalar field rules
contain no differentiated ghost, and the first scalar derivative tadpole
vanishes. Thus they cannot cancel this B partial C coefficient in the d_Phi
sector. This is not a new physical vector mass or measured Slavnov anomaly.

The complete heat primitive may respect background H while this intermediate
flat T chart term alone need not. Simultaneous background-covariant transport,
Gamma_ref[A]/phase/member choice and the uncut domain must be reconciled before
claiming a single fully admissible restored physical prescription. Do not call
an algebraic chart relation a completed W2/A3-A5 construction.

## 7. Earned scope and next decision

The result sought is the actual graded compact-domain one-loop anomalous
insertion principle and its necessary finite chart comparison. It supplies
the missing causal/locality component of A2 in this bounded domain. It does
not identify the whole A1-A5 class as proved, calculate every anomaly tensor,
construct multiple independent nonlinear Ward products, prove physical
unitarity, resume flavor or qualify E5/A5. No new physical scheme is adopted.
The next exact dependency is comparison of the source/background/current and
constant-quadratic reference domains, using the completed original finite
primitive and preserving all physical quantum-control limitations.
