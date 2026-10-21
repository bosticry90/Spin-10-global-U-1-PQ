# Classical scaling does not scale the fixed-gauge loop slopes

## 1. Define the family without retuning a background

Treat all34 real coefficient coordinates of the qualified scalar potential
as independent once their finite-point values have been evaluated. Multiply
each by the SAME positive epsilon, including dimensionful masses/cubics and
both real components of complex coefficients. Hold fields/VEVs/kinetics fixed.
This is allowed parameter exploration, not adoption or a finite renormalization.

The potential is linear in these coordinates, so V_e=epsilon V_0 identically
for all fields. All field derivatives scale the same way. Stationarity and
all mass signs/zero ranks therefore persist for epsilon>0. The weak light
root is scaled with the whole mass matrix; it is not solved again while a
derivative is taken. The full328 quartic lower bound becomes epsilon*c_0>0.
The complete contact operator is epsilon times its former operator. A heavy-
relaxed quartic has the form q-b^T H^-1 b; it scales as epsilon, including
the cubic relaxation term. These transfer statements preserve the declared
classical properties; they do not certify a physical or quantum benchmark.

All kinetic metrics, eigenvectors and projector ranges are unchanged. Squared
scalar masses and their fixed-parameter radial derivatives scale as epsilon.
The vector masses g²gamma do not scale: g and the vacuum are fixed.

## 2. Keep the explicit scalar logarithm at the same Q

For raw radial index i, define the already qualified T_i and B_i at epsilon1:

 T_i=sum_b d_b Tr[M_b(log(M_b/60)-1)D_bi]/(32pi²),
 B_i=sum_b d_b Tr[M_b D_bi]/(32pi²).

The recorded M eigenvalues are SQUARED masses. The finite first-derivative
zero-mode limit is inherited; it is not a zero-momentum propagator prescription.
At fixed Q²=60,

 T_i^scalar(e)=e²(T_i+log(e)B_i),
 H_raw(e)=e H_raw0,
 r_i^scalar(e)=e[r_i0-b_i log(e)],
 r_i0=-T_i/H_ii, b_i=B_i/H_ii.

The actual radial H is positive diagonal. The current Sigma r0 and b are
positive, so this scalar response stays positive throughout0<e<=1. Dropping
log(e) would instead describe a changed reference choice without its proper
companions. This family is not running the couplings or holding generated
portals zero along an RG trajectory; their zeros are reference-scale inputs.

## 3. Reevaluate the orbit derivative too

Use exact gamma=(3/5,3,50,253/5), multiplicities(8,1,12,12), unbroken rank12.
Let t_P=Tr(P_gamma GP), t_S=Tr(P_gamma GS). The radial derivatives of Gamma
are2t_P,2t_S,0. The inherited gauge/orbit Gaussian gives

 O_gamma,i(e)=e*H_ii/(G_i*gamma)*t_i,

where G=(60,3/5,3/5), t_i=t_P,t_S,0. The longitudinal/ghost cancellation
retains this orbit remainder; it does not set it zero. For fixed u=xi*g²,

 V_i(g)=3g^4 sum_gamma gamma*(2t_i)
            [1/3-log(g²gamma/60)]/(32pi² H_ii),
 O_i(u)=u sum_gamma t_i[1-log(u gamma/60)]/(32pi² G_i),

 r_i^known_boson(e;g,u)=e[r_i0-b_i log(e)]+V_i(g)/e+O_i(u).

Both S gauge terms are zero by the inherited actual mixing/derivative check.
For Phi/Sigma the vector/orbit terms are positive in the stated domain,
since gamma/60<=253/300<1. The vector tadpole is independent of e; the orbit
tadpole scales as e, so its response is CONSTANT, not1/e. The1/3 vector
constant follows from differentiating the5/6 potential constant and remains.

