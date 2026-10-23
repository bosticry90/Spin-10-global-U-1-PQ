# SRG1: stationary parameter flow from measured pole kernels

Let A_alpha be the SIMPLE-POLE coefficient of a PARENT PARAMETER,
p_alpha,B=mu^(d_alpha epsilon)(p_alpha+ell*A_alpha/epsilon),
d_alpha=n_alpha-2 for a scalar degree-n monomial and d_g=1. Differentiate
the bare definition before taking epsilon0. With E=sum d_beta p_beta partial_pbeta,

 beta_alpha^(1)=(E-d_alpha)A_alpha.

Every one-loop scalar CT monomial has E weight d_alpha+2, including the
quadratic/cubic parameters. Thus beta_alpha^(1)=2A_alpha. Verify this on
ALL recovered RSC polynomial monomials, not only quartic examples. This
does not double a field-endpoint or gauge-reference two-point pole blindly.

SQP explicitly separates Hpar,Href,Hend. At xi1 the reference pole is
d_BVN=2Cv in scalar coordinates, or(20,25,0) in raw fractional coordinates,
times g². Its scalar potential contribution is Href=2TC, TC=V'''[Cv].
The surviving FCI potential jet is Hp=Hpar+Href. Pure parameter gauge2
Hpar=-3(TC+CH+HC)/2; full field-endpoint-containing Htotal is different.
RSC0 and GQH4 are invariant parent potential counterterms as already
qualified. Their one-point derivatives and all fixed-field Hessians exist.

Write t_CT=T0+g²T2+g4T4 for the actual UTP cancelling tadpole residue.
Then t_CT=t_par+M*d_BVN (with d_BVN only at orderg²). At a stationary
parent expansion point, its PARAMETER coordinate pole satisfies

 a_stat=-M^-1 t_par=d_BVN-M^-1 t_CT.

This follows by differentiating tree stationarity, not from the finite
quantum minimum. Let d=M^-1 t_CT, D_j=partial_hj H at fixed parent inputs.
FCI's prescribed scalar potential jets P=(RSC0,Hp,GQH4) therefore convert to

 A_H,stat=P-sum_j d_j D_j.

The distinct replay construction is RSC0+g²Hpar+g4GQH4+
sum_j(a_stat)_j D_j. These must agree in every matrix slot. The gauge2
jet reduces exactly to -3(CH+HC)/2 because d2=Cv/2 at this point.

Differentiated stationary invariance implies Pg*A_H,stat*Pg=0. It does
NOT imply A_H,stat*Pg=0: the orbit can rotate into physical massive
directions. Keep mixed columns. Consequently no inverse-g² scalar
POTENTIAL-Goldstone trace survives in the stationary RG direction.
This is an operator test, not a deletion based on the desired RG identity.

The vector mass pole from FCI includes d_BVN and delta_g/g=a_g*g²/epsilon,
a_g=-23/3. Replace the physical VEV motion by a_stat, retaining the
same coupling pole. In mass sector r, with lambda_r and rank n_r,

 (delta x_r/x_r)_stat,p = delta_(p,2)*j_FCI,r
   -sum_j d_p,j * Tr(P_r partial_j G)/(n_r lambda_r).

The simultaneous reference update contributes opposite scalar-GF and extra
half-ghost first traces, as qualified in HTB; they cancel only together.
Hence the physical stationary threshold derivative uses the complete
vector-multiplet factor -21/2, plus physical scalar mass derivatives. This
is only the current one-loop heavy F2 projection, not full gauge equivalence.

Primary computes these stationary scalar/vector jets and their traces.
Equivalently, with F the measured FCI pole coefficient and R the fixed-reference
HTB leaf, the closed-response replay is

 W=2*[F-R M^-1 t_CT].

Since t_fin,L=-t_CT in the actual heat/MSbar tadpole and the HTB bridge is
-R M^-1 t_fin, its measured linear scale coefficient is B_L=R M^-1 t_CT.
Therefore W=2(F-B_L). This is a derived independent input direction, not
W inferred from a two-loop amplitude slope. Inverse-g² cancellation can be
tested exactly, while powersg0,g2,g4 remain as measured numbers/matrices.

## Independent scale/forest grading check

At fixed renormalized inputs a genuine two-loop background F2 graph carries
exp(2epsilon*L); an original one-loop proper-CT closing carries exp(epsilon*L).
The dimensional vertex grading proves this even with cubic couplings and
VEV-induced vertices: coupling degree n-2, VEV degree-1, and
sum_vertex(n-2)=2*loop_number for two background legs. A one-loop CT removes
two epsilon-grading units, in agreement with the pole-to-beta identity.
Counterterms are Laurent poles, not unexpanded subgraph integrals.

Write these two contributions as B(epsilon)exp(2epsilon L) and
C(epsilon)exp(epsilon L). Denote their double/simple Laurent coefficients
by B2,B1,C2,C1. G2P qualifies zero COMBINED double pole and zero quadratic
finite L term: B2+C2=0 and2B2+C2/2=0, so B2=C2=0 in the total. Then

 F_G2P,L=2(B1+C1)-C1=2*P_Rprime-F.

Here F is the actual whole original proper-CT closing pole, identified
with the FCI trace by GCT/HPR on CBR's heavy projection. The original
overall R-prime pole is independently measured and equals(3/2)g²dc_GS.
The MSbar overall subtraction is pure pole; it supplies no finite L term.
The raw1PI versus reduced tadpole ownership is essential: add HTB once.

 Thus 2*(F_G2P,L+B_L)+W=6g²dc_GS.

This structural scale statement inherits the qualified dimensional
homogeneity, complete forests and common soft subtraction of its inputs.
Separately compare actual complete retained finite slopes at g²1/2,1;
samples corroborate implementation, not an all-coupling numerical theorem.
If actual values disagree, preserve the defect and investigate normalization
or coverage. Never solve for W or a counterterm from that defect.

Retain BMC's distinction from the old full-matter/Yukawa-independent beta
target. Only the BOSONIC GS scope is tested. No numeric C1 or gauge target
comparison. The parent MSbar finite inputs and all protected physical
limitations remain; a formal RG direction is not a controlled quantum vacuum.
