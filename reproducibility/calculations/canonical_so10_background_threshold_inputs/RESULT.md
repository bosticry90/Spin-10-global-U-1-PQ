# BFT1 result — C1 background-field input and topology construction

**PASS within the frozen kinematic-input and skeleton scope.** The finite
C1_GS remains uncalculated. This does not pass the original finite-amplitude,
master-basis, complete eigenstate-lift or counterterm gates. All old evidence
and scientific authority remain unchanged.

The original C1 contract fixes MSbar background-field Feynman gauge. BFT1
derives its linear Rxi Faddeev–Popov input from the frozen physical parent
kinetics, using the existing orthonormal representations and VEV as data.
It does not activate the inactive physical-reconciliation action or repair
the failed historical A10 gauge/source architecture. Its conventional
Gaussian auxiliary is not the E1 nonlinear auxiliary, and E1 quartic ghosts
and source-loop theorems are not imported as vertices for this calculation.

## Exact coefficient result

The ordered ghost-scalar density is xi*g10^2*barc_a T_abI eta_I c_b,
T_abI=(rho_a v)^T rho_b e_I. The two native routes and independent full
coefficient verifier agree on all45*45*328=664,200 positions:

| Scalar carrier | Nonzero T coefficients |
| --- | ---: |
| Phi54 | 524 |
| Sigma252 | 10,000 |
| phi20 and S2 | 0 |
| Total | 10,524 |

The653,676 remaining positions are zero by complete contraction, not absence
of a stored entry alone. The deterministic exact tables have decompressed
SHA256 `b020f223920bd6c4b8826f20dacef412e82e22428b61b925727573e944e34c3b`.
They also contain all45^3 Lie-constant positions (720 nonzero), the424-entry
orbit, Gram and every labelled background insertion word. Both compressed
tables reproduce identical bytes after decompression. No expected tensor was
read before its native derivation.

Primary used ordered ten-plane commutators and O^T rho_b. Replay used the
faithful phi20 trace and the polarized Gram derivative plus f_ab^c O_c.
The latter term is essential: T_abI-T_baI has6,784 nonzero positions. A
symmetrized ghost/antighost tensor is wrong, although contraction with v still
passes. This insensitive control is explicitly retained, alongside a full
antisymmetric test. The independent verifier reconstructs the complete
tensor directly from the separate replay input, including the zero complement.

All12 H-invariant-VEV and orbit-intertwining matrices pass. Together with the
authenticated representation algebra these prove the claimed kinematic
background covariance; no expanded quantum Ward identity was calculated.
Exact spectral projectors reproduce the Gram eigenvalues/multiplicities
0:12,3/10:8,3/2:1,25:12,253/10:12. With omega^2=60 these are the previously
recorded four massive-vector ratios .005,.025,50/120,50.6/120. Scalar-potential
Goldstone identities and the positive-Higgs mass certificate are reused;
the full328 Hessian is not recalculated.

## Two-loop inventory

The valence identity n3+2n4=2 and a complete Wick/species census give nine
bare1PI vacuum skeleton types: VVVV,VVSS,SSSS doublebubbles; VVV,VVS,VSS,SSS
boson sunsets; and vector/scalar ghost sunsets. Differentiating the skeletons
twice with respect to labelled external H backgrounds retains propagator
seagulls, both matrix orders and all vertex derivatives:

| Skeletons | Labelled insertion words per skeleton |
| --- | ---: |
| VVVV,VVSS,SSSS | 8 |
| VVV,VSS,ghostV | 29 |
| VVS,SSS,ghostS | 15 |

Total156 symbolic placements, before graph automorphisms or actual zeros.
These are not156 measured amplitudes. Ordinary external derivatives/momenta
must survive to the transverse p^2 projection. No constant-background
effective-potential calculation is substituted for gauge-kinetic matching.

The counterterm contribution is the general one-loop trace with deltaK plus
the local two-loop pure-background term. Its trace has six generic labelled
derivative words. One-loop cubic/quartic counterterms inside a two-loop
skeleton would be order hbar^3. Linear/tadpole effects are handled by the
Legendre transform and vacuum normalization, not silently dropped. Internal
light modes and all mixed light/heavy paths remain available; UV/EFT hard
subtraction, not manual diagram deletion, must determine their eventual role.

The extra V2 Gaussian control independently yields

    Gamma2 = k G^2/8-lambda^2 G^3/12+u^2 G/(2a^2).

