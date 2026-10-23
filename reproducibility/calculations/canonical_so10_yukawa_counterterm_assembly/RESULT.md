# YCA1: the full one-loop Yukawa parameter-pole matrices close

For R=10,126 the assembled barred physical UV parameter counterterm is

    deltaY_R,pole = 1/(16*pi^2*epsilon) * {
      [W^T Y_R + Y_R W + k_R Y_R]/4 - (135/8) g10^2 Y_R },
    W=(5/8)Y10^dagger Y10+(63/8)Y126^dagger Y126,
    k_R=Tr_family(Y_R^dagger Y_R).

Both family matrices remain general complex symmetric3x3. The first fermion
field carries a transpose, not a dagger. The scalar trace already includes
all three families; its independent off-diagonal coordinates have weight2.
This is a parameter-pole input, not an adopted finite scheme or beta function.

Receipt `validation_receipt.json`, SHA-256
`323d78b8262e0b9ec86ca55fdcf1a59b2e6328a0fcf17926dac0e547ac364980`,
status QUALIFIED_FULL_ONE_LOOP_YUKAWA_PARAMETER_POLE_ASSEMBLY.
Scientific/director acceptance NOT_PERFORMED; state113/authority34of39 unchanged.

## What was calculated and reused

The primary route forms the measured FYS1 family wavefunction matrix and
pulls both fermion fields and the scalar through the bare bilinear. The
replay extracts the independently tabulated full48x48 wavefunction pole,
substitutes its explicit family-index entries into the bare fields and
solves the differentiated first-order coefficient equations. They share
IO/types but no assembly routine or peer output.

The proper pure-Yukawa vertex zero is authenticated YPP1 reuse. The gauge
term uses the qualified GYV1 two-width-independent image in the primary
route and its actual Casimir contraction in the replay. No loop integral
was newly evaluated, and the old large gauge contractions were not repeated.
The relative normalization is fixed by actual FYS/FKP inverse-propagator
signs and the bare-field chain rule, not a desired Slavnov cancellation.

All18 complex matrix-entry polynomials agree, including their separately
reported Yukawa/gauge and external-field pieces (108 compared component
polynomials including Y). Each carrier's full3x3 answer has1362 polynomial
monomials when all9 entries, including symmetric duplicates, are counted.
Those counts are bookkeeping, not independent physical inputs.

Symmetry, conjugate-density transport and homogeneous degree3 were checked.
The constant-unitary congruence law is proved algebraically in DERIVATION;
two exact diagnostics, one nonreal unitary and one three-family cycle,
check36 transformed counterterm positions and the trace/matrix laws.
They are mathematical diagnostics, not numerical flavor benchmarks.

The gate checks167936 original two-carrier internal/scalar positions and
335872 scalar-metric products, using the actual primary/replay YCT maps.
Together with the full48x48 FYS tensor identity this proves closure in all
1511424 family/internal/scalar slots by tensor factorization. That large
polynomial array was not expanded, and no new loop coefficient count is
claimed for it. The other56 real scalar directions acquire no pole through
this barred dimensionless assembly; this says nothing about finite terms.

Wrong first-leg transpose/conjugation, omission of either fermion image,
omission of the scalar image, extra family3, lost off-diagonal trace terms
and replacing the fermion matrix by its averaged trace all change the
answer. These controls are sensitive in the symbolic24-real-variable domain.

## Execution and limitations

Primary/replay/gate COMPLETED exit0 in4.0105498/24.8306276/42.9329562s after
imports. Their3/13/22 private-memory samples have maxima55,816,192/
78,966,784/71,532,544 bytes, respectively; these are sampled maxima, not
peaks. Frozen600s/8GiBsampled/350MiBfloor/16MiB limits were unexhausted.
50/57 input bindings, eight source copies and all complete captures remain.
No failed worker, verifier or source correction occurred in this increment.
Fresh current-turn E4 completed expected exits0,0,0,0,0,2; custody remains
exit2/seven unresolved NOTPASS. Hashes authenticate reuse, not fresh science.

The AI-capability gain is a complete symbolic assembly and family-covariance
check without re-expanding or rerunning qualified diagrams. The reference
anchor is the bare-field chain rule with inherited published normalization
comparisons in FYS/GYV. Shared action, measured loop inputs, maps, software
and AI authorship remain common-error risks. This is internal mathematical
corroboration, not independent scientific or empirical model confirmation.

The scalar hatted pole2/3 remains separate. A full finite-hat field/source
transformation, mass/source/VEV/tadpole counterterms, fermionic measure/phase/
QAP, complete parent forest and finite matter C1 are not qualified here.
No relation y=g, parameter value or rescue fit was imposed. Original bosonic
hierarchy exclusions and the separate finite-point140% singlet warning remain.
Flavor stays paused; HB1/C5 remain blocked; quartetFAIL and historical
evidence are preserved. E5/A5 and physical matching/unification remain open.

## Next smallest scientific action

Read the actual432 dimension-one GF auxiliary-scalar coefficients in their
original frame and transport them to the matched matter/scalar carrier.
Determine the allowed mass/source/VEV insertion before computing the mixed
gauge/auxiliary/scalar fermion self-energy pole. The dimensionless vertex
exclusion of these entries does not prove that their mass contribution
vanishes. No VEV or tadpole normalization should be silently selected.
