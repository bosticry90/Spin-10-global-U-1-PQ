# Preserved V1 execution failure and V2 arithmetic-order correction

The original primary.py and its source copy, preparation.json, run.py,
primary_capture.json and controller_failure.json remain byte-identical.
The scientific worker exited1/FAILED at its raw/canonical roundtrip assertion;
no native result or table was completed, replay/validation were not launched.
Resource observation succeeded; there was no timeout, process abandonment,
resource-limit termination or scientific result relabelled PASS.

Cause: the check compared an unrounded90-digit calculation to a shift parsed
back from vector(), which intentionally serializes60 digits. An absolute
1e-70 agreement is then impossible in general, even for an exact identity.
This was an avoidable implementation precision error, not a mismatch between
the raw and canonical equations. The full captured traceback is retained.

V2 changes ONLY that assertion's operand: compare ac to -S*mi*t0 at full
working precision. Its original1e-70 threshold stays unchanged. The complete
serialized coefficient/old-HTB comparisons retain the prospective1e-25 scaled
threshold. No inputs, physical assumptions, acceptance requirements or effort
limits change. primary_v2.py is a new frozen file; old primary.py is not edited.
The V2 controller points to that file and preserves its own failures separately.
Replay and verifier retain their original frozen mathematical sources.
