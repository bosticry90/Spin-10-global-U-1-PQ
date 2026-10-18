# Singlet pole control: the formal one-loop correction exceeds the tree mass

The same classically feasible scalar point does not support a small
first-order singlet pole correction in the declared MSbar expansion. The
complete one-loop coefficient on the selected electroweak-unbroken stationary
branch is larger in magnitude than the tree-level squared mass. This is
stronger evidence than the large tadpole displacement alone, because the
calculation retains momentum dependence, decay cuts and the required
vacuum-source insertion.

It is not a prediction of a new physical mass or width. A large first-order
coefficient does not establish that every reorganized input prescription or
the full quantum theory fails. Higher-order accuracy, the actual quantum
vacuum and a controlled physical input definition remain unestablished.
No benchmark, gauge, scheme, physical input or scientific authority is adopted.

Qualification is defined by the [record](RECORD.md), preserved
[primary correction](CORRECTION_V2.md), [verifier correction](CORRECTION_V3.md)
and actual [independent receipt](validation_receipt.json). The general
Spin(10) construction has not been excluded.

## 1. What was calculated

At Q²=omega²=60 and the unchanged finite point, the tree singlet radial
squared mass is 6/5=1.2. The table separates all terms, including their loop
factors. Units are the existing internal squared-mass convention.

| Contribution to the formal squared pole | Real part | Imaginary part |
| --- | ---: | ---: |
| Quartic scalar seagulls | -0.112120557206 | 0 |
| Two-cubic scalar bubbles | -1.255870823946 | -0.235571666346 |
| Total one-particle-irreducible self-energy | -1.367991381152 | -0.235571666346 |
| Tree-vacuum source insertion | +3.031443946682 | 0 |
| Complete first-order correction | +1.663452565530 | -0.235571666346 |
| Tree value plus formal correction | +2.863452565530 | -0.235571666346 |

The correction magnitude divided by the tree squared mass is
1.40004177709326; its real part divided by the tree value is1.38621047127503.
Thus the ordinary assumption of a small correction to this tree mass is
unsupported. The last row is a formal first-order expression, not an adopted
quantum particle mass. No nonlinear pole equation or shifted vacuum was solved.

The absorptive part gives a leading width/tree-mass diagnostic of0.19630972.
It is not a reliable measured or predicted resonance width when the real
mass correction is this large. The physical PQ-pair channel alone contributes
0.023873241464 to minus the imaginary squared pole; other open scalar channels
are included. Positive absorptive rates supply a normalization/sign check.

## 2. Why missing fermions and gauge fields do not complete another term here

The external radial state is entirely in the gauge-trivial S plane at tree
level. The declared renormalizable theory has no direct S Yukawa vertex to
the16_F matter multiplets. This earned field-content result was checked in
the [preceding source closure](../canonical_so10_singlet_quartic_running/RESULT.md).
No numerical flavor fit, Yukawa evolution or new matter assumption is used.

Every scalar coefficient block was specialized at the unchanged point and
canonically normalized. The full neutral S plane is isolated, and its
positive pole is nondegenerate within the neutral-singlet sector. The
derivatives of its squared mass along Phi and Sigma vanish at the current
zero portals; the independent field inventory verifies why. Consequently,
unknown Phi/Sigma one-loop tadpoles multiply zero in this first-order pole
component. They remain necessary for other quantum questions.

The complete spectrum has290 positive directions and38 inherited symmetry/
tuning zeros. Independent projectors separate33 gauge-orbit directions,
one physical PQ mode and four physical light Higgs directions. Both the
first and second S derivatives of the potential mass operator annihilate
EVERY gauge-orbit projector. At110 digits the largest primary residual is
about3.44e-111; the separate realified verification satisfies its own bounds.

This has a structural justification, not just a numerical zero: generators
annihilate S, the tree S plane is isolated, and the differentiated Ward
identity removes one-S orbit vertices. Terms with two S fields can couple
to gauge-orbit directions only through the Phi/Sigma portals, which vanish
here; the vector background is zero. Gauge fixing, ghost masses and kinetic
mixing also have no external S derivative. Thus no missing vector, ghost,
gauge-orbit or fermion propagator is silently replaced by a massless scalar.

The claim applies to this parent action and the selected stationary branch.
It does not establish every diagram of a physical electroweak vacuum, full
quantum restoration, or gauge independence to all orders. A changed point,
nonzero portals or new matter would require a new closure check.

## 3. Momentum dependence, signs and the vacuum insertion

