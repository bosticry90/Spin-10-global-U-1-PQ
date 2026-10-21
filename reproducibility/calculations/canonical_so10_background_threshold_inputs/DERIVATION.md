# BFT1 derivation frozen before execution

Let rho_a be real antisymmetric matrices in the orthonormal physical scalar
frame, [rho_a,rho_b]=f_ab^c rho_c, O_Ia=(rho_a v)_I. The parent normalization
uses plane generators (E_ij-E_ji)/sqrt2, Tr_10(h_a^T h_b)=delta_ab.
The phi20 realification has index2, so f_ab^c=-Tr_20(rho_a rho_b rho_c).
These are kinematic representations of the frozen parent, not a new action.

Dbar=partial+g rho(A), delta eta=-g rho(c)(v+eta), sQ=Dbar c+g[Q,c].
Use Euclidean F=Dbar.Q+xi*g O^T eta, Sgf=F^T F/(2xi). It cancels
the kinetic mixing -g eta^T O Dbar.Q. With sbarc=b, sb=0 and gauge fermion
barc(F-xi b/2), sPsi=bF-xi b^2/2-barc sF. The b contour is parallel to the
imaginary axis through F/xi; its Gaussian gives Sgf and an A-independent
normalization. This is not a positive-real b integration. BRST statements
before elimination are off-shell; elimination does not establish off-shell
nilpotence on barc. Minkowski F_M=partial.Q-xi*g O^T eta and -F_M^2/(2xi)
Wick rotate to this Euclidean prescription with the usual vector phases.

The Faddeev–Popov density is, in the fixed ordered barc,c convention,
barc[-Dbar^2-g Dbar ad_Q+xi*g^2 O^T O+xi*g^2 T.eta]c,
T_abI=sum_J O_Ja (rho_b)_JI. Integrating the vector term by parts gives
+g (Dbar_mu barc)_a f_db^a Q_mu^d c_b. The Lie and polarized-Gram identities are

    T_abI-T_baI=f_ab^c O_Ic,
    partial_I Gram_ab=-(rho_a O_b+rho_b O_a)_I,
    T_abI=(partial_I Gram_ab+f_ab^c O_Ic)/2.

Sum_I v_I T_abI=Gram_ab, but v.O_c=0 makes this control insensitive to the
antisymmetric term. Keep a full coefficient/antisymmetry test as well.
rho_H v=0 and rho_H O=O ad_H, together with the inherited full representation
algebra, prove H covariance of these tensors. No derivative-free projection
is substituted for local background covariance: Dbar supplies its affine jets.

At xi=1 the tree Hessian is block diagonal in Q,eta,ghost even for varying
H background (Dbar v=0). Its masses are g^2 Gram, V''+g^2 OO^T and g^2 Gram.
Potential Goldstone nullity at a stationary point is inherited evidence, not
a fresh full328 Hessian computation here. The exact Gram spectrum/multiplicity
is0:12,3/10:8,3/2:1,25:12,253/10:12, with omega^2=60; dividing by60 gives
the frozen vector ratios(.005,.025,50/120,50.6/120). This is no choice of g.

Write S_int=C3 q^3/3!+C4 q^4/4!+barc V(q)c, with derivatives/momenta kept
inside the vertices. Ordinary Legendre sources cancel all linear vertices
and 1PR connected vacuum dumbbells in Gamma. Bosonic two-loop vacuum terms:

    Gamma2_b=+C4 G G/8-C3 C3 G G G/12.

There are3 quartic Wick pairings. Of15 pairings between two cubic vertices,
6 have all3 cross edges (1PI) and9 have one bridge (1PR); exp factor1/72
gives1/12. The latter are canceled by the Legendre transform, not assumed zero.
Mixed VVSS gives1/4 and VVS/VSS sunsets -1/4 when those species-normalized
vertices are used. Identical VVV/SSS retain -1/12. Ghost integration first
gives -Tr log(Kc+Vq); its second term is +Tr(Gc Vq Gc Vq)/2. Contracting q
therefore gives +1/2 for each oriented ghost sunset, with no extra ghost sign.
Generic symmetric superfield formulas require the same ordering convention.

With only degree3 and4 interactions, L=I-V+1=2 and2I=3n3+4n4 imply
n3+2n4=2. Block-diagonal propagators permit exactly these species families:

