# Connected source sewing: algebra and remaining analytic bridge

## The formal one-loop identity

For W=j phi-Gamma, Gamma=S+hbar Gamma1, and the formal tree stationary
map S_phi(phi0,J)=j, differentiation at fixed j gives

    y_i=-H^{-1} S_phi_i,
    y_ij=-H^{-1}(S_phi_ij+S_phi_phi_i y_j+S_phi_phi_j y_i
                         +S_phi_phi_phi[y_i,y_j]).

The order-hbar change of phi cancels by tree stationarity in the Legendre
transform, leaving W1=-Gamma1(phi0,J). Consequently

    W1_ij=-Gamma1_ij-Gamma1_i_phi[y_j]-Gamma1_j_phi[y_i]
                        -Gamma1_phi_phi[y_i,y_j]-Gamma1_phi[y_ij].

These formulas use complete even directions over the graded coefficient
algebra. They do not assert existence of a global inverse on Schwartz
functions or a pullback of singular distributions. The component source
derivatives in the stored endpoint table are LEFT Euler derivatives;
conversion to complete directions retains their Grassmann coefficients.

The nonlinear finite tests compare three constructions: implicit tree
stationarity followed by the determinant/Schur complement, the full chain,
and direct Wick expansion of log Z from the original action. Ordinary
cubic boson vertices are retained through degree two, sufficient for the
one-loop coefficient with these three external direction amplitudes:
one-loop connected graphs have as many cubic as linear vertices, and at
most two linear vertices can use the selected source labels. Cubic degree
is bookkeeping in a diagnostic coupling, not nilpotence of the boson.
The explicit exponential/log truncation also checks that no further term
exists in that selected algebra. For the odd example the exterior algebra
is theta1,theta2,f0,f1; E[f0 f1]=-hbar/m. This sign follows from the original
quadratic action exp(-m f0 f1/hbar), not from a shared Hessian mapper.

The bosonic example includes a uab*c*z term. Its field Hessian vanishes,
but S_phi_ab=u*c and the tadpole contribution gc/(2k^2) survives. Every
one of the five chain omissions is detected in all four fixtures. The
odd example likewise has a nonzero source-pair mean response. Its zero
proper source Hessian is a fixture property, not a model-wide omission.

## Actual source support, including zeros

Use the authenticated original NMP/ghost source chart and full-jet QG,
not the finite diagnostic actions. Left source Euler columns are obtained
before sources are set to zero. The replay removes each raw graded port
and integrates its jet derivatives by parts before restriction. All 90
Ja/JLambda columns and all ordered source-pair columns are retained with
explicit zero complements. Intrinsic degrees zero/one and both probes
are included, with no source momentum or field jet dropped.

The base source action has 45 affine Ja-to-Lambda endpoints. The unbroken
probe has 48 derivative-vector and 12 auxiliary endpoints. The broken
probe has 132 derivative-vector, 33 auxiliary and 296 intrinsic scalar
endpoints. JLambda has no affine field endpoint at zero ordinary mean.
Full first source columns remain nontrivial away from zero mean.

The second source Euler columns have 12 and 257 nonzero ordered columns
for the two probes. Their source-only contacts have 12 and 33 entries.
All affine second-source field columns vanish: S_phi_JJ at zero ordinary
mean is zero in this declared classical module. This does NOT set S_JJ
to zero, and does NOT set y_ij to zero: the other three terms in its
stationary equation remain, as does the one-loop tadpole contraction.

With the inherited positive-scalar-reference dressed Green bounds,
BB<=2, BL/LB<=1, Bx/xB<=1, xx<=0, Ca/aC<=2, absent entries absent,
the affine Ja endpoint has soft degree at most one. The derivative on
the B endpoint lowers its degree by one; the auxiliary endpoint uses a
mixed edge; the intrinsic scalar endpoint uses a massive scalar edge or
the Bx mixed edge. This is a necessary endpoint bound, not a bound for
every joint sewn graph or for independent repeated Slavnov insertions.

## Conditional canonical tadpole reduction

On the even-source plane define K_r=Euler_JLambda_r G. The actual GF
Lambda Euler equation has F_D=i*identity multiplying div B. Extract
the BB term F_BB and K's divergence and BB terms. The code tests the
projection of K_D F_D^{-1}F_BB-K_BB on a separately computed nullspace.
All projected polynomials vanish in both probes.

That nullspace is the annihilator of the H-ghost coefficients in qLambda,
not an authenticated complete background-covariance module. The exact
qualification in COVARIANCE_CLARIFICATION applies. The test supplies a
possible way to annihilate an auxiliary tadpole without choosing its
value, conditional on a separately derived membership statement. Neither
the actual tadpole nor full nonlinear mean response is constructed here.

## Why the existing proper trace theorem is insufficient

A Schwartz source direction acted on by a massless inverse generally
has a power-law tail. Thus the proper functional on Schwartz mean fields
cannot simply be composed with that map using its old domain theorem.
In sewn graphs, tree momenta become differences of loop momenta. Joint
arrangements such as q,p,q+p must be controlled as arrangements, not as
independent old loop nodes. The endpoint bound above helps, but the
complete nonlinear branching/zero-transfer proof is still required.

Most acutely, a translation-invariant tadpole is a delta at zero total
momentum. Independent free-edge smoothing is not an innocuous replacement
on that distribution. Let delta_sigma be the normalized four-dimensional
Gaussian, chi_epsilon=1-exp(-p^2/epsilon^2), and m^2>0. With r=sigma/epsilon
fixed as both tend to zero,

    integral delta_sigma(p) chi_epsilon(p)^2/(p^2+m^2) dp
      -> (1/m^2)[1-2/(1+r^2)^2+1/(1+2r^2)^2].

This follows by integrating three normalized Gaussian terms after p=sigma z;
dominated convergence applies because the remaining denominator is bounded
by 1/m^2. The limiting values are 0,11/(18m^2),1/m^2 as r tends to 0,1,
infinity. The coefficient multiplying such a distribution in the actual
model has not been shown nonzero here. This is a sensitive diagnostic of
an unjustified inference, not a model obstruction or anomaly result.

There is a second distinct issue. At a fixed UV cutoff the connected
Legendre map uses the classical regulated Hessian H+R_t; a renormalized
proper Legendre map uses H. If F_t=a/t+b and T_t=T0+t*T1, then

    FP(T_t F_t)=T0*b+T1*a,
    lim T_t(F_t-a/t)=T0*b.

Transporting only T0*a/t instead of the complete proper subtraction leaves
T1*a. This elementary control shows why external heat factors and power
subtractions must be tracked together. It does not measure such a term
in this model. An arbitrary finite A0/A2 or tadpole choice cannot supply
the missing actual regulated bridge.

## Disposition

The formal identity, nonlinear finite checks and complete classical source
endpoint data are established by this bounded increment after review. A
full connected continuum construction remains NOT_ESTABLISHED. The next
least expensive test is an action-derived tadpole projection/membership
and regulated tree-sewing subtraction analysis, before any new loop table.
All chi4,kappa,b0 and IR normalization freedoms remain distinct and unfixed.
