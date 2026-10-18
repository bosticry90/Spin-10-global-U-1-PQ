# Benchmark input control: large finite shifts and a failing tree scattering screen

The current parameter point fails a standard fixed-input, high-energy tree
scalar perturbative-unitarity test. A directly calculated coherent channel has

```text
|a0(uu -> coherent WW)| = 0.7680903223664... > 1/2.
```

This is a negative perturbative benchmark result. It does not refute Spin10,
all benchmarks of this construction, exact nonperturbative unitarity or the
possibility of a quantum vacuum. It is a stronger reason to defer expensive
physical Higgs matching at this point than the coordinate-dependent tadpole
shift alone. No input values, scheme or scientific authority were changed.

Use the [input/contact contract](RECORD.md), [coherent-channel contract](COHERENT_RECORD.md),
[radial-assessment contract](ASSESSMENT_RECORD.md), [input data](original_result.json),
[coherent data](coherent_original_result.json), [radial data](assessment_original_result.json),
their sources and three original/fresh pairs, and [final receipt](validation_receipt.json).
The director's supplied assessments are research inputs, not verification.

## 1. Counterterm reachability does not make the shifts small

The measured three scalar-reference tadpoles require the following conditional
mass increments to cancel their radial slopes at the fixed tree point:

| Parameter | Frozen value | Conditional increment | Absolute ratio |
| --- | ---: | ---: | ---: |
| mPhi2 | +0.02384604 | +7.56819904 | 317.38 |
| mSigma2 | -0.74702788 | +419.41928674 | 561.45 |
| mS2 | -0.6 | +0.26084425 | 0.43474 |

The masses have internal mass-squared units. These are finite algebraic target
increments, not selected renormalized parameters. Ratios describe this input
choice; they are not tuning probabilities or a universal convergence theorem.
The two declared bosonic diagnostic examples retain comparably large shifts.

Using the three masses alone also changes the weak mixed-mass rows. If the
previous S0 map is used to cancel only these measured radial targets while
holding the six selected mixed rows unchanged for this increment, it requires
additional large changes: z4 real/imaginary increments are about34.19 times
their original values, z6 real about80.38 times, and zEta real about41.72 times.
The six target zeros specify this increment; other unknown mixed loop targets
are not asserted to vanish. Ratios to zero frozen coefficients are undefined.

The direct unit-Higgs mass insertion differs between these two permitted
choices: approximately+1.64751 for mass-only and-22.09540 for S0. Neither is
a physical mass prediction or the complete relaxed insertion. This illustrates
why one cannot infer an observable from an isolated counterterm choice.
The same-bare translation p_new=p_old-hbar*d remains required; V82 already
proved its off-shell and path consequences. No translation or scheme is adopted.

