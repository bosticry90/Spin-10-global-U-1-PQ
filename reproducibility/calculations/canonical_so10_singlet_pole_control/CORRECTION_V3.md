# Independent derivative evaluation-point correction V3

The first independent verifier failed the neutral block bubble comparison.
Its interpolation reconstructed M(r)=A+B*r+C*r², but used the central
difference [M(1)-M(-1)]/2=B as the derivative at the selected r=1.
That is the derivative at r=0. It omitted2C, including the known nonzero
radial/PQ cubic vertices from lambdaS. The original source, frozen validation
preparation and complete failed native capture remain unchanged.

The corrected verifier uses D_raw=B+2C, while E_raw=2C remains unchanged.
It adds a literal symbolic polynomial control showing the derivative at1
is B+2C and differs from B when C!=0. This repairs an implementation of the
already required fixed-background derivative; it does not change the theory,
primary result, tolerances, loop signs, massless prescription or acceptance
conditions. The primary is still unqualified until this verifier completes.

Standing AGENTS.md delegation admits one additional corrected verifier under
the same120-second/8GiB/350MiB bounds. It reuses the completed corrected
primary and retains every previous check. Preserve one failed primary and
one failed verifier in the final counts; no extra physical calculation or
parameter search is introduced. This is a prospective bounded continuation,
not a retroactive passing classification of either failed run.
