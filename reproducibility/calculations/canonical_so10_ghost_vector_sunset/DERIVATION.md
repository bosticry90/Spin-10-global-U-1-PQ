# GVA1: model assembly and original forest ownership

GVS1 fixes the actual derivative vertex, Wick weight+1/2, mass projectors,
all125 sector triples and all three charge insertions. GVR1 gives the bare
current/divergence identity; its V2 paired mixed-vertex correction is mandatory.
GVC1 derives the original subtractions and proves R_G=R_CCK+z R_SCK+R_T.
GVM1 qualifies the two actual one-light limits without discarding a finite
delta*SCK endpoint. These are prerequisites, not calculations repeated here.

For positive squared masses the exact proper finite U_G functions are those
in GVC1's native tables, with Iabc derivatives of the same finite absolute
sunset master. Their remaining pole vector is p=(-1,-1,-1/3), and scale
vector s=(-5/3,-5/3,1/3-(10/3)(x+y)/z). For each actual profile(r,a,b), put
(x,y,z)=(c_a,c_b,c_r) at g10^2=Q^2=1 in computational reference units. With
J=log(Q^2/g10^2), its finite coefficient is U_G(x,y,z)+J*s. Homogeneity is
checked at a different common squared-mass scale before using this equality.

GVS stores ideal weights in (vector,antighost,ghost) order, while the kernel
axes are (leftghost,rightghost,vector). Thus the unit contraction uses
(W_a,W_b,W_r). Ghost exchange swaps a,b AND the first two weights/kernels.
Vector roles cannot be exchanged with ghosts. Seven canonical heavy keys
cover12 ordered profiles. The full ordered contraction and canonical weight
grouping must agree, including separate finite contributions by profile.

For a one-light vector and equal heavy coefficient c, use GVM's finite
(1/2,1/2,13/18) and slope(-5/3,-5/3,-2/3), with j=J-log c.
For a light left ghost use(5/2,-7/6,-71/18) and(-2,-5/3,-3); exchange the
first two axes if the right ghost is light. Keep the pole vector p in all
cases. The all-light H tree primitive has the same actual density, metric,
heat/IR reference and family-local UV operation as its EFT partner. Their
regulated difference is0; its pole is kept separately as the EFT marginal.

The resulting matched primitive has the form

    Lambda_GV^(2)=g10^2 [F0+S*J+P/eps]
                =g10^2 [C(g10^2)+S*L+P/eps],
    L=log(Q^2/60), C(g10^2)=F0+S*(log60-log(g10^2)).

F0 is a derived finite coefficient, not a physical coupling selected to
improve matching. The pole P is a remaining OVERALL pole, not removed by
this increment. Other primitives, the parent counterterm complement and
finite parameter/reference/tadpole/width jets remain necessary.

## Keep the full original subtraction before hard simplification

Use H_k=exp(gamma eps)Gamma(1+eps)exp(eps*J)c_k^(-eps), c_0=d>0.
For every profile, original cut prefactors before1/eps are

    f_a=-H_a/3, f_b=-H_b/3,
    f_r=H_r[-1-eps/9+(10/3+eps/3)(c_a+c_b)/c_r].

Multiply the actual three charge weights and3/4 BEFORE summing. This gives
Cfull. If one edge is light, Csoft contains that light-edge cut only. If
all three are light, Csoft contains all three original cuts. Tensor-zero
profiles contribute0 by GVS's exact support theorem. This retains light
INTERNAL lines in heavy closures. No product of overlapping cuts is added.

Cfull-Csoft has no H0 coefficient. Its d->0 limit is the hard forest; keep
Cfull itself for subsequent parent-minus-family accounting. A cancellation
from the hard representation does not delete that forest from Cfamily.

    Bfull+Cparent-Sbare-Csoft
      = Rprime_matched+(Cparent-Cfull).

All outputs preserve this identity. The independent forest comparison groups
by closing-sector H_k and sums literal pole operators rather than summing
the primary serialized per-profile forest. Epsilon terms, power-sensitive
terms and the all-light EFT marginal are retained separately.

The group pole check adds the derived hard and all-light EFT marginals and
compares the complete adjoint charge trace. It checks group bookkeeping;
it is not a new independent loop integral or a physical-unification theorem.
No unmeasured parent term is supplied by requiring that check to pass.
