# Finite first-probe Ward limit with independent probe momentum

October25,2026, base36ced0de8f1570986cd21ff233ddc087112f455a. PROGRESS:
the selected constant-probe Ward result extends to independent Euclidean
probe transfer. The unmodified symmetric kinetic counterterm cancels the
resulting local joint regulator-removal limit. No coefficient was adjusted.
This is a bounded analytic/operator result; a new complete numerical
three-point finite-kernel table was neither required nor calculated.

## Scientific scope

Original unshifted SMA/CSW, one-loop parity-even physical PP, external hats0,
A0, one first independent rho insertion, formal grade0 in ALL
positive-dimensional orbit/mass/interaction insertions. Euclidean external
momenta are P=K-R, Pprime=L-R, with rho transfer K-L=P-Pprime. Require
positive nonexceptional P²,Pprime² and m², m=(P+Pprime)/2, at finite
transfers and compact physical scales. This is not a choice of physical
zero masses/Yukawas, an on-shell result, or a massive physical amplitude.

Actual finite-transfer EPV symbols, PFJ derivative-current coefficients,
NFP1 source/phase/color definitions and CSW source-Hessian identity are
authenticated dependencies. Q_full curvature and nonzero Ihat remain.
The root reduction is conditional on CSW's qualified four-leg source
identity, not a fresh full835-field root-trace component replay.

## Ordered algebra before integration

The actual quadratic kernel and its ordered inverse derivative are

```
U(k,l)=[[-2 k_mu l_nu, w k_mu],[-w l_nu,w²/2]],
-G0(k) U(k,l) G0(l)
 =[[w² k_mu l_nu/(2k²l²), -w k_mu/k²],
   [w l_nu/l²,             -2]].
```

Primary full5x5 multiplication and replay rank-one factorization agree,
retaining transverse and auxiliary blocks. Actual A=0 is checked before
projection; no derivative-rho current was silently omitted. The two
oriented current/inverse identities retain their separate k,l heat
factors E_k E_l. Replacing these with two heat factors on one momentum
changes the expression; that error is invisible when k=l.

The source Euler terms use distinct external inverse momenta. Their
noncommuting numerator reduction is

```
Kbar Rbar Lbar - (Pbar Rbar Lbar+Kbar Rbar Pprimebar)/2
 = Rbar² (Kbar+Lbar)/2.
```

Both explicit Clifford matrices and free-word algebra check the identity.
The source primitives are full ordered matrices before integration, rather
than two copies of the constant-probe scalar S. Internal hats survive:
Rbar²=Rfull-hat². As in NFP1, actual color contractions give the ordinary
CU=w_r² C_r/2 and the two source Euler coefficients sum to -CU.

Write j=(k+l)/2 and a=(k-l)/2. Then k=j+a,l=j-a,r=j-m, and the reduced group
is the hatted insertion H_a plus the ordered adjacent-inverse root A_a:

```
D_a(j)=1/[|j+a|² |j-a|²], N=exp(gamma_E epsilon)*(mu_R²)^epsilon,
A_a=N exp(-2ca²) integral exp(-2cj²)(E_r-1) jbar D_a,
H_a=-N exp(-2ca²) integral exp[-c(2j²+Rfull)] hat_j² jbar D_a/Rfull.
```

The unheated-unit root term is odd under j->-j and locally integrable
before being set to zero. No critical tadpole is assigned a new IR
extension. The root E_r-1 is inherited from the actual ordered free inverse
defect, not selected to make the final identity vanish.

## Why the transfer-dependent remainder vanishes

This is the central analytic improvement. Compare the transferred group
with the qualified constant-a0 group at the SAME m. Set deltaD=D_a-j^-4.
Its exact rational form gives

```
|deltaD| <= 100 |a|²/|j|^6  for |j|>2|a|.
```

The absolute majorant B_D(a)=integral |j||deltaD| has soft degrees3,2,2
at0,+a,-a and UV degree5. It is uniformly integrable on D in[7/2,4]
and bounded compact transfers. Homogeneity gives
B_D(a)=|a|^(D-3) B_D(unit); a0 is identically zero.

Choose a physical plane containing a,m. After transverse vector averaging,
the split hat moment gives -2epsilon/(D-2) times the ordinary transverse
radial square. Since j_perp²/Rfull<=1, the hatted difference inside the
common heat prefactor is at most(4/3)epsilon*N*B_D(a), which tends to zero.
This uses an analytic trace identity, not a positive negative-dimensional
measure.