* quartic: VVVV,VVSS,SSSS;
* bosonic sunsets: VVV,VVS,VSS,SSS;
* ghost sunsets: barc c V,barc c S.

No quantumquarticghost arises from this linear gauge fixing. Abar-Q-barc-c
has quantumdegree3 and one external background, not quantumdegree4. Internal
scalar singlets, Goldstones, light Higgs and massive mixed modes remain in S.
Tadpoles from genuine1PI doublebubbles are retained. This topological proof
is complete for the gauge/scalar/ghost subaction, not for fermionic diagrams.

For two DISTINCT labelled background variations h,k,

    G_h=-G K_h G,
    G_hk=G K_h G K_k G+G K_k G K_h G-G K_hk G.

K has backgrounddegree<=2. C4 has degree0. VVV,VSS,barc c V cubic vertices
have degree<=1; VVS,SSS,barc c S have degree0 because A is H-valued and
Dbar v=0. Count raw ordered insertion words before graph automorphisms:
two-edge doublebubble:2*3+2=8. Three-edge sunset:3*3+3*2=15.
If both vertices have first derivatives add12 edge-vertex and2 vertex-vertex
words, giving29. Total3*8+3*29+3*15=156. These are symbolic placements,
not distinct integrals, nonzero coefficients or independently measured graphs.
Keep derivatives and external momenta until the transverse p^2 projection;
constant A or p=0 before differentiation loses the kinetic threshold.

At order hbar^2 counterterms also give

    1/2 Tr_b(G_b deltaK_b)-Tr_c(G_c deltaK_c)+deltaS2[A].

There are6 generic labelled words for Tr(G deltaK):3 from G_hk,2 cross
terms and1 deltaK_hk. One-loop cubic/quartic CTs inside the two-loop skeleton
are order hbar^3, so do not belong here. Full deltaK is a Hessian of the
counterterm action, including background-dependent terms. Off-diagonal VS
deltaK alone has zero trace against block-diagonal G(A); this is not evidence
that its diagonal/mass/width partners or other Green functions can omit it.

Distinct gauge-width CTs are essential even at tree Feynman gauge. A commuting
two-width diagnostic F0=Dbar.Q+g sqrt(X1 X2) O^T eta, Sgf=F0^T X1^-1 F0/2,
gives at Xj=I+hbar dXj: vector longitudinal coefficient -dX1;
scalar GF mass g^2 O dX2 O^T; ghost mass g^2(dX1+dX2)Gram/2; residual mixing
+g eta^T O(dX2-dX1)Dbar.Q/2. Setting dX1=dX2 too soon erases this slot.
This does not assert two widths exhaust the full H-covariant CT module;
deltaK remains general and repeated-irrep mixing is not discarded.

At a tree stationary point, parameter/VEV counterterm bookkeeping is
delta t_CT=V'' delta v_CT+sum_alpha (partial_palpha t) delta p_alpha.
The physical one-loop shift v1 instead obeys V'' v1+t1_ren=0 on the physical
singlet subspace. These are distinct objects. Do not set their finite parts,
identify pole and MSbar masses, or infer a VEV shift from matching residuals.

The inherited one-loop D=4-2epsilon heat coefficient uses vector
(D/12-2)/2, Goldstone1/24, complex ghost -1/12, total -7/8-epsilon/12.
It gives scalar-log ratio -21 and finite/log(mass^2) ratio -2/21, hence the
frozen T_i[1-21log(M/scale)] convention. This regression is not the two-loop
diagram evaluation or a test of arbitrary gauge independence.

References (primary): Martens, arXiv:1011.2927v2 section2.1,2.2, defines two
independently renormalized widths and uses on-shell masses with MSbar gauge
couplings/fields. Its single-GUT-VEV finite result is not applicable here.
Martin–Patel arXiv:1808.07615 sectionII–III gives a generalized gauge-fixing
and vacuum-topology comparator; it is not this model's background-kinetic
matching calculation. Shared published conventions are not independent data.
The original C1 contract does not specify every finite mass/VEV/tadpole
condition. Keep these slots symbolic; a numerical C1 needs a legitimate
complete prescription or a derived scheme-conversion law, not arbitrary zeros.
