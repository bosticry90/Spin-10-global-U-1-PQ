# VQP1: an actual complete regulated quartic-vector primitive is calculated

The complete VVVV doublebubble now has an explicit model-specific bare F2
coefficient, with all mass assignments retained. Its infrared-sensitive part
has also been connected to an independently opened two-point kernel from the
actual quartic action. This is a genuine primitive two-loop contribution,
unlike HTB1's product of one-loop leaves. It is not yet a renormalized finite
hard matching contribution or full C1_GS.

Final receipt validation_receipt_v3.json SHA256:
`fb2c3f4557b203c4975b020f5bc0b1c583106385c2ddeab0c485b2b330744cd3`.
V2 receipt retained at SHA
`a7495823ebe1d8a96388d7bb51c8c50e005f37c04c200332426e30ee925f8398`.
Scientific acceptance NOT_PERFORMED; project_state113 and34/39 unchanged.

## What was calculated

Use the same source-zero BFT1 action and xi1 Gaussian. The quartic density
g10^2 f_abe f_cde Q_mu^a Q_nu^b Q_mu^c Q_nu^d/4 fixes all three Wick pairings.
Their coincident vector propagators include orbital curvature, vector spin,
the actual mass projectors and D=4-2epsilon. All eight labelled background
placements are retained by the differentiated inverse/heat identity.

The five masses are x_r=60*g10^2*k_r with
k=(d,1/200,1/40,5/12,253/600) and d=delta/(60*g10^2)>0. Delta is an auxiliary
mass only on the previously massless color subspace. Infinitesimal background
derivatives precede its small-delta limit. This is a controlled IR diagnostic,
not a physical mass or a new regulator/renormalization prescription for the
complete theory. It preserves background H covariance; no full Slavnov
invariance of this isolated auxiliary regulator is asserted.

For z=log(Q^2/60)-log(g10^2), the output is the exact symbolic family

    Lambda_VVVV,bare2 = g10^2 [p2/epsilon^2+p1(d,z)/epsilon+f0(d,z)].

Logs of d and all four actual heavy mass ratios remain explicit. No numerical
g10, Q, finite tadpole or parameter condition is selected. This Lambda strips
the two external couplings: Lambda2=-12 Gamma2_Fphys2/(ell^2*g10^2), with
ell=hbar/(16pi^2). Equivalently it is the connection-curvature coefficient.
The physical Gamma2_Fphys2 instead carries g10^4. Nonzero one-loop scalar,
vector-only and ghost checks establish correspondence to FCI1/HTB1's units;
adding an extra external g10^2 to their old coefficients would be incorrect.

The entire result fits in7177 decompressed bytes/2008 gzip bytes. Actual color
tensors X,L,Y contain225 exact entries, plus their zero complements and the
derived Z=L-Y. All25 ordered mass assignments appear. Both native tables have
raw SHA `845898ee988a990b669034aa36f1727ca9edbd07520da4a71e8b22862721c49f`
and gzip SHA `be3f4adec9e9921017771c898f36b4c998aec6343c314f7bf9500db4395541e0`.
The complete polynomials and IR decomposition are in primary_v2_tables.json.gz
and replay_v2_tables.json.gz. p2=-1152 for each remnant gauge factor is an
absolute primitive-graph check, not a complete beta coefficient or anomaly.

The finite coefficient retains the dimensional correction -13 rather than
the premature-D4 value -30 in its C_r A_s term. It also retains the finite
zeta(2) contribution from epsilon terms multiplying poles in B_r B_s. Bare
finite parts differ from renormalizing each factor first. These are important
subdivergence obligations, not already implemented counterterm cancellations.

## The infrared limit is different in the three factors

| Factor | Coefficient of1/(epsilon*d) in Lambda/g10^2 | Bare finite d->0 limit |
| --- | ---: | --- |
| U1 | 0 | Exists coefficient by coefficient |
| SU2 | 1509/10 | Contains inverse-d and logarithmic terms |
| SU3 | 3027/20 | Contains inverse-d and logarithmic terms |

The U1 result still contains UV poles. Its finite IR limit is not a
renormalized physical threshold. Some neutral-vector mass sets affect the
coefficient through the other leg of the quartic vertex, even when their
direct U1 charge vanishes. For SU2/SU3, setting the massless assignments0
before differentiation would conceal nonzero terms. This is not evidence of
a model anomaly; the common UV/EFT partners have not all been assembled.

## The actual inverse-d term has a verified one-soft origin

After V2 completed, V3 opened the same quartic density at two vector legs.
A matrix contraction and a separate derivative of all six unordered field
slot choices agree on every45x45 entry for each of the five mass projectors:

    Sigma_QQ,V4/ell = g10^2 (D-1) sum_s K_s A(x_s),
    K_s,ac = sum_ebd f_abe f_cde(P_s)_bd.

