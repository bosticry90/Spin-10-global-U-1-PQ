# V2 controller collision; uncaptured native table remains unqualified

V2's corrected primary wrote primary_tables.json.gz, then its outer controller
attempted exclusive creation of primary_capture.json. That name already held
the V1 FAILED capture. Exclusive creation correctly preserved it and raised
FileExistsError. controller_failure_v2.json contains the complete traceback.

The V2 native RESULT/stdout was held in the controller's in-memory capture
but was NOT saved before the collision. Its table is therefore preserved as
an unqualified/unfinished evidence product, not authenticated as a successful
native result. No primary_result.json exists. Do not infer completed scoped
validation from that table. No replay or validation ran in V2.

This is a second avoidable orchestration error: the first correction changed
the worker path without versioning the capture paths. It is distinct from
the V1 serialization-precision assertion failure. Neither failure is erased
or relabelled PASS. The repeated engineering weakness is part of TrackB.

V3 uses explicit primary_v3/replay_v3/validation_v3 artifact names and checks
every prospective output path before launch. Native sources retain the V2
arithmetic correction; replay and verifier change only frozen input/output
names. This new bounded continuation repeats the SMALL affected computation
to obtain complete observed captures, not any previously qualified loop.
No physics input, resource bound or scientific acceptance requirement changes.
