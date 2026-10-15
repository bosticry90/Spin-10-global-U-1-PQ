# Reproduce the bounded calculations

The [technical note](../paper/spin10_pq_technical_note.pdf) describes the scientific scopes. This directory provides the original calculation programs, inputs, evidence, and a byte manifest. This is a source/evidence snapshot, not a replacement scientific authority ledger.

## Start with the package check

Clone or download this repository. From its root, run:

```sh
python -B reproducibility/verify_package.py
```

This checks the release files and every member of the two source archives against the recorded SHA-256 hashes. It reads files only. A successful package check authenticates bytes; it does not execute or scientifically accept any calculation.

## Core scalar and gauge programs

The [calculations directory](calculations/) is directly browsable. It includes frozen exact scalar points, result records, and their local dependencies. For the standard scalar/gauge environment, use Python 3.10 and install:

```sh
python -m pip install -r reproducibility/requirements-core.txt
```

The versions in that file match the recorded environment. Julia 1.12.6 is optional for selected separate tensor replays. The result records explain each method's shared-input and software limitations.

From the repository root, two short, read-only entry points are:

```sh
python -B reproducibility/calculations/canonical_so10_scalar_reconstruction/verify_pq.py
python -B reproducibility/calculations/canonical_so10_direct_gauge_next_order/independent_replay.py
```

The first checks the stated charge arithmetic; it does not prove representation multiplicities. The second reproduces the frozen inverse-coupling diagnostic using a different integration coordinate and checks it against the stored result. Its fitted numbers remain diagnostics, not physical parameters.

For substantive scalar reproduction, read these records before running their commands:

- [Complete scalar definition](calculations/canonical_so10_scalar_reconstruction/RESULT_V2.md).
- [Stage 1 and initial Stage 2](calculations/canonical_so10_scalar_benchmark/RESULT.md).
- [Failed initial relaxed quartic](calculations/canonical_so10_light_higgs_quartic/RESULT.md).
- [Later positive-quartic point](calculations/canonical_so10_positive_higgs/RESULT.md) and its [exact point](calculations/canonical_so10_positive_higgs/POINT.json).
- [Direct one-loop gauge matching](calculations/canonical_so10_direct_gauge_matching/RESULT.md).
- [Two-loop SM running with one-loop heavy matching](calculations/canonical_so10_direct_gauge_next_order/RESULT.md).
- [Missing finite two-loop heavy boundary](calculations/canonical_so10_direct_two_loop_heavy_threshold/RESULT.md).

An example positive-point replay is:

```sh
python -B reproducibility/calculations/canonical_so10_positive_higgs/verify_exact_point.py
```

Some other scripts write derived results or caches. Use a disposable checkout for those runs, preserve the supplied inputs, and do not confuse an optimizer flag with a validated point. Full Hessian, quartic, and quantum replays can be expensive. No optimizer search is needed to read or authenticate the frozen evidence.

## Supporting symmetry and quantum evidence

The original protected-input and evidence manifests have a substantial dependency chain. All selected bytes, including historical failed and blocked records, are retained in two ordinary independent ZIP archives:

- [Source snapshot, part 1](spin10_pq_source_snapshot_v1_part1.zip).
- [Source snapshot, part 2](spin10_pq_source_snapshot_v1_part2.zip).

Extract **both** into the same new directory, such as `reproducibility/source/`, preserving the stored relative paths. There is no overlap between their file inventories. Together they contain the selected source/evidence tree. A short extraction path is useful on Windows; some original frozen filenames are long.

The [source manifest](../provenance/source_manifest_v1.json) identifies every file, its archive, exact SHA-256, and original Git blob. The exporter preserves the existing worktree bytes. Where Git and the worktree already differed solely in line endings, that fact is recorded rather than silently normalizing an evidence file.

Within the extracted tree, the note's supporting records include:

```text
tools/two_loop_qft_compiler_v1/LAYER5B_M05_M08_RESULT.md
tools/two_loop_qft_compiler_v1/uvp_m06_evidence.json
tools/two_loop_qft_compiler_v1/uvp_m07_evidence.json
tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/A10_PHYSICAL_ACTION_RECONCILIATION_RESULT.md
tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/A10_E5_AUXILIARY_VERTEX_RESULT.md
```

The archive retains original result labels, contracts, primary/replay outputs, controls, receipts, and byte bindings. Some original audit drivers use additional `jsonschema` or `python-flint` libraries; inspect their recorded dependencies before an expensive replay. The current packaging interpreter had jsonschema 4.26.0 and python-flint 0.9.0, but that is not a claim that every historical calculation used those versions.

The archive includes original provenance documents where required by byte bindings. Those historical instructions and broader records do not add claims to this standalone note or authorize resuming a scientific workflow.

## Limits of this publication

- The source snapshot is anchored to local source commit `8a07e12f61350e1c6f488d0c52d7d23c676e156c`; it does not include the original Git history.
- Original custody checks that inspect historical Git objects cannot be reconstructed from a flat export alone. Seven original unresolved references remain unresolved; custody is not a global PASS.
- The archived `project_state.json` is a fixed original input. Publishing it creates no second live scientific authority and makes no acceptance decision.
- Packaging checks did not repeat the 35-block Hessian, relaxed-quartic, or expensive quantum-pole computations. The [packaging validation record](../provenance/packaging_validation_v1.json) lists the actual executed checks.
- The positive-quartic point is a local tree-level result. Global stability, loop control, complete quantum consistency, gauge unification, and phenomenology remain open.

The [snapshot metadata](../provenance/snapshot_metadata_v1.json) records provenance and shared dependencies. The technical note was corrected before publication to include the later positive-quartic point and to identify it as the spectrum used in gauge matching; the earlier failed tuning remains explicit.