It derives the sunset sign and1PI subtraction from the actual Gaussian
moments with a Grassmann determinant and a solved mean-zero Legendre source.
The connected calculation initially retains its tadpole/dumbbell terms.
Omitting the source shift or reversing the ghost contribution fails.
Exact noncommuting2x2 matrices also detect missing inverse-Hessian seagulls,
ordering and vertex derivatives in the full word inventory. Such controls
test universal algebra and combinatorics, not model-specific loop integrals.

## Counterterm dependency clarified

Tree Feynman gauge does not justify equating all one-loop width counterterms.
The frozen two-width diagnostic gives first jets

| Coefficient | dX1 | dX2 |
| --- | ---: | ---: |
| Vector longitudinal | -1 | 0 |
| Scalar GF mass | 0 | 1 |
| Ghost mass | 1/2 | 1/2 |
| Residual vector/scalar mixing | -1/2 | 1/2 |

The full deltaK remains general; two widths are not asserted to exhaust
H-covariant mixing. Its off-diagonal VS component alone has zero trace against
the block-diagonal tree Feynman propagator, which is not permission to omit
its associated diagonal CTs or other Green functions.

The one-loop heat regression recovers -7/8-epsilon/12, vector/scalar log
ratio-21 and finite/log(M^2)=-2/21, hence T_i[1-21log(M/scale)].
This is a convention check, not a two-loop finite coefficient.

The consulted original matching contracts do not supply every finite mass,
VEV and tadpole normalization. Keep these CT slots symbolic. Martens uses
on-shell masses and separately renormalized widths; importing those finite
terms would require a justified scheme correspondence. This is a missing
numerical matching input, not a demonstrated inconsistency. MSbar gauge
couplings alone do not determine all finite mass/VEV conventions.
Parameter CT shifts, renormalized tadpoles and the physical one-loop vacuum
shift are distinct. No one of them is set to a convenient finite value here.

## Validation and limits

Native primary2.717654s; replay3.069535s; full independent coefficient/word
verifier1.704145s; supplemental Gaussian/Legendre verifier4.884157s, after
imports. Zero failed native/verifier executions. V2 supplements a successful
V1, not a failed scientific run; all original bytes/captures are preserved.
45 initial,52 first-verification,63 supplemental bindings. Largest observed
private-memory sample59,027,456 bytes is NOT a true peak.120/180s,8GiB sampled,
350MiB launch and4MiB package limits apply. Complete captures precede checks.

The commands were executed separately in the workspace, in this order:

```powershell
python -B calculations/canonical_so10_background_threshold_inputs/prepare.py
python -B calculations/canonical_so10_background_threshold_inputs/run.py
python -B calculations/canonical_so10_background_threshold_inputs/prepare_validation.py
python -B calculations/canonical_so10_background_threshold_inputs/run_validation.py
python -B calculations/canonical_so10_background_threshold_inputs/prepare_gaussian_v2.py
python -B calculations/canonical_so10_background_threshold_inputs/run_gaussian_v2.py
```

Exclusive outputs prevent accidental overwriting. Original helper controllers
and source copies remain bound. Completed receipts authenticate/validate this
scope, not director acceptance or project-wide scientific authority. Final V2
receipt SHA256: `fd1afe95d714f99d37828660f146bdc1b71c6ae13b014de16d51123766f561e6`.

Shared premises include the physical action, supplied representation/VEV
data, inherited Lie/Goldstone evidence, SymPy, published conventions and the
same AI author. This is internal computational corroboration, not external,
Lean or experimental validation. It demonstrates useful structural reduction
and a sensitive check of ghost ordering; it does not validate shared physics.

The remaining finite C1 obligations include actual eigenstate/vertex weights,
one-loop counterterm coefficients and finite prescriptions, tensor/IBP
reduction, required epsilon/massless UV–IR descendants, and common UV/EFT
subtraction. No gauge-parameter cancellation, target alignment/refit,
perturbative-control or physical-unification claim is earned.

State113,34/39 and sevenfalse unchanged; E5/A5 unqualified, HB1/C5 blocked,
flavor human-paused, C1_GS uncalculated. QuartetFAIL3960/648 and historical
custodyexit2/seven remain.140% local-inclusive singlet,1.94% Euclidean and
20.27% timelike diagnostics, matching residual0.745476 and missing Yukawa
control remain separate limitations. No historical/source functional changed.
