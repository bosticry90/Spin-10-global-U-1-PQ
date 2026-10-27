# SBJ1: a controlled selected quadratic finite-part family

## Result and scope

The actual scalar bubble admits an explicit joint heat/epsilon finite-part
comparison with a uniform remainder bound and an arbitrary common additive
normalization. Together with the qualified JHP Ward and CTJ transverse
results, this constructs a controlled comparison for the complete selected
parity-even gauge two-point tensor, retaining its nonlocal log q.

This is one constructed mathematical family, not adoption of a physical
scheme. Existing sequential endpoint contracts do not uniquely prescribe a
joint extension. A local analytic countermodel demonstrates that logical
limitation without establishing its admissibility in the full quantum theory.
The nonzero Ward contact and unprobed hatted defect remain; no full chiral
source/product, measure, QAP or E5/A5 result is claimed.

## Inputs, exact subtraction and the nonlocal limit

Base15cbd4ae408566f21baa2b813c53cf298ab838df, main, October25,2026. Use the
original unshifted SMA, its actual CSW free P/S heat derivation, and the same
mass-independent parity-even gauge two-point projection at A0,p_hat0,q=p_E²>0.
The bound holds for 0<=epsilon<=1/4 and positive compact q/mu_R² sets. The
45-generator family Gram, physical trace, Gaussian normalization and earlier
power/finite comparisons are reused qualified premises, not new model replays.

With c=2t, N=exp(gamma_E epsilon)(mu_R²)^epsilon, u=x(1-x), m=min(x,1-x),

    I=N integral_0^1 (qu)^(-epsilon)
                       Gamma(epsilon,cq*max(x,1-x)) dx,
    I_D=N q^(-epsilon) Gamma(epsilon) Beta(1-epsilon,1-epsilon).

The moving lower face has L(epsilon)=integral m^(-epsilon)dx=2^epsilon/(1-epsilon).
Integrating the lower incomplete gamma before limits gives

    I=I_D-N c^epsilon L(epsilon)/epsilon+R_I,
    0<=R_I<=N q c^(1+epsilon)L(epsilon)/(1+epsilon).

The local, q-independent subtraction is

    S=[1-N c^epsilon L(epsilon)]/epsilon,
    S(0,c)=-gamma_E-log(2c mu_R²)-1.

Define the comparison family I_R=I-S+beta_fin, retaining beta_fin symbolically.
Its common joint limit is log(mu_R²/q)+2+beta_fin, with no condition on
epsilon log c. The bound follows from 0<=1-exp(-v)<=v and max(x,1-x)<=1;
it is not fitted from a desired tensor or Ward result. Numeric tables use
the zero-additive reference solely to compare algorithms. This is not a
physical choice beta_fin=0 or an identification with chi4,zeta,kappa,b0.

An additional boundary-flow derivation gives

    dI/dc=-N c^(epsilon-1) integral m^(-epsilon)exp[-cq max(x,1-x)]dx,
    dS/dc=-N c^(epsilon-1)L(epsilon).

Their difference is positive and integration supplies the same uniform bound.
At epsilon0,c=2t it recovers the actual qualified auxiliary-bubble derivative
-(exp(-tq)-exp(-2tq))/(t²q), including its sign and factor2.

## Full selected tensor and normalization comparison

Let T=q delta-pp. The earlier actual tensor is K_R=2B T+W_R delta. CTJ defines
F=2B-I/3 and derives the local boundary transport A=N c^epsilon j(epsilon).
JHP proves W_R=D_e+R_W; CTJ proves F+A=F_D+R_F. Consequently

    K_R^beta=[(I-S+beta_fin)/3+F+A]T+W_R delta

has a uniform comparison to [(I_D-1/epsilon+beta_fin)/3+F_D]T+D_e delta.
If B_I,B_F,B_W are the three qualified error bounds, its operator-norm error
is at most q(B_I/3+B_F)+B_W, since the Euclidean norm of T is q. Its joint
limit per color trace in the inherited action units is

    [log(mu_R²/q)/3+5/9+beta_fin/3]T + q delta/6.

The nonlocal logarithm is retained, and the Ward contact is nonzero. The
physical three-family Gram6I45 and action/polarization factor remain inherited.
This is a selected quadratic comparison; it says nothing about arbitrary
chiral backgrounds or coincident multi-source products.

The old scalar heat finite part is
log(mu_H²/q)-gamma_E+1-log4+n_log. Our N equals the conventional dimensional
prefactor (4pi mu_D²)^epsilon under the auxiliary reparametrization
mu_R²=4pi exp(-gamma_E)mu_D². Taking the same auxiliary scale symbol
mu_D²=mu_H² reproduces the old relative constant

    I_D,FP-I_H,FP=1+log16pi-n_log=chi4.

A common beta_fin added to both cancels. This is a convention comparison,
not selection of a physical scale or a new finite baseline. chi4,zeta,kappa
and b0 remain distinct and unselected.

## What the endpoint information does not determine

