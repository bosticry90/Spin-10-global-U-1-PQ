# BCR1 resource correction, before rerun

V2 reached the fixed120-second limit, exit124, with no completed native result.
The last milestones were carriers47.466689s, symmetry100.486684s and scalar
trace forms100.735611s. This is resource-exhausted/incomplete evidence, not a
mathematical failure or a partial PASS. Its source, preparation and capture are
immutable. Together with the original unsimplified-comparison failure, two
unsuccessful native executions are retained; no verifier has yet run.

V3 memoizes the PURE exact scalar simplification function on immutable SymPy
expressions. Every row, zero, matrix product and comparison is still evaluated;
identical scalar expressions reuse their earlier canonical simplification.
It moves the inexpensive radial identities before expensive carrier work, so
the previously problematic comparison cannot waste a complete group-data run.
No scope, formula, precision, type, input, authority or resource cap changes.
Both complete native routes and the independent verifier remain required.
