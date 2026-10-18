# Reproduce the bounded calculations

The [Version 3 technical note](../paper/spin10_pq_technical_note.pdf) reports evidence through source checkpoint `22709b33f20484efe16eb4c3592d690c8e0650f3`. The original public note is preserved in [paper/archive](../paper/archive/). The new source update retains the unchanged original archives and overlays new or changed evidence. Publication changes no scientific authority or acceptance.

## Check the package first

From the repository root:

```sh
python -B reproducibility/verify_package.py
```

This reads every release file and every member of the base and update archives, compares inventories, lengths and SHA-256 hashes, and checks the current source-view references. Success authenticates packaged bytes. It does not execute calculations, prove a scientific derivation or infer human acceptance.

## Read the current results

The final [handoff V253](RESEARCH_EXECUTION_HANDOFF_V253.md) gives the frozen continuation context. The [reference-symbol test](calculations/canonical_so10_ub12_reference_symbol/RESULT.md) verifies weighted principal invertibility; the [local covariant reference witness](calculations/canonical_so10_local_covariant_reference_witness/RESULT.md) constructs one explicit local member. This does not establish the actual heat-regulated UV/subtraction correspondence or full quantum consistency.

These original files are directly browsable, alongside their frozen contracts, actual receipts and successful/failed captures:

| Question | Result and input |
| --- | --- |
| Earlier +0.10486 Higgs point | [Positive quartic](calculations/canonical_so10_positive_higgs/RESULT.md), [point](calculations/canonical_so10_positive_higgs/POINT.json), and [subsequent tree perturbativity failure](calculations/canonical_so10_radial_input_control/RESULT.md) |
| Different exploratory point | [Joint local tests](calculations/canonical_so10_coherent_joint_witness/RESULT.md), [reduced frozen fixture](calculations/canonical_so10_coherent_joint_witness/POINT.json) |
| Complete classical contact bound | [Whole-operator upper bound ≤ 0.47004](calculations/canonical_so10_complete_contact_bound/RESULT.md) |
| Global quartic positivity | [Strict full-328-field certificate](calculations/canonical_so10_finite_full_bfb/RESULT.md) |
| Quantum-control warning | [Large complete selected singlet pole correction](calculations/canonical_so10_singlet_pole_control/RESULT.md), [local RG/log check](calculations/canonical_so10_singlet_pole_rg_check/RESULT.md) |
| Gauge matching at the older point | [One-loop diagnostic](calculations/canonical_so10_direct_gauge_matching/RESULT.md), [two-loop SM running](calculations/canonical_so10_direct_gauge_next_order/RESULT.md), [missing finite two-loop boundary](calculations/canonical_so10_direct_two_loop_heavy_threshold/RESULT.md) |
| Gauge and PQ structure | [Local representation anomaly traces](calculations/canonical_so10_local_gauge_anomaly/RESULT.md), [PQ coefficients and conditional wall count](calculations/canonical_so10_pq_anomaly_screen/RESULT.md) |
| Conditional quantum background extension | [Actual commutation and conditional local uniqueness](calculations/canonical_so10_ub12_background_locality/RESULT.md) |

The exploratory fixture is specified by reduced rational coordinates plus unchanged inherited action inputs and dependent stationarity/weak-root maps. Its POINT.json alone is not a complete standalone numeric potential. Use its RECORD.md, sources and bound prerequisites in the assembled source tree. The original result reports describe their own chronological knowledge; later certificates and warnings appear in separate records. A false “full BFB” flag in an earlier necessary-set receipt is not a contradiction of the subsequent separate BFB certificate.

## Assemble the source/evidence tree

The unchanged **base** contains 15,909 selected source files at original checkpoint `8a07e12f61350e1c6f488d0c52d7d23c676e156c`:

- [Base part 1](spin10_pq_source_snapshot_v1_part1.zip).
- [Base part 2](spin10_pq_source_snapshot_v1_part2.zip).

