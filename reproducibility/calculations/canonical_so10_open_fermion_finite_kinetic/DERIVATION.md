# OFK1 frozen integral and representation specification

Use physical gamma4=(sigma2 tensor sigma1,2,3; sigma1 tensor I2), with
chi4=product gamma4 and PL=(1+chi4)/2. In a6D witness set
Gamma_bar=gamma4 tensor sigma3, Gamma_hat=I4 tensor sigma1,2,
chiBar=product four barred Gamma, chiAC=i product all six Gamma.
Z=chiAC chiBar is an involution commuting with barGamma and both chi.
Pext=(1+Z)/2 must have rank4. Derive an isometry U with Udagger U=I4,
Udagger Gamma_bar U=gamma4, Udagger chiAC U=chi4. HatGamma maps Pext to
its complement. A single projected hat vanishes; contracted pairs do not.
No orientation average or odd-chi trace removal is used on the open chain.

Reference gauge charge A=PL T+PR R,R=-T^T, and At=PR T+PL R.
For all Lorentz directions Gamma A=At Gamma. Reference mass vertex is
PL M+PR Mdagger, with qM=ig(cR M-McL), cR=-cL^T. Physical projection must
recover both SMA1 current and mass. Formal chiral identities are checked
before applying the4D external volume relation. This does not define an
analytic closed odd-chi trace or a complete anomaly prescription.

Strip common1/(16pi^2). Let k be gauge momentum,r=p-k. Actual Feynman
numerator is sum_bar Gamma_mu barslash(r) Gamma_mu. Reference replaces
both summed vector indices and fermion slash by full ones. Longitudinal
numerators are barslash(k)barslash(r)barslash(k) and the full analog.
Use the actual open-line phase -V S V: gauge(-ig)^2 and S=-i slash/k^2
give phase -i; scalar vertices have phase+i. Preserve chiral color order.

Primary parameterization: denominator k^4 r^2 gives weight2x and
k=l+(1-x)p,r=xp-l,D=x(1-x)p^2. Compute linear-in-p tensor numerator and
the remaining p^3 term. Gaussian second moment is delta_ij/d times l^2;
integral l^2/(l^2+D)^3=(d/4)Gamma(eps)D^-eps and
integral1/(l^2+D)^3=Gamma(1+eps)D^(-1-eps)/2.
Feynman denominator k^2 r^2 has first moment r=p/2 by exchange symmetry.
The MSbar-normalized off-shell scalar bubble is
J=exp[(gamma_E+L)eps] Gamma(eps) B(1-eps,1-eps), L=log(mu^2/p_E^2).
Keep all finite terms; both endpoints are integrable near epsilon0.

Replay uses full-Clifford identities before integration. With hats(p)=0,
project the full and barred unshifted numerators. Terms odd in an individual
hat momentum may vanish after projection/integration, but contracted pairs
must remain. Derive evanescent differences and integrate them by independent
Schwinger parameter moments. Derive the reference longitudinal result using
2k.r=p^2-k^2-r^2 and the vector bubble, rather than primary's shifted tensor
numerator. Any scaleless odd integral used is a justified symmetric momentum
integral in this dimensional family, never a heat-regulator boundary claim.

Yukawa open line: project (PL m+PR mdagger) fullslash(r)
(PL m+PR mdagger); compare to the barred SMA1 numerator without using
closed chiral traces. Sum all328 actual real scalar directions before
asserting the two carrier products or cross zeros. Preserve Ydagger Y
and YYdagger as3x3 matrices, not family traces. The complete mass-dependent
propagator remains SMP1's original one; this mass-independent computation
does not replace it by a conventional massive denominator.

Report actual and reference UV/finite jets separately, their difference,
complete model tensors, known UV comparison and every control. A local
relative kinetic density is not an independently measured Ward/Slavnov
breaking insertion and does not fix an invariant finite normalization.
