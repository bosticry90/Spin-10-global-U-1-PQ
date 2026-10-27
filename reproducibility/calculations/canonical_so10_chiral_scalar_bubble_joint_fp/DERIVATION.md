# Prospective scalar joint finite part and selected tensor assembly

All statements use RECORD's nonexceptional compact domain and inherited actual
JHP/CTJ action, heat and normalization premises. Put u=x(1-x),m=min(x,1-x),
N=exp(gammaE e)muR2^e. The scalar bubble and its dimensional continuation are

 I(e,c)=N integral (qu)^-e Gamma(e,cq*max(x,1-x))dx,
 ID(e)=N q^-e Gamma(e)Beta(1-e,1-e).

The actual lower face has moment L(e)=integral m^-e dx=2^e/(1-e). Integrate
the lower gamma before taking e0:

 I=ID-N c^e L(e)/e+RI,
 0<=RI<=N q c^(1+e) L(e)/(1+e).

This follows from 0<=1-exp(-v)<=v and max<=1, not a fit. The LOCAL subtraction

 S(e,c)=[1-N c^e L(e)]/e

has a removable e0 at fixed c, S(0,c)=-gammaE-log(2c muR2)-1. Define the
comparison family I_R^beta=I-S+beta_fin. ID_R=ID-1/e has continuous e0
log(muR2/q)+2. Consequently I_R^beta has uniform joint limit
log(muR2/q)+2+beta_fin. Uniformity has no restriction on e logc.
Beta_fin remains an unspecified common additive local normalization. The
nonlocal logq is retained. This is one exploratory extension, not adoption
of an absolute physical subtraction or proof that old contracts mandate it.

At e0 the raw heat bubble is -gammaE+1-log2-log(cq)+O(cq), with c=2t.
Subtracting log(1/(t muH2)) and adding n_log gives
IH_FP=log(muH2/q)-gammaE+1-log4+n_log. The conventional DIM prefactor
(4pi muD2)^e equals N when muR2=4pi exp(-gammaE)muD2. Setting the SAME
auxiliary scale symbol muD2=muH2 is the old comparison, not a new physical
scale selection. Then ID_FP-IH_FP=1+log16pi-n_log=chi4. A common beta_fin
added to both sides cancels. No identification with kappa/b0/zeta is inferred.

CTJ has F=2B-I/3, A=Nc^e*j(e), j=2^e(e-5)/[6(1-e)(2-e)(3-e)],
F+A=FD+RF, |RF|<=Nq c^(1+e)2^e/[3(1-e)(1+e)]. JHP has WR=De+RW
with its qualified bound BW. Thus the complete SELECTED renormalized tensor

 KR^beta=[(I-S+beta_fin)/3+F+A]*(qdelta-pp)+WR*delta

differs from the dimensional finite-part tensor
[(ID_R+beta_fin)/3+FD]*(qdelta-pp)+De*delta by operator norm at most
q*(BI/3+BF)+BW. Beta_fin cancels from this comparison. The joint limit is

 [(log(muR2/q)+2+beta_fin)/3-1/9]*(qdelta-pp)+qdelta/6.

Physical familyGram6I45 and action/polarization factor are inherited, not
remeasured. The limit's Ward contact is NONZERO; Ihat/Q_full are not made
nilpotent by this tensor comparison. No arbitrary background/source product,
distributional q0 pullback, full scalar interaction or massive physical limit.

Replay: lower-gamma compact moments Ln=2 integral_0^(1/2) x^-e(1-x)^n dx,
evaluated by finite polynomial coefficients. The remainder RI equals
-Nc^e sum_(n>=1) (-cq)^n Ln/[n!(e+n)]. Keeping n1..63 has tail bound
|Nc^e|*(cq)^64*L(e)/[64!(e+64)]. Retain every omitted tail explicitly.

Endpoint countermodel: tau=-e log(c muR2), psi=tau exp(-tau). It is local
(no q dependence) and analytic in e at fixed c>0. Both iterated limits
vanish; along cq=exp(-a/e),psi->a exp(-a). Adding lambda*psi changes joint
limits without changing the two endpoint prescriptions. This shows those
endpoint data alone do not select a unique joint rule in this larger class.
It does NOT establish this addition's admissibility in the actual full
renormalized contact module. Our uniform rule excludes it by its explicitly
imposed common-limit requirement. Existing sequential endpoint results survive.

[DLMF gamma series](https://dlmf.nist.gov/8.7.E3) and
[Euler beta integral](https://dlmf.nist.gov/5.12.E1) are reference identities.
[BMHV chiral counterterms](https://arxiv.org/abs/2004.14398v2) are a methodological
comparator, not proof of this model or of its missing chiral source domain.
