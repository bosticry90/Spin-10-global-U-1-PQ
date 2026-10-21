# VQP1 V1 failure: wrong inherited Gram wire schema, no amplitude

Primary failed with TypeError at matrix(data['Gram']): BFT1 stores the Gram
as a list of sparse triples, whereas WHP1 projectors use shape/entries objects.
No stage reached the color/amplitude contraction or output table/result.
Exact frozen sources, preparation, primary_capture.json and external complete
capture are preserved. Replay and scientific validation were not launched.
This is an implementation/input-adapter failure, not a failed physical gate.

The native watchdog thread was not daemonized. After the immediate exception
it kept the owned failed process alive until the180s watchdog exit124. Thus
this was not a180s hard scientific calculation or evidence of computational
complexity; it was an avoidable controller inefficiency. The full trace,
observations and lack of an amplitude remain explicit.

V2 uses a strict105-triple,45x45 Gram decoder in native/verifier, and daemonizes
both watchdogs so ordinary exceptions terminate promptly. No physical input,
proof formula, expected coefficient, method, tolerance or resource cap changes.
New output names and a fresh preparation preserve all V1 evidence unchanged.
