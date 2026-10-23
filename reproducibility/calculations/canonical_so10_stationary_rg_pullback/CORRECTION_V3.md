# SRG1 V3 verifier zero-format correction; completed V2 natives reused

primary_v2 and replay_v2 both COMPLETED with full observed captures and
authenticated compressed results. The separate V2 verifier completed all
exact matrix comparisons,531 Goldstone-compression positions and numerical
W comparisons before failing its line77 zero STRING equality. Primary
exports exact zero as "0"; replay formats its proven exact zero as "0.0".

The scientific requirement is zero value, not identical presentation. New
verify_v3.py converts those three entries in both outputs to exact Rational
numbers before comparing with zero. The original assertion, source/copy,
validation_v2_capture.json and controller_failure_v2.json remain unchanged.
This is an avoidable verifier serialization error, not a nonzero coefficient.
It is not evidence that the later finite-scale check passed; that check did
not run in V2. Neither failure nor incomplete validation is relabelled PASS.

V3 authenticates and reuses the two COMPLETED V2 native outputs/captures;
no scientific native rerun. It launches only the corrected separate verifier
with a new exclusive preparation, capture and receipt. No coefficients,
tolerances, physical premises, resource limits or acceptance requirements
change. The original V1 namespace failure remains separately preserved.
