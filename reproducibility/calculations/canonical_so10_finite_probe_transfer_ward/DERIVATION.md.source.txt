# Prospective transferred Ward reduction and regulator limit

Use the full actual EPV U(k,l), PFJ A=0 current, and NFP CSW ending identity.
Source-triangle phases and the two physical-source Euler polarizations are
inherited with their authenticated definitions. With P=K-R,Pprime=L-R,
the complete ordinary/source numerator, before any angular integration, is

```
Kbar Rbar Lbar - (Pbar Rbar Lbar+Kbar Rbar Pprimebar)/2
 = (Rbar² Lbar+Kbar Rbar²)/2 = Rbar² jbar.
```

The last equality uses the actual barred Clifford algebra, not commuting
the three independent slashes. The two source primitives are matrices and
cannot separately be replaced by the constant-probe scalar S. A single
source coefficient does not create an additional family trace or Nambu half.
All external hats0 imply khat=lhat=rhat. Rbar²=Rfull-hat² gives the direct
mixed-PS insertion H_a and the adjacent-inverse term. After the full
nonminimal ending reduction, the latter is the root E_r-1, not a guessed
negative Ward remainder. E_k E_l stays ordered on its actual two momenta.

Set j=(k+l)/2,a=(k-l)/2,m=(P+Pprime)/2. Then

```
D_a(j)=1/[|j+a|²|j-a|²],
Rfull=|j-m|², E_k E_l=exp[-2c(j²+a²)],
A_a=N exp(-2c a²) integral exp(-2cj²)(E_r-1) jbar D_a,
H_a=-N exp(-2c a²) integral exp[-c(2j²+Rfull)]
                       hat_j² jbar D_a/Rfull.
```

At fixed positive c, the unheated-unit term is odd under j->-j: D_a and
exp(-2cj²) are even. For a nonzero, its nodes have degree2; for a0 its
numerator gives degree3. Both are locally integrable for D>=7/2. Thus
discarding that integrated unit term is justified; no arbitrary IR extension
of a critically singular separate tadpole is introduced.

Compare a with0 at the SAME m,c,epsilon. Factor exp(-2c a²) outside both
kernels and write deltaD=D_a-j^-4. The exact denominator difference is

```
deltaD = [4(j.a)²-2j²a²-a^4]/[j^4 |j+a|² |j-a|²].
```

At |j|>2|a|, the denominator is at least j^8/16 and the absolute numerator
is at most(25/4)j²a². Thus |deltaD|<=100a²/|j|^6.
B_D(a)=integral |j||deltaD| is finite: degree3 at j0, degree2 at j=+/-a,
degree5 at infinity. D in[7/2,4] gives strict integrability margins1/2,3/2,1.
Homogeneous rescaling gives B_D(a)=|a|^(D-3)B_D(unit); the unit-direction
integral is uniformly bounded on that compact D interval. Rotations remove
its direction dependence. At a0 the difference is exactly0.

For the hatted difference choose a two-dimensional physical plane containing
a,m (an enlarged plane if they are collinear). All scalar factors depend
on transverse j only through j_perp²; the transverse vector components
integrate to zero, so the surviving jbar is its physical parallel component.
The split continuation has

```
integral hat_j² f = [-2epsilon/(D-2)] integral j_perp² f.
```

The remaining radial dimension D-2 is in[3/2,2], with bounded sphere factors.
This identity is first obtained for ordinary split tensor moments and then
analytically continued; it does not posit negative-dimensional positive
probabilities. Since m has no transverse part, j_perp²/Rfull<=1.
Consequently the difference inside the common heat prefactor satisfies
|deltaH|<=(4/3)epsilon*N*B_D(a), uniformly in c. It vanishes jointly.

For the root difference,

```
deltaA=N integral exp(-2cj²)(E_r-1) jbar deltaD.
```

Its absolute integrand is bounded by N|j||deltaD|. N is bounded for compact
positive mu_R² and epsilon in[0,1/4]. On compact j regions E_r-1 tends to0
uniformly as c->0. The uniformly integrable tail bound just proved permits
uniform dominated convergence also when epsilon varies. Thus deltaA tends0
along every joint path. This argument preserves the unheated subtraction;
discarding it pointwise instead of after integration would break the proof.

NFP1 bounds the whole constant-a0 group at momentum m; do not assume separate
regulator limits commute. H_a+A_a=exp(-2ca²)[H_0+A_0+deltaH+deltaA]. The common
prefactor tends1 and the whole0 group is bounded. Therefore the transferred
group has joint limit jbar coefficient mbar/6, independently of a. Separate
hatted/root shares still depend on epsilon logc and cannot be discarded.

Restoring color, the selected finite first-variation coefficient is
`i g10² CU mbar/6`, with CU=w_r² C_r/2 and the same NFP conventions. The
unmodified symmetric kinetic counterterm has image i g10² F mbar,
F=-CU/6. Checking the two independent P,Pprime coefficients is a late
applicability test, not fitting F from this limit. Baseline freedom common
to the ordinary/source products stays free. Complete finite kernels away
from the regulator-removal limit, positive-dimensional insertions, other
fields, multiple variations, measure/phase and physical E5/A5 are not proved.
