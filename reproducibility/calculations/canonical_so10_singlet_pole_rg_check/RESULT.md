# Singlet pole RG consistency: induced portals are required

The complete one-loop singlet pole coefficient passes its local RG/log
consistency test at the unchanged scalar point. Its explicit scale logarithm
cancels the running of the stationary tree mass exactly. Both the initially
zero Phi–S and Sigma–S portals are generated at one loop and are essential
to that cancellation.

This strengthens the internal consistency evidence for the pole calculation.
It does not reduce its previously qualified large correction, establish a
physical mass, prove higher-order accuracy or validate the GUT. A zero allowed
coupling at one reference scale is a legitimate input; holding it zero under
running would describe a different assumption not supported by these equations.

The [record](RECORD.md), [primary data](primary_result.json) and actual
[independent receipt](validation_receipt.json) define qualification. No
new input, benchmark, gauge, scheme, scale or scientific authority is adopted.

## 1. What the one-loop projection determines

Use the same parent dimreg/MSbar action and point. Write beta_p=beta_p^I/(16pi²)
at one loop. The field-normalization and general one-loop conventions are
those of [Luo, Wang and Xiao](https://arxiv.org/pdf/hep-ph/0211440), equations13,
22 and38–43. The pole and tadpole convention is the one applied in the
[preceding pole result](../canonical_so10_singlet_pole_control/RESULT.md),
anchored to [Martin](https://arxiv.org/pdf/hep-ph/0312092).

On the formal backgrounds Phi=a*Phi_v, Sigma=b*Sigma_v, S=c*S_v, phi=0,
the S-dependent tree terms are

```
(3/10)mS²*c²+18lambdaPhiS*a²c²
 +(9/50)lambdaSigmaS*b²c²+(9/100)lambdaS*c4.
```

The scalar UV polynomial Tr(M²)/2 was reconstructed with all34 coefficient
directions,35 blocks and328 real fields. M is a squared-mass operator.
The full odd-c coefficients vanish exactly. The c² coefficient contains
only1,a²,b², and its c4 coefficient is independent of a,b. These are complete
polynomial checks, not a sample of potentially positive field directions.
No logarithm or mass-positivity assumption on these formal backgrounds is used.

S has no direct gauge generator or allowed parent Yukawa vertex. Its one-loop
anomalous dimension vanishes. At the actual lambdaPhiS=lambdaSigmaS=0, other
external wavefunction terms multiply zero. Thus the four projected coefficients
below are FULL parent one-loop values AT THIS POINT, even without numerical
Yukawa matrices. They are not general beta functions at nonzero portals, and
do not supply the full RG flow or resume paused flavor work.

| Parameter | beta^I at the existing point |
| --- | ---: |
| mS² | -2.63202612614018990 |
| lambdaPhiS | +0.9699814857132424 |
| lambdaSigmaS | +0.413852774354334 |
| lambdaS | +20.000009957245796 |

The portal coefficients have exact rational values
1212476857141553/1250000000000000 and206926387177167/500000000000000.
The mass expression, including the already frozen weak-root parameter, is
retained exactly in the primary data. The lambdaS result reproduces its
preceding complete one-loop calculation.

An independent canonical O(2) plus ten-complex-vector reference gives

```
beta_mS²^I=8lambdaS*mS²+20lambdaVectorS*mphi²+40|z6|²
```

at these zero portals. The separate literal norm/cubic Hessian reproduces
this expression and agrees with the full328-field extraction. In particular,
dimensionful z6 contributes to the mass beta while remaining absent from the
dimensionless singlet-quartic beta. Established QFT identities are inherited
human knowledge; the new result is their application to the actual action.

## 2. Exact pole-log cancellation

Let v²=3/5 and P=mS²+60lambdaPhiS+(3/5)lambdaSigmaS. On the declared
stationary branch the tree radial squared mass is -2P=6/5. Define

```
B_P=beta_mS²^I+60beta_lambdaPhiS^I+(3/5)beta_lambdaSigmaS^I
   =55.8151746812669545... .
```

Because the portals vanish at this point, their products with the running
Phi/Sigma backgrounds do not enter this first-order mass derivative. Those
unknown background responses are not set to zero.

With canonical S derivatives D,E of the squared-mass operator, the explicit
logarithmic coefficients are

```
K_1PI= -Tr(ME)-Tr(D²),
K_source=3Tr(MD)/v,
K_complete=K_1PI+K_source=2B_P,
beta_tree_mass²^I=-2B_P.
```

The exact primary remainder is zero. The independent reconstruction from the
qualified mass-basis weights and prior tadpole slope gives a remainder about
-4.41e-58, below the frozen1e-45 comparison threshold.

| Contribution | 16pi² times its explicit derivative with respect to ln(Q) |
| --- | ---: |
| One-particle-irreducible pole term | -91.8151926043094 |
| Vacuum-source insertion | +203.445541966843 |
| Complete one-loop correction | +111.630349362534 |
| Stationary tree-mass running | -111.630349362534 |

The explicit derivative of the complete one-loop correction is about
0.706907445489 in the current internal squared-mass units. The absorptive
cut has no explicit Q logarithm. The corresponding local tree-VEV-squared
RG/source identity was also checked, with numerical remainder about-1.64e-58.

Omitting the portal running leaves a nonzero remainder116.894401614814 in
the beta^I convention. Omitting the vacuum-source insertion leaves a
remainder about-203.445541966843. Neither can be removed merely by calling
the initial portal values zero or declaring a tadpole convention.

## 3. Predetermined scale check and its limits

The following rows change the explicit logarithms while holding the loop
inputs fixed, and add the FORMAL first-order tree-running companion. They
are not newly selected points or a finite integrated RG trajectory.

| Q/Q0 | Re of fixed-input one-loop correction | Formal companion tree mass² | Formal compensated real pole² |
| --- | ---: | ---: | ---: |
| 1/2 | 1.173461662773 | 1.689990902757 | 2.863452565530 |
| 1 | 1.663452565530 | 1.200000000000 | 2.863452565530 |
| 2 | 2.153443468287 | 0.710009097243 | 2.863452565530 |

Every row retains the same imaginary part,-0.235571666346. At Q0 the
correction magnitude/tree ratio remains1.40004177709. On the half-scale row
its ratio to the ORIGINAL tree mass² is about0.9974, still not a small
correction; the compensating parameter contribution must also be retained.
No favorable row is selected as a rescue. This local cancellation does not
bound two-loop effects, establish a preferred scale, or prove the formal
pole is a reliable physical mass. It only verifies the required first-order
scale covariance of the stated expression.

## 4. Verification and research consequence

The primary exact polynomial/trace route and independent canonical Frobenius
interpolation agree. The latter uses a separate29-term field-content ledger,
c=0,±1,±2 samples, independent a,b interpolation, the literal O(2)/vector mass
reference and the separately qualified pole/tadpole mass-basis data. The
expensive timelike integrals were not repeated. The common cache, action and
kinetic conventions remain shared assumptions rather than independent evidence
for those inputs.

Controls reject the wrong interpolation evaluation point, omitted generated
portals, omitted source, wrong mass-running sign and incorrect complex/real
cubic normalization. The two accepted native roles completed in about1.68
and1.14 seconds after imports, within120seconds/8GiB and immediate350MiB
available-commit gates. No new native failure and no fresh byte-identical
replay pair occurred. Complete captures, source copies, hashes and scoped
raw Git checks accompany qualification.

The important physical distinction is now explicit: the parent action already
contains these portal operators, but the zero-portal subspace is not invariant
under the local one-loop running. Their counterterms/running belong in a
same-theory quantum input definition. Their generation does not refute the
action or retroactively alter its reference values. The prior classical
certificates and the large pole correction both remain valid in their scopes.

This resolves the scoped one-loop RG-consistency question. Before another
quantum increment, reassess the research direction against the remaining
physical-input obligations and original restoration contracts. The current
point has earned classical feasibility, not a controlled physical benchmark.
Do not automatically release another coupling, search for favorable numbers,
expand Higgs diagrams or interpret this RG check as a quantum-viability PASS.
Any further calculation should address a consequential remaining uncertainty.

Track B credits the crossing of UV, finite-pole and source descriptions and
the use of a separate canonical reference. Published physics, shared software/
data and the same analyst limit independence; this is not expert endorsement
or an empirical test. Education remains concurrent, voluntary and nonblocking.
Statev113/authority34 of39, historical custodyexit2/seven, all old failures/
closed routes, E5/A5 unqualified status, HB1/C5 blocks, uncalculated C1_GS
and paused flavor remain preserved. No external action, publication, new
branch/worktree or protected promotion. The full investigation is incomplete.
