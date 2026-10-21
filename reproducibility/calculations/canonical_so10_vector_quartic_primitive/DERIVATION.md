# VQP1: covariant coincidence, Wick contraction and the bare Laurent coefficient

Use BFT1's Euclidean source-zero linear background gauge at xi1. On an
H-valued covariantly constant Cartan background, P_r commutes with T=ad(h)
and the tree mass. Give P0 only an auxiliary positive mass delta. For fixed
delta>0 the F2 coefficient is an analytic local coefficient measured by a
weak magnetic plane, with the small-field derivative taken first. Its
delta->0 behavior diagnoses IR dependence; the massless constant-background
functional itself is not inferred from the massive heat-boundary argument.

For physical background F_munu, Omega_munu=g T F_munu and
Kv=-Dbar^2 delta_munu-2 Omega_munu+x. The coincident inverse is

 G_munu = sum_r [ P_r delta_munu A_r
       +2g (P_r T) F_munu B_r
       +g^2 (P_r T^2)(delta_munu F_ab F_ab/12
                            +2 F_mualpha F_alphanu) C_r ] +O(F3,DF),

where the common loop measure is normalized by16pi^2,

 A(x)=x exp(e gamma_E)(Q^2/x)^e Gamma(e-1),
 B(x)=  exp(e gamma_E)(Q^2/x)^e Gamma(e),
 C(x)=x^-1 exp(e gamma_E)(Q^2/x)^e Gamma(1+e).

The orbital heat factor is1+s^2 Omega_ab Omega_ab/12; the spin factor is
exp(2s Omega_munu). They commute here. Tr_L F_matrix^2=-F_ab F_ab fixes
the relative spin/orbital sign. This inverse heat kernel solves the SAME
massive minimal operator as the Neumann inverse; differentiating twice gives
G K_h G K_k G +G K_k G K_h G -G K_hk G. Applying the product rule to its
two edges therefore includes exactly BFT1's eight labelled placements; no
constant-connection p=0 projection or deletion of its seagull is used.

The quartic density from the actual gauge action is
g^2 f_abe f_cde Q_mu^a Q_nu^b Q_mu^c Q_nu^d/4. Its three Wick pairings
are (ab)(cd), (ac)(bd), (ad)(bc). At zero background the first vanishes;
the other two give D(D-1) sum_rs W_rs A_r A_s, before the1/4 density weight.
This reproduces the BFT1 C4/8 symmetric-vertex convention without fitting a
two-loop coefficient. The quartic has no explicit background vertex.

Put F_e,ab=f_abe (a real antisymmetric color matrix), S_r=P_r T^2 and
U_r=P_r T. Define

 X_rs=sum_e,abcd f_abe f_cde (S_r)_ac(P_s)_bd
     =-sum_e Tr(S_r F_e P_s F_e),
 L_rs=sum_e [sum_ab f_abe(U_r)_ab][sum_cd f_cde(U_s)_cd],
 Y_rs=sum_e,abcd f_abe f_cde(U_r)_ad(U_s)_bc
     =-sum_e Tr(F_e U_s F_e U_r),  Z_rs=L_rs-Y_rs.

L,Y,Z are symmetric in r,s; X need not be. All mass/projector orders remain
explicit. The (ab)(cd) pairing gives4 L_rs B_r B_s; the (ac)(bd) pairing
gives2D(D/12-2) X_rs C_r A_s; the (ad)(bc) pairing gives
-2(D/12-2) X_rs C_r A_s -4Y_rs B_r B_s. Hence

 Gamma2_Fphys2/ell^2 = g^4 {[(D-1)(D/12-2)/2] sum_rs X_rs C_r A_s
                              +sum_rs Z_rs B_r B_s}.

No background or Ward coefficient was used to choose these contractions.
The external normalization is important: the existing MST1/FCI1/HTB1 Lambda
strips the two external couplings, Lambda2=-12 Gamma2_Fphys2/(ell^2 g^2).
For example the one-loop real scalar has Gamma1_Fphys2/ell=g^2 tau J/24,
so Lambda1=-tau J/2, exactly FCI1. Vector-only gives(10+e)tau J and complex
ghost+tau J, exactly HTB1. Thus the primitive Lambda2 is

 g^2 { (30-17e-2e^2) sum_rs X_rs C_r A_s -12 sum_rs Z_rs B_r B_s }.

All occurrences of F2 here mean F_munu F_munu, not merely one B^2 component;
one magnetic plane has F2=2B^2. Overall hbar/16pi^2 factors are already stripped.

## Entire mass-assignment Laurent coefficient, before subtractions

Set x_r=60g^2 k_r, k=(d,1/200,1/40,5/12,253/600), d=delta/(60g^2)>0.
Write z=log(Q^2/60)-log(g^2), l_r=log k_r, j_r=z-l_r. Then

 C_r A_s=(k_s/k_r)[-1/e-1-j_r-j_s+O(e)],
 B_r B_s=1/e^2+(j_r+j_s)/e+(j_r+j_s)^2/2+zeta(2)+O(e).

Consequently Lambda2_VVVV/g^2 has coefficients

 p2=-12 sum_rs Z_rs,
 p1=-30 sum_rs X_rs k_s/k_r -12 sum_rs Z_rs(j_r+j_s),
 f0= sum_rs X_rs(k_s/k_r)[-13-30(j_r+j_s)]
        -12 sum_rs Z_rs[(j_r+j_s)^2/2+zeta(2)].

The constant -13 contains the dimensional17 correction and is NOT -30.
B's epsilon terms contribute the finite zeta(2) and square-log terms when
multiplied by another pole. Renormalizing individual B functions first would
give another expression; this is explicitly the BARE primitive Laurent
coefficient, not its forest-renormalized value. It must not be added as if
its double/single poles or finite subdivergence pieces were already removed.
The full simple SO10 sum obeys sumX=-64, sumL=64, sumY=-32, sumZ=96 for
every unit normalized probe. Thus p2=-1152 is a sensitive absolute check,
not a complete two-loop beta coefficient.

All25 ordered assignments enter these equations, including zeros fixed by
actual contractions. Expansion in d has powers-1,0,+1 and log d degree<=2.
Keep the coefficient of d^-1 at every log power and the nonconstant log d
terms at d0. These are IR-sensitive terms of this regulated family; they
are not identified with UV counterterms or declared anomalies. At positive
delta the heat integrals have a common convergence strip Re(e)>1, and their
meromorphic continuation defines the displayed Laurent coefficients. Taking
delta->0 before this construction changes the problem.

The common OSF1 soft/EFT cancellation is an input identity, not a license to
drop this explicit d dependence without constructing its complete partner.
Graph-level UV forests and all required primitive/CT companions must be
reconciled before this becomes a finite hard matching contribution. No new
finite parameter/tadpole condition, source-normalization law or physical IR
prescription is adopted.

Published primary comparators checked for applicability: Ananthanarayan,
arXiv0808.2781 section3 (mass factorization and covariantly constant vector
kernel); Martin-Patel1808.07615 (actual gauge quartic vacuum topology, not this
background-kinetic amplitude); Fuentes-Martin etal2412.12270v2 appendixD
(scaleless overlaps in expansion by regions, not this model's missing common
gauge/EFT construction). Existing MVM1 fixes the dimensional master convention.
Agreement with these comparators does not adopt their actions or prove the
full C1/QAP/gauge-restoration requirements.
