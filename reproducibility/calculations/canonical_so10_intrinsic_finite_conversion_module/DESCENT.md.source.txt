# Prospective source and mass descent; requires IFC receipts

Let l32=log(3/2), l43=log(4/3). Use actual Qx=R_a x C_a and qC=A(CC),
with the transported ghost chart and the positive source Euler rule.
For a scalar vector V and source-first polynomials J W(C),

    d0(V)_a = R_a V,
    d1(W)_ab = R_a W_b - R_b W_a - W A_a[:,b].

These formulas follow by differentiating the actual source action:
qJ_i contains sum_j J_j R_a[j,i] C_a. Applying q to J_i C_a has the
minus sign from the odd source, hence the QC contribution has a minus.
For higher degree use the full odd Leibniz rule, not a commuting ghost
calculus. The ghost source action must supply the same transported A.

For the measured C= rho J V + u J U(C) + u D(M), its Jx-dependent
first variation at the specified means is

    (q+d)C |_sources = rho J H(C) + u J F(CC),
    H=U-d0(V), F=d1(U).

Here V=-l32 T, U=l32 W0-l43 W2. Thus

    H=l32(W0+R T)-l43 W2.

This is the exact source remainder against the sole FIS lift. If nonzero,
it cannot be removed by adding the same canonical scalar translation to
all partners: U->U+R Z and V->V+Z leaves H invariant. F is also invariant
since d1 d0=0. No parameter is divided out or normalized to0.

From the actual representation and ghost Jacobi identities, d1(H)=F
and d2(F)=0. The resulting second source variation vanishes. This is
compatibility of the source descent; H or F themselves need not vanish.
The curved full chiral operation is retained. Ihat is source-independent
and has no scalar/source slot, so this source subcalculation does not
assert that Q_full is globally nilpotent.

The allowed source types and actual scalar transformation give a useful
closure of this projection: no other source variable has an Euler term
proportional to Jx unless Qx depends on its conjugate field. Actual Qx
depends only on x,C. The C source is outside this local type budget;
other retained source companions therefore cannot secretly change H/F
at these means. This is a projected applicability statement, not the
complete action's counterterm space or anomaly cohomology.

For the corrected alternating mass convention the rhoPP coefficient of
(q+d)C is M-BV. It must be compared against MINUS the measured IRR heat
root. With M=-2 B T l43 it is B T(l32-2l43)=-B T log(32/27).
Use the actual Nambu/source pairing to check this sign in the code.
For uCPP it is the ordinary mass variation plus B U. For holo matrices,
variation(M)_c=ig(Tc^T M+M Tc); anti has -ig(Tc Mbar+Mbar Tc^T).
Actual B R=-ig L(Tc)B (and the separately checked anti version) relate
the two routes. Compare against MINUS the measured IRS finite root.
This equality is a reuse of independently measured quantum roots; the
new H/F source coefficients are not thereby separately measured roots.

An explicit local polynomial with these coefficients specifies the
conversion on the three measured carrier families. It need not be a
Q-closed restoration counterterm. Neither locality and covariance nor
this projected descent proves an absolute renormalized prescription,
full source involution or a physically accepted finite normalization.