[Martin, hep-ph/0312092v3](https://arxiv.org/pdf/hep-ph/0312092)
provides the general scalar self-energy convention in equations3.1–3.3 and
the complex-pole expansion in equations1.3–1.4. His discussion around2.13
explains that expanding about a tree stationary vacuum requires tadpole
graphs, whereas formulas omitting them need the corresponding vacuum
treatment. Only the scalar diagram identities are applied here; no new
Landau-gauge vacuum prescription or dimensional-reduction scheme is adopted.

For each canonical squared-mass operator M, define D=partial_r M/sqrt(3/5)
and E=partial_r² M/(3/5), at the fixed raw S background r=1. With
A(x)=x[ln(x/Q²)-1], A(0)=0, the evaluated expression is

```
Pi(s)=sum_blocks d/(32pi²) [
  sum_i E_ii*A(m_i²)+sum_ij |D_ij|²*L(s;m_i²,m_j²)],

L(s;x,y)=integral_0^1 du ln[(u*x+(1-u)*y-u*(1-u)*s-i0)/Q²].
```

All35 blocks/328 real directions and all34 potential coefficient slots are
retained;15 blocks have nonzero S vertices. Dimensionful z6 belongs in this
self-energy even though it did not enter the dimensionless quartic beta.
The primary uses exact field degrees and analytic quadratic logarithmic
primitives/cut lengths. The independent route uses a separate29-term ledger,
background interpolation, realified spectral projectors,148 numerical
Feynman-parameter integrals and two-body phase space.

At a tree stationary vacuum the complete correction is Pi(6/5) plus the
source insertion. The canonical cubic self-coupling and the established
singlet response give

```
delta_s_source=(18/5)*delta rS=3.031443946682329...
```

Keeping only Pi would give a negative formal real squared pole; including
the source makes it positive but still a large correction. Neither value
justifies a physical particle-mass interpretation without the proper terms.

The independent calculation checks a formal tadpole-free input translation
for the SAME bare theory. Writing v²=3/5, lambdaS=1,

```
delta m²=-T_can/v, delta v=-T_can/(2lambdaS*v²),
6lambdaS*v*delta v=3delta m².
```

In that parameterization the translated tree mass supplies2delta m² and the
finite mass counterterm suppliesdelta m². Their sum agrees with the original
source insertion through first order in a formal loop-counting parameter.
The bare-mass translation was checked at the same order. Omitting the
companion translation fails. These are perturbative identities, not a
numerically controlled finite shift or adoption of new physical inputs.

## 4. Physical massless modes remain; a zero-momentum shortcut fails

The surviving physical PQ and Higgs zero modes are included. At positive
timelike s, L(s;0,0)=ln(s/Q²)-2-i*pi is finite and has the expected cut.
The separate O(2) singlet reference reproduces its PQ-pair absorptive term
with the correct identical-particle factor.

At zero momentum, however, these same massless scalar bubbles generate a
nonzero logarithmic IR coefficient, approximately0.01022089907265. This is
why an unregulated effective-potential curvature cannot replace the pole.
The verifier's regulated Euclidean curvature values are

| Regulator squared mass | Zero-momentum curvature | Relative finite-difference error |
| --- | ---: | ---: |
| 1e-6 | -1.600428539868 | 6.02e-40 |
| 1e-9 | -1.671036585517 | 5.86e-34 |

These regulators are numerical limit checks, not physical propagator masses.
The logarithm is a defect of the zero-momentum substitution, not a divergence
of the finite one-loop timelike result or proof that the theory is inconsistent.

## 5. Execution history, limits and scientific direction

There were two primary attempts and two verifier attempts:

- The first primary stopped before integrals on a structural Hermitian
  equality assertion. The correction requires exact algebraic zero residuals
  and numerical Hermiticity; it does not symmetrize an invalid matrix.
- The first verifier exposed its own interpolation error: it used the
  derivative at r=0 instead of r=1 and omitted the quadratic contribution.
  The corrected version adds a literal polynomial control and retains all
  previous comparisons and tolerances.

The accepted primary completed in about1.13 seconds after imports and the
accepted verifier in about50.14 seconds. Both remained within120seconds/8GiB
and the direct350MiB available-commit gate. Complete failed and accepted
captures/source hashes remain preserved. No failed attempt is scientific
PASS; zero fresh byte-identical replay pairs are claimed.

The independent per-block integrals agree within the frozen1e-35 threshold;
the primary80/110-digit pole evaluations agree within1e-50. Counts, projector
closure, spectral sums, scalar CW limits, cut signs, O(2) normalization and
same-bare identities are checked. Shared action/cache/kinetics, mathematical
standards, software and analyst still limit independence. This is not expert
or experimental confirmation.

Defer further physical Higgs matching at this point until quantum input/control
is addressed. The most useful next bounded consistency test is the singlet
pole's explicit matching-scale logarithm against the relevant parent running
parameters. In particular, at the current zero Phi/Sigma portals the tree
radial relation is m_radial²=-2[mS²+60lambdaPhiS+(3/5)lambdaSigmaS]. The
one-loop UV S² projections can test the corresponding beta combination
without a numerical flavor fit. This would check scale consistency, not
reduce the observed correction by selecting a convenient scale or new point.
No iterative pole resummation, new parameter release or scalar search follows
automatically from this failure of a small first-order correction.

The classical full328 quartic/contact/mass/Higgs results remain valid. The
new finding concerns quantum control of this specific expansion. Prior failed
benchmarks/domains, closed curves, quartet discrepancy, E5/A5 unqualified
status, HB1/C5 blocks, uncalculated C1_GS, paused flavor and historical custody
exit2/seven remain intact. Statev113/authority34 of39 is unchanged. Science
and AI capability remain equally important; the director's education is
voluntary/nonblocking. The two preserved implementation errors are relevant
AI-limit evidence alongside the corrected calculation. Investigation incomplete.