[Expectation management](https://link.springer.com/article/10.1140/epjc/s10052-021-09285-4)
discusses related problems when fixing small scalar VEVs induces large mass
counterterms, and alternative tadpole treatments combined with EFT matching.
That established example supports investigating input definitions. It does not
demonstrate a controlled alternative for this Spin10 point.

## 2. Why the radial response is large

The complete three-radial tree Hessian has exact S decoupling at the frozen
zero-portal point. This is checked explicitly; it is not inferred from the
separate tadpole results. The coupled scalar-reference linear response is

```text
delta(a,b,rS) = (175.1060687852, 280.4601915630, 0.2173702099).
```

It is a first-order response, not a distant quantum minimum. The canonical
Hessian decomposition is

| Approximate direction | Mass squared | Projected scalar tadpole |
| --- | ---: | ---: |
| Mostly Phi, Sigma admixture0.0002585 | 0.08656156 | -117.41399 |
| S | 1.2 | -0.20204909 |
| Mostly Sigma, Phi admixture-0.0002585 | 2.99563152 | -649.73124 |

The mostly-Phi mode supplies+175.1133 to the Phi raw response; the mostly-Sigma
mode supplies-0.00724 there. For Sigma, those contributions are+0.45266 and
+280.00753. Thus the eigenmode attribution is explicit.

Both slope size and curvature matter. Dividing the same slopes by a comparison
curvature60I would give raw responses(0.25227,13.98064,0.0043474). This is an
internal dimensional comparator, not a changed benchmark. The very weak Phi
curvature provides strong amplification. The Sigma slope is already large
relative to its small VEV, and its smaller curvature further amplifies it.
Neither problem is settled by describing every individual coupling as small.

The scalar contribution includes all35 inherited SM blocks. The previously
derived vector/orbit terms are retained in the diagnostic bosonic examples;
longitudinal/ghost cancellation does not remove orbit curvature. Fermion and
Yukawa terms remain unavailable, and paused flavor work was not resumed.
Unknown cancellation is neither assumed nor excluded. A full quantum vacuum
and a controlled physical input prescription remain underdetermined.

## 3. Scale and gauge diagnostics do not rescue the point

At fixed parent parameters the explicit one-loop logarithm satisfies
T(Q)=T(Q0)-log(Q2/Q02)*B. Algebraic mass-square traces give the three scalar
canonical coefficients B=(92.17305866,344.20252718,0.16632509). No new loop
integral or old spectrum replay is needed.

| Q/Q0 | Scalar-reference raw response(a,b,rS) |
| --- | --- |
| 1/2 | (-15.64442,74.34234,-0.03069) |
| 1 | (175.10607,280.46019,0.21737) |
| 2 | (365.85656,486.57804,0.46543) |

The first two displacements remain large on this predetermined grid. No scale
is optimized or adopted. This is explicit-log sensitivity, not the uncertainty
of an RG-improved physical prediction: all parent running and complete fermion
inputs are missing. Compatible parameter translation is required to compare
the same underlying theory at different scales.

The two inherited positive gauge-width examples remain explicit diagnostics;
the same assessment propagates their known vector/orbit logarithms. Off-shell
gauge-coordinate dependence does not imply gauge-dependent observables.
No Nielsen-identity completion or gauge-independent pole mass is claimed.

## 4. A direct tree scattering failure independent of the tadpole prescription

The initial single real-direction entry has |a0|=0.31357156, below1/2. It is
preserved as INCONCLUSIVE, not promoted to PASS. The selected physical heavy
Sigma representation and its conjugate form six real directions. The actual
module is constructed using color and electric-charge generators, with exact
closure, metric and a unique invariant symmetric bilinear.

Let u be the unit radial Sigma direction. The fourth derivative in each
canonical real direction w_a is the same number:

```text
K = V4[u,u,w_a,w_a] = 78809129/2500000 = 31.5236516.
```

The cache-derived field-degree identity selects the candidate. Direct
polarization of the unchanged four pure-Sigma quartics confirms it exactly,
and a second generated direction is also checked directly. The final validator
uses paired-tensor coefficient convolution. The relevant physical coupling
combination is

```text
K = 8*lambdaSigma1 + 24*lambdaSigma2
    + 24*lambdaSigma3 + 32*lambdaSigma4.
```

For normalized identical pairs, the coherent final state is
sum_a |w_a w_a>/sqrt(12), with a=1,...,6, and the initial state is
|u u>/sqrt2. Their partial-wave entry is -sqrt6*K/(32pi). The symmetric
scattering matrix's spectral norm bounds this entry regardless of unknown
diagonal elements or additional channels. The exact certificate
6*K2>(16*22/7)^2, together with pi<22/7, proves the entry exceeds1/2.

The normalization follows the general scalar conventions in
[Goodsell and Staub1805.07306, eqs2--5](https://arxiv.org/pdf/1805.07306),
with independent single-scalar/O(N) and Fock normalization controls. A necessary
condition from this channel for future inputs in the same field orientation is

```text
sqrt6*abs(8*lambdaSigma1+24*lambdaSigma2
          +24*lambdaSigma3+32*lambdaSigma4) <= 16*pi.
```

Satisfying this one inequality would not certify the complete scattering matrix.
The current inputs fail it. All270 actual cross currents and identical-state
currents vanish, so no tree vector exchange contributes to this selected
channel. Its heavy charged scalar t/u exchanges are subleading in the
fixed-coupling high-energy limit. No general gauge diagrams were discarded.
These are high-energy partonic tangent states; they are not observed particles.

This is the usual local, fixed-input tree perturbativity screen. Finite-energy
scattering, RG-evolved couplings, loop-improved unitarity and exact quantum
unitarity are distinct questions. The large finite translations also mean
that existence of a better perturbative scheme cannot be settled by changing
notation. No conclusion is transferred to every benchmark or the theory.

## Scientific disposition

| Question | Disposition |
| --- | --- |
| Small scalar/bosonic-reference vacuum displacement | FAIL within tested reference |
| Allowed local potential counterterms reach radial targets | Yes, with large measured translations |
| Small finite input correction demonstrated | No |
| Fixed-input tree high-energy perturbativity | FAIL, explicit coherent channel |
| Complete quantum vacuum and same-theory controlled prescription | UNDERDETERMINED |
| Spin10 construction or nonperturbative theory excluded | Not established |

Defer further expensive physical Higgs matching at this parameter point. Retain
it as a qualified mathematical/reference benchmark and preserve every prior
calculation. The smallest useful next work is to turn this channel inequality
and the earlier necessary constraints into a compact benchmark-admissibility
decision before any proposed replacement search. A changed benchmark or physical
input prescription remains a director-controlled consequential choice; none
has been selected. Do not fit unknown fermion/threshold terms to cancel failures.

## Validation, AI capability and authority

Three original/fresh pairs reproduce byte identically. Independent final checks
use direct numerical parent-map solves, tensor coefficient convolution, an
operator commutant instead of a symmetric-bilinear nullspace, moving-slot
currents, Fock normalization, mass-square trace interpolation and closed radial
response calculations. No new failed execution occurred. The earlier V83
engineering/numerical failures remain untouched. Resource, source, state and
raw Git checks are required; verification completion is not a scientific PASS
for the failed perturbative screen.

This demonstrates bounded AI capability to connect an unfavorable loop result
to input sizes and a cheaper decisive tree test, while preserving an initially
inconclusive single entry. Literature supplies established standards. Shared
action, representations, software and analyst remain limits on independence;
multiple algorithms are not independent scientific endorsement. The director's
education remains voluntary and nonblocking.

Statev113/34of39, quartetFAIL3960/648,E5/A5unqualified,HB1/C5blocked,
C1_GSuncalculated,full328BFB/naturalness,matter/phenomenology gaps,flavor pause,
custodyexit2/seven references and all frozen inputs/evidence are unchanged.
No finite scheme, scale, new vacuum, replacement benchmark or authority is
adopted, and no blocked stage is activated. The investigation remains active.