The root difference is bounded by N|j||deltaD|, with the explicit factor
E_r-1 tending to0 uniformly on compact j regions. The uniform tail bound
therefore proves joint dominated convergence even as epsilon changes.
The common exp(-2ca²) tends1. NFP1 supplies the bounded **whole** constant
group limit; its noncommuting separate hat/root limits are not substituted.
Consequently the transferred joint limit is

**i g10² CU (Pbar+Pprimebar)/12 = i g10² CU mbar/6.**

This is nonzero before the counterterm. The proof establishes a local
limit for the entire selected first-variation group, not locality of
each finite-cutoff three-point function or a full contact-mixing theorem.
`DERIVATION.md` and `REVIEW.md` detail the assumptions, IR neighborhoods,
analytic continuation and dominated-convergence argument. The code checks
the algebra and bound constants/exponents; it is not a formal proof
certificate for every analytic statement.

## Fixed candidate and tests

Only after the independent operator routes completed did the verifier
read the original PFJ F and compare the symmetric kinetic density.
F=-CU/6 gives i g10² F mbar, canceling the derived local limit. Both
independent P,Pprime coefficients, two chiralities and zero complements
pass across2,048 matrix positions. Doubling the old candidate leaves124
nonzero positions. No new normalization is fitted and no complete mixing
space is declared exhausted. Beta baselines retain the selected common
freedom; chi4,kappa,b0 are distinct and unselected.

Fresh generic-witness controls change8 positions on deleting a source
Euler half,8 on replacing Pprime by P,8 on reversing the ordinary Clifford
word,16 on erasing auxiliary inverse blocks,4 on erasing the auxiliary
current, and16 on replacing one bosonic momentum by the other. These are
small algebra fixtures, not full model component counts. The heat error
is E_k²-E_k E_l and vanishes at k=l, an honestly insensitive constant limit.

## Failure, correction and execution

Original primary completed in5.6098319s after imports. Original replay
failed at JSON serialization because rank-factorized sparse matrix keys
were SymPy Integer objects. Its assertions ran, but it produced no
completed output and earns no qualification. Original native/source copy,
manifest, full failed capture and controller failure remain unchanged.
There is no original validation receipt. A separate shell-quoted generator
command failed before Python; no generated source was written. Its decoded
observation is retained externally, with raw-stream limitations disclosed.

V2 converts output indices to ordinary ints and uses distinct source,
manifest, output and capture names. Scientific assertions and caps are
unchanged. Original primary was reused after authentication; it was not
repeated or edited. Corrected replay took3.7912609s; verifier .1917789s.
The completed 4/3/1 resource samples reached59,527,168/60,264,448/397,312B.
The failed original replay's3 samples reached59,531,264B. These are sampled
maxima, not continuous peaks. All frozen180s/8GiBsampled/350MiBfloor/12MiB
limits held. The pre-report packet was258,267B with12 source copies;
preparation/continuation/validation bind45/64/71 inputs.

Corrected validation receipt SHA256:
`48d50d89ea8f00d044482fe7ac5afbe8837da8abb9eb784ce4fe071c3d397200`.
Full native captures and preservation/readiness records are retained under
the external finite-probe-transfer-ward-v1-2026-10-25 control directory.
Historical custody is exit2/sevenNOTPASS; authentication is not scientific
acceptance. No protected evidence or project_state.json is changed.

## Significance, limitations and next dependency

This removes the constant-rho restriction from the selected finite
mass-independent physical-fermion first-variation test. It demonstrates
that an ordered algebraic reduction and a uniform comparison theorem can
avoid unnecessary three-point quadratures. It also preserves a real
serialization failure and a separate shell-quoting error as workflow evidence.

The calculation and review share action, source and Clifford conventions,
CSW domain, NFP limit, software and AI author. They do not supply external
scientific/experimental validation. Positive-dimensional scalar/mass
insertions, other fields, multiple variations, complete connected-product
mixing, chiral measure/global phase, causal/physical limits, E5/A5 and
physical unification remain unresolved. Authority stays34/39, State113.

The next justified scientific dependency is the first positive-dimensional
scalar/mass contribution to the finite probe identity. Reuse the existing
general-Yukawa scalar and physical/sterile inverse evidence to determine
the smallest complete first-grade sector. The present grade0 result cannot
be transferred to it by asserting that all finite masses are UV-irrelevant.