The independently constructed light ideals have ranks1,3,8. Full projector,
Gram-nullity, diagonal Schur and zero off-diagonal identities are checked.
In units Sigma_pole/(ell*60*g10^4), the hard-loop graph-local coefficients are
(-1309/200,-1509/200,-1009/200)/epsilon. They are NOT physical gauge-boson
masses or a permission to add mass counterterms to the action. Contributions
from other families may cancel or modify them.

Closing that independently opened kernel on the light vector loop reproduces
the ENTIRE inverse-d pole and finite polynomial in V2. Its dimensional factor
is (10+epsilon)(3-2epsilon), exactly30-17epsilon-2epsilon^2. Thus the leading
IR behavior is precisely the actual one-soft structure described by OSF1,
including its finite logs and evanescent terms. It was not assigned the value
needed to cancel the measured answer. U1 has zero light adjoint charge, so
this closure vanishes even though its opened graph-local mass kernel does not.

This identification supplies a specific subtraction dependency. It does not
perform the common UV/EFT subtraction, dispose of the d0 logarithms, or sum
the other families. The earlier FCI+HTB known sub-sum remains unchanged. This
bare primitive is not silently integrated there as an already renormalized
finite contribution. Its UV forests, all-soft partner and remaining mixed
terms require explicit treatment before a finite matching claim.

## Verification, failures and research-capability evidence

Primary contracts color matrices. Replay independently rebuilds all720
orthonormal10-plane Lie brackets, contracts tensor entries and derives the
Lorentz polynomial by explicit magnetic-plane sums at D4,6,8 with a degree
bound. Every table byte agrees. The separate verifier uses projected norms,
an alternate weak non-Cartan probe and alternate color Cartan, and checks
mixed-factor X/Z coefficients vanish. Unit normalization and mass-resolved
indices are tested, avoiding the historical unnormalized H frame.

Smooth Mellin derivatives at two frozen diagnostic IR arguments reproduce
all nine Laurent coefficients (18 evaluations) with maximum scaled error
3.6259132757e-81. Fifteen independent convergent positive Schwinger integrals
at epsilon5/4 agree within1.52955908132e-46, versus1e-25 bound. These are
diagnostic integral points, not new physical parameter choices. Native and
separate symbolic checks are exact; numerical comparisons use the frozen
80/45-digit precision requirements.

Controls detect an incorrect Wick density factor, omitted pairing, omitted
orbital/spin terms or wrong spin magnitude, premature D4, lost epsilon terms,
wrong external-coupling normalization and omitted nonzero massless terms.
V3 separately detects half closure and lost finite terms in the non-Abelian
channels. Global T reversal and the gyromagnetic sign are INSENSITIVE at this
even order; neither is independently certified by this primitive alone. No
source-normalization or arbitrary-width test is claimed in source-zero xi1.

One failed native is preserved. V1 assumed the Gram used shape/entries rather
than BFT1's105 sparse triples; it failed before color/amplitude contraction.
A non-daemon watchdog delayed that already failed process to its180s exit124.
That was an avoidable input/harness failure, not a hard physics computation.
V2 fixes only that decoder and watchdog lifecycle; all scientific inputs,
methods, tolerances and caps remain. V1 sources, preparation and full capture
are intact. No failed run is counted as passing or erased.

V2 native times after imports6.4273803/36.8385548s; separate validation
36.2449461s; V3 supplement1.0046075s. Observed successful sample counts4/19/19/1;
maximum53,239,808 bytes, NOTpeak. The supplement's one startup sample does not
bound its unobserved peak. Failed V1 samples91/max48,693,248 bytes, NOTpeak.
Limits180s natives/240s verifier,120s supplement, sampled8GiB private,
350MiB launch floor and2MiB total package were retained. Preparations2119,
2133 and2140 bindings, plus17 V3 direct bindings and its authenticated nested
manifest. Full captures/frozen sources are retained; completed V2 work was
not rerun for V3.

Track B demonstrates a compact actual primitive calculation and identification
of a required IR partner, together with a costly avoidable schema mistake.
All methods still share the physical action, projectors, software and AI
analyst. This is bounded computational evidence, not outside/Lean/empirical
validation of the theory. The mathematical primitive is not a new physical
unification prediction.

The delegated research_check.py e4 completed six checks with their expected
exits; full output is external readiness.jsonl. Historical custody remains
exit2/seven, not overall PASS. Old evidence, action, point, main, scientific
authority, scalar140%/1.94%/20.27% diagnostics, mismatch.745476, absent Yukawas,
quartetFAIL3960/648 and protected pauses/blockers are unchanged. No full finite
C1, E5/A5 promotion, physical quantum-control claim or external action follows.