Set tau=-epsilon log(c mu_R²), psi=tau exp(-tau). This coefficient is local
in external fields (no q dependence), analytic in epsilon at fixed c>0, and
vanishes in both iterated regulator limits. Along cq=exp(-a/epsilon), however,
psi tends to a exp(-a). Thus adding lambda*psi preserves both endpoint
prescriptions while changing mixed-path limits in this larger analytic
comparison class. The endpoints alone cannot select a unique joint rule.

This is not proof that lambda*psi is an admissible counterterm under every
actual symmetry/contact requirement. Our explicit common-limit condition
excludes it. The present construction earns existence of one controlled
selected comparison family, not physical adoption or uniqueness.

## Validation, controls and execution

Primary directly integrates the upper-gamma kernel. Replay uses independently
integrated polynomial half-interval moments in the lower-gamma expansion.
Terms n1..63 are retained, with explicit omitted-tail bound
|N c^epsilon|(cq)^64 L(epsilon)/[64!(epsilon+64)]. Its maximum is
3.13894339935618e-80, below1e-48. The exact uniform remainder bound, not the
numerical sample alone, proves the joint statement.

Nine finite cases and nine correlated paths were evaluated at100digits and
stored at75. All144 scalar comparisons pass the1e-40 scaled gate. Their
largest scaled stored discrepancy,1.22e-99, is a numerical diagnostic, not
a claim of99-digit accuracy. Only after scalar agreement were JHP/CTJ tables
read to test all288 entries (18cases x16components) at the prescribed nonzero
momentum orientation. These are assemblies with inherited tensor data, not
288 newly integrated quantum amplitudes.

The gate and separate heat-flow review record the following omissions:

- Removing or reversing complete S changes all18cases; using only its
  epsilon0 logarithm changes15, with the expected three epsilon0 insensitive.
- The explicit lower-face term is nonzero in all15 positive-epsilon cases;
  its separately singular epsilon0 value is not evaluated as a finite number.
- Replacing the lower-face moment by a fixed-face value changes all18cases;
  the removable epsilon0 difference is log2+1.
- Omitting CTJ's A or erasing JHP's nonzero Ward coefficient changes all18cases.
- The symbolic nonlocal slope and beta_fin local direction are retained;
  no beta_fin value or desired cancellation is used to determine a quantum input.

Sources and inputs were frozen before computation. P/R/verifier/flow review
completed38.2580565/1.8189303/.8043874/.4275632seconds after imports. Caps180s
each,8GiB sampled-private,350MiB launch floor,8MiB packet respected; no cap
expanded. Resource samples20/2/1/1 and sampled private maxima
52,293,632/51,871,744/393,216/487,424bytes are not continuous memory peaks.
Nine source copies; preparation/validation/review bindings43/51/60;
pre-reportpacket107987B. No SBJ worker, preparer or verifier failure occurred.
JHP's earlier failures remain unchanged and FAILED.

Receipt validation_receipt.json SHA256
4148c1e6d1759bcecd9beabee9ead7135d8502bb75ed0b50cac564cd41ab961f.
Review receipt SHA256
af7f8d48d2cbdcd8e5ef4e4de37cba5b8bb4cbb118e9feabeb77cdc7d338250f.
Full captures, source copies and packed/raw table hashes accompany them.
Fresh E4 completed native0, steps[0,0,0,0,0,2]; custody remains exit2 with
seven NOTPASS references. This is authentication, not fresh scientific
replay or director acceptance. External before/index/after seals under
C:/Users/psboy/.codex/research-control-records/ToE-Next/chiral-scalar-bubble-joint-fp-v1-2026-10-25/
protect all35578priorGitblobs and new raw/index/HEAD bytes.

[DLMF8.7.3](https://dlmf.nist.gov/8.7.E3) and
[Euler's beta integral](https://dlmf.nist.gov/5.12.E1) supply established
mathematical identities. The [BMHV analysis](https://arxiv.org/abs/2004.14398v2)
is a methodological comparator for retaining evanescent terms, not validation
of this model. Distinct integration/flow routes share action/reference data,
old JHP/CTJ results, Python/SymPy/mpmath and AI author. Agreement is internal
mathematical corroboration, not external scientific or experimental confirmation.

## Next scientific dependency and authority ceiling

The next useful calculation is an actual finite chiral probe-connected
amplitude, using the full source-Hessian and heat placement before any
restriction. A low-cost first target is the constant-u physical two-fermion
response at nonexceptional p, with its actual action-derived probe insertion
and both bosonic heat edges. Derive its support, mixed auxiliary contributions,
sign and normalization before integration. A repeated boson edge has three
heat factors overall; it cannot be replaced by a derivative of the ordinary
two-edge answer without transporting the regulator variation. Retain hatted
terms at nonzero epsilon and the independent finite normalization.

A constant-probe result will not qualify varying probes, two independent
transfers, KP descendants or all connected products. Use it to test the
actual finite primitive needed for that extension, not to claim full QAP.
Unprobed Ihat remains nonzero and Q_full curved. General backgrounds,
source/product trace domain, measure/phase, causal/physical-vacuum limits,
massive C1 and E5/A5 remain open. State113/34of39 unchanged, state SHA
d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8.
No action, foundation, scheme, benchmark or protected status changed;
flavor/HB1/C5 remain paused/blocked. Whole goal ACTIVE and INCOMPLETE.
