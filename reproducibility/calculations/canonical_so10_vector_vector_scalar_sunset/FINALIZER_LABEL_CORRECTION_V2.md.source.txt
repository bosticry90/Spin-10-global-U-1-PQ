# Prelaunch finalizer label correction

The measure worker was deliberately captured under the initial exact phase,
producing combined_exact_capture/result.json. Frozen finish.py instead looked
for combined_measure_capture/result.json. Review caught this before any
finalizer execution. Preserve finish.py and its original source copy unedited.
finish_v2.py changes only that evidence-label tuple to the actual exact phase;
the mathematical assembly, gates and resource contract are byte-identical.
Freeze V2 before execution. This is an unexecuted harness mismatch, not a
failed scientific calculation or permission to alias/relabel native evidence.
