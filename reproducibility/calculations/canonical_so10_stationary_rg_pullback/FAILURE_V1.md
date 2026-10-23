# SRG1 V1 parameter-name schema failure

The first native primary exited1/FAILED at the dimensional-weight check,
before building stationary matrix jets or completing any result/table.
Its complete primary_capture.json, original sources/copies, preparation.json
and controller_failure.json remain unchanged. Replay/validation did not run.
Resource observation succeeded; this was not a timeout or physics mismatch.

The recovered parameter dictionary names Hermitian component ROWS as
z4:im, while polynomial VARIABLE names use z4_im. The first weight lookup
handled only the latter suffix and raised KeyError('z4:im'). This is an
avoidable schema error, not evidence against parameter dimensional grading.

V2 maps both explicit component namespaces back to the same parent invariant
name. It changes no coefficient, weight, tolerance, physical input, resource
limit or mathematical acceptance condition. New frozen primary_v2.py retains
the old primary.py. Replay/verifier change only preparation/output paths;
all V2 artifacts have explicit unique names checked before launch. Neither
the failed V1 nor unfinished intermediate checks are relabelled PASS.
