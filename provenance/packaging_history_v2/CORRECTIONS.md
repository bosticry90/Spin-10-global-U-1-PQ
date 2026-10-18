# Publication packaging corrections

No new scientific worker was launched by these failures.

- The first receipt-authentication pass inspected only input_sha256 maps. The corrected pass also inspects byte_sha256, external_sha256 and supplemental_input_sha256: 743 bindings, including three historical policy inputs, authenticate. The initial narrow report is retained as limited scope.
- The expanded pass initially did not classify a removed historical AGENTS.override.md. Its exact expected bytes were recovered from Git and stored separately under historical/<commit>/. No old manifest or live policy was changed.
- The first release-finalization attempt used Windows' default text decoder on the UTF-8 guide and failed before producing the manifest. The following premature verifier invocation consequently had no release manifest. Explicit UTF-8 reading fixes the exporter; failed source is retained.
- A provisional package verification authenticated all 24,709 archive members but found a stale LaTeX hash after a concurrent final editorial change. That FAILED result is preserved. The stable final document is resealed before the final full check. It is not relabeled PASS.
- Early malformed orchestration/patch submissions were rejected before execution or rejected by patch validation; they did not change scientific files.

The final validation receipt records completed checks separately. All scientific exclusions, failed native runs and original custody limitations remain unchanged.
