# V3 prelaunch parsed-slot bookkeeping correction

Code inspection before launching V2 caught an overrestrictive bookkeeping
assertion: differentiating ALL34 Hessian slots also visits the two
initially-zero portal coefficients lambdaPhiS and lambdaSigmaS. Their
derivative carriers are present and must evaluate to their exact zero values.
V2's expected parsed-name set listed only the five nonzero S derivative names.

V2 was NOT executed. Preserve verify_v2.py.source.txt, its validation preparation
and controller as an unlaunched revision. V3 includes both zero portal names
in that assertion; it changes no derivative, value, normalization, input,
scientific condition or cap. Parsing the S-independent nested mphi2 remains
unnecessary; it is not set to zero. There is still one failed native worker
and one failed verifier worker, plus this one prelaunch bookkeeping correction.