The [Version 2 source manifest](../provenance/source_manifest_v2.json) lists every **update** archive, exact members, the complete current source view and any removed paths. Each ZIP is an ordinary independent archive. Extract both base parts into a new directory, then extract every update archive into that SAME directory, allowing its named replacements. Remove only paths explicitly listed in removed_paths if you need an exact current source view. Base-only historical files otherwise remain archival residue. A short extraction path is useful on Windows.

For exact assembly, an optional standard-library helper verifies the whole release first and requires a new, empty destination:

```sh
python -B reproducibility/assemble_source.py C:/spin10-source
```

The update exports all tracked source paths at the frozen checkpoint; it includes the completed reference-symbol and explicit local-reference witness; work after the frozen checkpoint is excluded. Broad provenance and intermediate records are retained to avoid omitting dependencies; archive inclusion is not endorsement of every historical claim.

The separate `external/research-control-records/` namespace contains referenced external preparation/verifier/control folders, including preserved failures. Its manifest records the original absolute paths. Historical policy bytes are stored separately under `historical/<commit>/`. Neither namespace substitutes its files for live policy or silently rewrites historical manifests.

The base and current manifests preserve original source bytes, hashes and Git blob IDs. Existing worktree/Git line-ending differences are explicitly recorded. Original receipts retain machine-specific absolute paths and read guards; some historical harnesses require a declared relocation plan to replay on another machine. Do not edit frozen inputs or bypass integrity checks to make an old driver pass.

### Update archive downloads

- [spin10_pq_source_update_v2_part1.zip](spin10_pq_source_update_v2_part1.zip).
- [spin10_pq_source_update_v2_part2.zip](spin10_pq_source_update_v2_part2.zip).
- [spin10_pq_source_update_v2_history.zip](spin10_pq_source_update_v2_history.zip).

- [spin10_pq_source_update_v2_checkpoint.zip](spin10_pq_source_update_v2_checkpoint.zip).

## Environment and short replays

The original core environment used Python 3.10.11 and the versions in [requirements-core.txt](requirements-core.txt):

```sh
python -m pip install -r reproducibility/requirements-core.txt
python -B reproducibility/calculations/canonical_so10_scalar_reconstruction/verify_pq.py
python -B reproducibility/calculations/canonical_so10_direct_gauge_next_order/independent_replay.py
```

The first replay checks charge arithmetic, not representation multiplicities. The second reproduces the older frozen gauge residual with another integration coordinate. It does not calculate thresholds at the new exploratory point. Optional selected tensor replays use Julia 1.12.6; some audit programs need jsonschema or python-flint. Inspect each record's actual dependency and resource requirements.

From the assembled source tree, follow the RECORD.md for a substantive replay. Scientific scripts can write outputs or caches and should run in a disposable copy. Do not overwrite frozen evidence, rerun an optimizer unnecessarily or infer a validated point from a solver success flag. The original Hessian/representation proofs and other inherited dependencies are explicitly reused where recorded.

## What was checked for this update

The [claim authentication](../provenance/claim_authentication_v2.json) checks the selected completed receipts and their byte, input, external and supplemental SHA-256 maps. Historical policy hashes are authenticated at their recorded Git objects, separately from current AGENTS.md. The [publication validation](../provenance/packaging_validation_v2.json) records package/member checks, actual short replays, PDF compilation and visual inspection, checks omitted and preserved packaging failures.

No expensive Hessian, complete contact, quartic, singlet-pole or quantum calculation was repeated for publication. Receipt authentication is not a fresh scientific replay. Full original Git history is absent: historical Git-custody checks cannot be recreated from this flat export alone. Original custody exit 2/seven unresolved references remains unresolved, not PASS.

The archived project_state.json remains a fixed original input at version 113. It creates no second live authority ledger. Earlier failed benchmarks, closed parameter families, blocked quantum stages and paused flavor retain their classifications.

The new point's global quartic and contact certificates are classical, point-specific results. Its large singlet correction is a warning against a small-correction expansion, not a reliable predicted mass or an exclusion of every input prescription. Preferred vacuum, quantum control, complete gauge/IR scattering, finite thresholds and realistic phenomenology remain open. Different routes share assumptions, inputs, software and an AI-assisted solo analyst; they are not external verification.
