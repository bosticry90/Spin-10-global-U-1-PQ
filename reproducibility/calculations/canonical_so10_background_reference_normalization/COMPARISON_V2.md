# BCR1 comparison correction, before rerun

The first primary run completed the carrier, source, normalization, inverse and
shape steps but stopped at the unsimplified Gamma/power identity. Its source and
FAILED capture remain unchanged; no partial result is accepted. This was not a
resource termination. V2 explicitly removes the common Gamma(1-D/2) by the
Gamma recurrence and uses one logarithm branch for the remaining power. The
independent verifier still evaluates the original Gamma formulas numerically
and checks the epsilon-pole/contact term. No mathematical condition is removed.

V2 also stores sparse sector dictionaries once instead of repeatedly extracting
the same matrices. The replay's ordered trace uses intersection of the two
nonzero position sets. The original scope, resource limits, proof and constants
are unchanged. Both native routes must complete from frozen inputs; no reuse
of the failed worker's intermediate values or one-route partial qualification.
