# VSP1 derivation frozen before calculation

The actual kinetic quartic is -g^2 Q_mu^a Q_mu^b eta^T rho_a rho_b eta/2.
Contract its distinct species once: Gamma2=-g^2 sum_abmu Gv_ab,mumu
Tr(rho_a rho_b Gs)/2. Equivalently differentiating Q^2 eta^2 yields the
species-normalized C4/4. There is no sunset or ghost in THIS family.

Let L(M)=-sum_ab M_ab rho_a rho_b. With actual vector mass projectors Pr,
A_r=L(Pr), B_ri=L(Pr S_i), S_i=sum_{h in ideal i} ad_h^2/n_i, n=(1,3,8).
All M are symmetric H-invariant matrices. Do not use a single Cartan squared
on a reducible mass set. H invariance follows by the inherited rho Lie law
and NEW checks [M,ad_H]=0 for all12 directions. The qualified complete SM
lowering frame then permits projection to its65 normalized highest weights.
Full frame Q is NOT unitary: Qi=diag(Q.H Q)^-1 Q.H. Seeds alone have norm1.
The replay contracts (rho_a Qseed).H (rho_b Qseed); primary uses literal
full rho products. Reconstruct every full operator through Qi, including zeros.

For a normalized H curvature T, coincident vector inverse through F2 is
Pr A_v delta +2g Pr T F B_v+g^2 Pr T^2 (delta F2/12+2Fmatrix^2) C_v.
Scalar inverse is A(X)+g^2 rho_H^2 F2 C(X)/12; X=H+g^2 OO.T commutes H.
Scalar has no linear Lorentz-curvature term; vector linear trace is zero.
Hence no B_v B_s product. The Lorentz traces are a_D=D/12-2 and b_D=D/12.
For block b of representation dimension d_b and real index tau_bi,
u_rbi=d_b B_ri,b, w_rbi=-tau_bi A_r,b. No commutation of A_r or B_ri with
the potential H is assumed. Ordinary ordered multiplicity traces suffice.

Gamma2_F2/ell^2 = g^4/2 sum_rb [a_D C(xr) Tr(u A(X))
                                      +b_D A(xr) Tr(w C(X))].
Lambda2=-12 Gamma2_F2/(ell^2 g^2), ell=1/(16pi^2).
The covariant coincident expansion is the local F2 projection of the exact
two distinct labelled resolvent variations G_h=-G K_h G,
G_hk=GKhG KkG+GKkGKhG-GKhkG. On two edges this is2*3+2=8 placements.
The two cross-edge linear terms vanish by Lorentz contraction, not by p=0.
No constant A substitution occurs before differentiation; F remains explicit.

Set H_eps(x)=exp(gammaE eps) Gamma(1+eps)(Qscale^2/x)^eps,
A(x)=-x H_eps/[eps(1-eps)], C(x)=H_eps/x. With jv=log(Qscale^2/xv),
js=log(Qscale^2/xs), U=u xs/xv and W=w xv/xs, Lambda2/g^2 per eigenpair:
bare pole=-10U+2W; bare finite=-U[11+10(jv+js)]+W[1+2(jv+js)].

Derive graph-local minimal UV CTs by closing ONE actual tadpole first.
The scalar-loop pole is -xs/eps, leaving a_D C_v. Its CT has pole10U,
finite U(1+10jv). The vector-loop pole includes its CLOSED Lorentz trace D;
project the pole at D=4, leaving scalar C_s. CT pole=-2W, finite=-2W js.
These are actual local subgraph UV projections, not fitted counterterms.
Thus graph-local R_MS pole0 and finite -10U(1+js)+W(1+2jv).
Keeping D inside the CLOSED vector pole changes the finite W coefficient;
premature D4 in the bare graph changes it too. Retain both diagnostics.
There is no double pole: every term is A*C, C ultraviolet finite.

For r>0 and positive scalar subspace this gives
 Lambda_R =g^2 sum_ri {-10/xr Tr[u_ri X(1+log(Qscale^2/X))]
                  +xr(1+2log(Qscale^2/xr)) Tr[w_ri X^-1]}.
Keep physical H290 and Goldstone g^2 lambda33 separately, not soft zeros in
a numerical inverse. Analytic null projectors from FCI define exclusions.
Serialize g^0,g^2,g^4 coefficients with L=log(Qscale^2/60), Ulog=log(g^2).
No g or scale chosen and no model parameters retuned.

IR/EFT: put the SAME auxiliary mass delta>0 on vector P0 and scalar Psoft.
Write F(Gvh+Gvl,Gsh+Gsl), bilinear in propagators at the literal vertex.
Open the hard scalar loop: Sigma_v,ab,mn=-g^2 delta_mn Tr(rho_a rho_b Gsh).
Open hard vector loop: Sigma_s=-g^2 sum_abmu Gvh_ab,mumu sym(rho_a rho_b).
The actual mixed closures are 1/2 Tr Gvl Sigma_v and1/2 Tr Gsl Sigma_s.
Restricted tree VVSS is the same literal tensor on V12 and Psoft5.
rho_H preserves Psoft, rho_H v=0 and O.T rho_H Psoft=0 imply no leading
heavy exchange modifies this two-vector/two-soft-scalar tree vertex: the
heavy-vector/light-vector/soft-scalar VVS cross term also vanishes. Retain
and test the actual matrices instead of invoking an abstract EFT equality.
Therefore FULL-OPENED_HS-OPENED_SH-EFT=HH before eps expansion or delta0.
The graph-local UV projection above is linear in each tadpole mass, so this
identity holds with those same CT attachments at fixed delta. No arbitrary
scaleless discard or universal IR regulator theorem is asserted. This family
factorizes; this proof is not a momentum-region theorem for sunset graphs.

Exact-once: R_VVSS=B_VVSS+C_VVSS and parent insertion C_parent implies
R_VVSS+(C_parent-C_VVSS)=B_VVSS+C_parent. Do NOT sum R_VVSS+C_parent.
No change to the old FCI or HTB values; their source/width/tadpole obligations
remain. This graph-local grouping is not a new physical finite prescription.
