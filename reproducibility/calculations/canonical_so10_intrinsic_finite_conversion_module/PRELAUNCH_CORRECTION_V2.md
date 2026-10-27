# Preserved controller syntax failure, before preparation or workers

The first `python -B .../run.py` returned native1 while parsing run.py:
the conditional `else300` lacked whitespace. No preparer, source freeze,
worker, mathematical comparison or receipt ran. The original run.py is
unchanged and bound as failed source. The observed tool result is recorded
as an observation, not fabricated as a nested scientific-worker capture.

run_v2.py corrects only that lexical token. prepare.py had not run and now
freezes run_v2 and this correction, together with the original failed
source and tool observation. All scientific records, sources, inputs,
conditions and resource limits remain unchanged. No executed calculation
is relabeled PASS. This V2 is a routine controller correction under the
standing delegation.
