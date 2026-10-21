# QIR1: an actual quartic light matching construction at fixed positive IR mass

All statements here are for the BFT1 source-zero vector quartic family at xi1,
the retained F2 coefficient, and the shared positive auxiliary delta on P0.
VQP1 supplies the full regulated bare amplitude. This work supplies its missing
actual mixed and all-light partners, not a theorem for the other eight families
or a global Slavnov-invariant auxiliary-mass prescription.

Let G_h be the positive-heavy color part of the exact vector inverse and G_s
its P0 part, with identical background, delta, dimensional measure and scale
on the UV/EFT sides. For the symmetric quartic tensor C4,

 V[G_h+G_s] = C4(G_h+G_s)(G_h+G_s)/8,
 Sigma_h = C4 G_h/2,
 V[G_h+G_s] -(1/2)Tr G_s Sigma_h -C4 G_s G_s/8 = C4 G_h G_h/8.

This is an ordered tensor identity, not an assignment of unknown coefficients.
The independently defined Sigma_h is the actual quartic contribution to the
one-loop two-point matching kernel. OSF1 handles its correlated UV/EFT CTs
through the common bare two-point equality; their values are not chosen here.
For this factorized diagram the remainder has only positive-mass inverses.
The proof disposes of its actual light assignments before taking delta0; it
does not equate field mass type and momentum region in arbitrary diagrams or
invoke an unseparated scaleless rule. No general all-hard matching theorem is
inferred from this example.

## Open the original action through second curvature

Write the quartic density g^2 f_abe f_cde Q_mu^a Q_nu^b Q_mu^c Q_nu^d/4.
For a covariance component M_ab L_munu with M^T=sigma M and L^T=sigma L,
sigma=+1 or-1, differentiate all six unordered field-slot pairs and both
external source orderings. With F_e,ab=f_abe define

 K(M)=-sum_e F_e M F_e,
 J(M)=sum_e F_e sum_ab f_abe M_ab.

The resulting open Hessian is exactly

 Sigma[M,L]/g^2 = K(M) delta_munu tr_L L
                                  +[J(M)-sigma K(M)] L_munu.

For symmetric M, J(M)=0. For antisymmetric M, trL=0 and the sign is J+K,
not J-K. The factor1/4 and external-source transpose are essential. Native
replay checks the actual45x45 matrices via the six slot derivatives, with
the unsummed vector indices retained. Check D4 and6, using the proved degree1
bound for a single internal Lorentz trace; no epsilon term is discarded.

In VQP1 the heavy coincident propagator has components

 P_s delta A_s,
 2g(P_s T) F B_s,
 g^2(P_s T^2) L2 C_s,
 L2=delta F_ab F_ab/12+2 F_matrix^2.

Thus its actual opened kernel is

 Sigma_h = g^2(D-1) sum_{s>0} K(P_s) delta A_s
       +2g^3 sum_{s>0}[J(P_sT)+K(P_sT)] F B_s
       +g^4 sum_{s>0} K(P_sT^2)[delta trL2-L2] C_s.

All full matrices are retained. Closing on the light propagator yields, in
the existing Lambda2/g^2 normalization,

 sum_{s>0} { kappa(e) [a_s C_0 A_s+c_s C_s A_0]
                                          +24 b_s B_0 B_s },
 a_s=Tr(P0 T^2 K(P_s)),
 b_s=Tr(P0 T [J(P_sT)+K(P_sT)]),
 c_s=Tr(P0 K(P_sT^2)),
 kappa(e)=30-17e-2e^2, D=4-2e.

Direct contractions give a_s=X_0s, b_s=-Z_0s, c_s=X_s0 of VQP1. These are
tested against the independently measured tensors, not used to determine
the opened kernel. The minus sign in tr_L F_matrix^2=-F_ab F_ab fixes the
BB trace orientation. This reproduces every mixed assignment including the
entire inverse-d, logarithmic and d log terms. The c_s term vanishes only
coefficient by coefficient as d log^k d ->0 after the Laurent expansion; it
is preserved until the full subtraction is verified.

## Construct the actual pure-light tree partner

Use the physical orthonormal planes h_ij=(Eij-Eji)/sqrt2. In the five plane
Cartans take Y=(-2,-2,-2,3,3)/sqrt30. A weak basis is their last difference,
(-h_69+h_78)/sqrt2 and(h_68+h_79)/sqrt2. A color basis comprises the first
two normalized traceless Cartans and, for each complex-plane pair p<q<3,
(-h_{2p,2q+1}+h_{2p+1,2q})/sqrt2 and
(h_{2p,2q}+h_{2p+1,2q+1})/sqrt2.

The embedding V: R12 -> R45 satisfies V^T V=I, VV^T=P0, O V=0. Directly
check(1-P0)[V_i,V_j]=0 for all144 brackets, using actual f. The restricted
brackets fH_ijk=V_k^T[V_i,V_j] therefore have the same kinetic metric and
quartic density as the parent on its light subspace. Invariance of that metric
also forbids a heavy-light-light gauge cubic. O V=0 makes the linear
light-vector/light-vector/heavy-scalar mass vertex vanish, since each term
in its derivative Gram factor contains O_H. Thus there is no heavy tree
exchange changing this leading four-light-vector vertex. This does not
eliminate unrelated tree exchanges or higher operators in the whole EFT.

With the same tree g and gauge/background normalization, the independently
computed12-dimensional fH quartic has the same mass-delta Gaussian as G_s.
Its F2 coefficient is the exact all-light term C4 G_s G_s/8. Beyond-tree
field/coupling matching and the other families remain separate; no freedom
is fixed by this restricted construction.

## Remaining coefficient and authority ceiling

The full VQP1 bare coefficient minus the actual mixed closure minus this EFT
quartic is therefore independent of d BEFORE taking d0. Each epsilon Laurent
coefficient agrees with a direct sum over r,s>0 of

 kappa(e) X_rs C_r A_s -12 Z_rs B_r B_s.

Output the exact double pole, single pole and finite polynomial in
z=log(Q^2/60)-log(g^2), h1=log(1/200),h2=log(1/40),h3=log(5/12),
h4=log(253/600),zeta2=pi^2/6. Overall Lambda2 carries g^2, as established
in VQP1; no model g or Q value is selected. The finite polynomial here is
still a BARE coefficient with unsubtracted UV subdivergences and overall UV
poles. A parent-compatible UV forest/CT assembly is required before a finite
renormalized hard contribution can be integrated with EAT1. No finite mass,
tadpole, local background CT or nonlinear C1 conversion is supplied here.

The relevant established comparator is the general1LPI/common-region discussion
in Fuentes-Martin etal2412.12270v2, sections4.1-4.2 and appendixD. Our proof
is this actual quartic action's restricted tree map and Gaussian identity,
not adoption of its unproved-for-this-model global gauge-matching premises.