The reference formulas are inherited and project-specific. Martin's
[effective-potential equations3.2-3.4](https://arxiv.org/pdf/hep-ph/0111209)
provide the scalar/vector normalization comparator; his Landau-gauge setup
is not adopted to replace the actual xi-dependent Gaussian construction.

## 4. A continuous necessary condition, not an optimized point

For Sigma write S=r_Sigma0>0, b=b_Sigma>0 and V=V_Sigma(g)>0. On0<e<=1,

 r_Sigma^known_boson>=S*e+V/e+O_Sigma(u)
                    >=2sqrt(S V)+O_Sigma(u).

It also exceeds V(g), because V/e>=V and the other terms are positive.
These are conditional bosonic OFF-SHELL displacement inequalities. They do
not bound an observable or a complete quantum correction. Unknown fermion
terms and different compatible input definitions remain uncalculated.

Every nonzero vector summand is monotone increasing for0<g<=1:

 d{g^4[1/3-log(c*g²)]}/dg=g³[-2/3-4log(c*g²)]>0,

because c<=253/300<exp(-1/6). The last strict inequality follows, for example,
from the alternating four-term lower bound1-1/6+1/72-1/1296 for exp(-1/6).
V(0+)=0 and V(1)>1. Thus define two UNIQUE diagnostic boundaries:

 g_V: V(g_V)=1,
 g_AM: 4*S*V(g_AM)=1.

For g>=g_V the vector response alone prevents a subunit Sigma response for
any uniform weakening. For g>=g_AM the sharper AM lower bound does so.
These are necessary conditions only; g below either is not a passing point.
The vector root can be enclosed using exact rational log/pi bounds. The AM
root inherits S's numerical validation and is not a new rigorous source interval.
Neither is a measured gauge coupling or a physical perturbativity cutoff.

At the inherited g=1/2 example, even discarding the positive logarithms in V
gives an exact vector-only bound above1 using pi²<10 and the rational weights.
The whole-domain inequality therefore cannot be an artifact of a selected
epsilon grid or a cancellation fit. At fixed nonzero g, V/e diverges as e->0.

There is a stronger diagnostic check when2S>3b and V>=S-b. Indeed
e²(S-b-b log(e)) increases on(0,1] and is bounded above byS-b. Hence
partial_e r_Sigma=S-b-b log(e)-V/e²<=0. In that case every weakening below
epsilon1 increases the known bosonic response. Test these inequalities at
the inherited g=1/2 example; do not infer them solely from a grid.

## 5. Keep the complete singlet pole separate

At the inherited point a=mS,tree²=6/5. Along this family a(e)=e*a, D=e*D0,
E=e*E0. The old field-content/isolation proof is preserved structurally: S
is gauge trivial, zero portals stay zero as reference inputs, the potential
and its derivatives scale uniformly, and orbit/S cross columns remain zero.
Thus the complete one-loop singlet component remains scalar in this scope.

Let delta_0 be its complete original pole correction and L its coefficient
of log(e). From the bubbles, seagulls and required vacuum-source insertion,

 delta(e)=e²[delta_0+L log(e)],
 L=sum_b d_b[sum_i E_ii*m_i²+sum_ij |D_ij|²]/(32pi²)
       -(18/5)*b_S.

The independent RG result requires L=-(1/2)*partial_logQ delta_0. Its
imaginary part has no explicit scale logarithm. The relative correction
therefore tends to zero as e|log e|, while the fixed-gauge Sigma response
grows as1/e. This is the scalar/gauge tradeoff the test measures. No full
higher-loop accuracy follows; SSI1's internal Yukawa carrier remains.

Only if Q² were ALSO changed to e*60 with the relevant parameter interpretation
would the displayed scalar log(e) cancel. That is not this fixed-Q family and
is not performed to obtain favorable numbers. Rescaling g/Y as well or adding
fermion cancellations would define another investigation, not a result here.

## 6. Interpretation and limits

The proof applies to the prescribed analytic family and conditional bosonic
reference. It does not refute the model, justify a new scheme, adopt a scalar
point, qualify physical masses or remove old failures. Classically feasible
and small in one loop component are distinct requirements. A new viable
benchmark would still need complete quantum-input, gauge/Higgs matching and
matter/physical-domain qualifications. State authority remains unchanged.

Numeric tables reuse qualified spectral inputs; tiny recorded mass residuals
are assigned to EXACT zero modes only via their inherited zero_copies/rank
certificate and its old thresholds. No new small-entry truncation is introduced.
Agreement of methods is bounded corroboration with shared action/data/software/
AI authorship. There is no external expert, experiment or Lean certificate.
