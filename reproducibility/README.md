# Reproduce the bounded calculations

The [Version 4.1 technical note](../paper/spin10_pq_technical_note.pdf) reports evidence through source checkpoint `7562f42c14ef1ab5a946fbfc4534509f3378c76b`. The earlier public notes are preserved in [paper/archive](../paper/archive/). The new source update retains the unchanged original archives and overlays new or changed evidence. Publication changes no scientific authority or acceptance.

## Check the package first

From the repository root:

```sh
python -B reproducibility/verify_package.py
```

This reads every release file and every member of the base and update archives, compares inventories, lengths and SHA-256 hashes, and checks the current source-view references. Success authenticates packaged bytes. It does not execute calculations, prove a scientific derivation or infer human acceptance.

## Read the current results

The final [handoff V421](RESEARCH_EXECUTION_HANDOFF_V421.md) records the current frozen continuation. State version 113 and formal authority 34/39 are unchanged. The current completed results include formal one-loop UV/normalization constructions, compact-domain graded causal/QAP work, additional singlet momentum diagnostics, and four scoped two-loop primitive amplitude families. Full finite C1, unification and physical viability remain unresolved.

The C1 program uses the older positive-Higgs point (hash 476645438ea8a7ada42fea90e80174b772d45ce3e729d013d134e9848950c816) and its specified background-field Feynman-gauge reference. The newer classical witness and its singlet diagnostics use different scalar inputs. The 643-field formal nonlinear-source construction is another precisely defined computational scope. Do not transfer results or assume equivalence between them.

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


| New completed scope | Result |
| --- | --- |
| Same-point singlet momentum response | [1.94% and 20.27% combinations](calculations/canonical_so10_singlet_momentum_shape/RESULT.md), [two-loop Yukawa input carrier](calculations/canonical_so10_singlet_two_loop_input_closure/RESULT.md), [scalar-weakening tradeoff](calculations/canonical_so10_scalar_gauge_homothety/RESULT.md) |
| Complete formal one-loop UV | [Slavnov identity](calculations/canonical_so10_bv_uv_residue_bridge/RESULT.md), [physical counterterm span](calculations/canonical_so10_physical_counterterm_span/RESULT.md), [strict one-loop acceptance distinction](calculations/canonical_so10_one_loop_acceptance_reconciliation/RESULT.md) |
| Local causal/QAP and finite normalization | [Graded QAP](calculations/canonical_so10_graded_causal_qap/RESULT.md), [joint normalization/reference member](calculations/canonical_so10_background_reference_normalization/RESULT.md), [local cutoff/source-functional boundary](calculations/canonical_so10_local_cutoff_comparison/RESULT.md) |
| Scoped VVVV / VVSS amplitudes | [Regulated quartic-vector coefficient](calculations/canonical_so10_vector_quartic_primitive/RESULT.md), [complete IR subtraction](calculations/canonical_so10_vector_quartic_ir_matching/RESULT.md), [mixed quartic finite family](calculations/canonical_so10_vector_scalar_quartic/RESULT.md) |
| Scoped VSS / ghost–scalar amplitudes | [All-sector common-scale VSS](calculations/canonical_so10_scalar_current_vss_assembly/RESULT.md), [ordered ghost charge operators](calculations/canonical_so10_ghost_scalar_charge_kernel/RESULT.md), [complete ghost–scalar primitive](calculations/canonical_so10_ghost_scalar_sunset/RESULT.md) |

The exploratory fixture is specified by reduced rational coordinates plus unchanged inherited action inputs and dependent stationarity/weak-root maps. Its POINT.json alone is not a complete standalone numeric potential. Use its RECORD.md, sources and bound prerequisites in the assembled source tree. The original result reports describe their own chronological knowledge; later certificates and warnings appear in separate records. A false “full BFB” flag in an earlier necessary-set receipt is not a contradiction of the subsequent separate BFB certificate.

## Assemble the source/evidence tree

The unchanged **base** contains 15,909 selected source files at original checkpoint `8a07e12f61350e1c6f488d0c52d7d23c676e156c`:

- [Base part 1](spin10_pq_source_snapshot_v1_part1.zip).
- [Base part 2](spin10_pq_source_snapshot_v1_part2.zip).

The [Version 3 source manifest](../provenance/source_manifest_v3.json) binds the unchanged v2 manifest and lists the new update archives and complete current source view. The v2 manifest binds the original v1 base manifest. Every old archive/manifest is retained. Each ZIP is an ordinary independent archive. Extract both base parts into a new directory, then extract all v2 updates followed by all v3 updates into that SAME directory, allowing its named replacements. Remove only paths explicitly listed in removed_paths if you need an exact current source view. Base-only historical files otherwise remain archival residue. A short extraction path is useful on Windows.

For exact assembly, an optional standard-library helper verifies the whole release first and requires a new, empty destination:

```sh
python -B reproducibility/assemble_source.py C:/spin10-source
```

The update exports all tracked source paths at the frozen checkpoint; it includes the completed evidence through V421; work after the frozen checkpoint is excluded. Broad provenance and intermediate records are retained to avoid omitting dependencies; archive inclusion is not endorsement of every historical claim.

The separate `external/research-control-records/` namespace contains referenced external preparation/verifier/control folders, including preserved failures. Its manifest records the original absolute paths. Historical policy bytes are stored separately under `historical/<commit>/`. Neither namespace substitutes its files for live policy or silently rewrites historical manifests.

The base and current manifests preserve original source bytes, hashes and Git blob IDs. Existing worktree/Git line-ending differences are explicitly recorded. Original receipts retain machine-specific absolute paths and read guards; some historical harnesses require a declared relocation plan to replay on another machine. Do not edit frozen inputs or bypass integrity checks to make an old driver pass.

### Update archive downloads

- [spin10_pq_source_update_v2_part1.zip](spin10_pq_source_update_v2_part1.zip).
- [spin10_pq_source_update_v2_part2.zip](spin10_pq_source_update_v2_part2.zip).
- [spin10_pq_source_update_v2_history.zip](spin10_pq_source_update_v2_history.zip).

- [spin10_pq_source_update_v2_checkpoint.zip](spin10_pq_source_update_v2_checkpoint.zip).

### New v3 update archives

- [spin10_pq_source_update_v3_part1.zip](spin10_pq_source_update_v3_part1.zip).
- [spin10_pq_source_update_v3_part2.zip](spin10_pq_source_update_v3_part2.zip).
- [spin10_pq_source_update_v3_part3.zip](spin10_pq_source_update_v3_part3.zip).
- [spin10_pq_source_update_v3_part4.zip](spin10_pq_source_update_v3_part4.zip).
- [spin10_pq_source_update_v3_history.zip](spin10_pq_source_update_v3_history.zip).

## Environment and short replays

The original core environment used Python 3.10.11 and the versions in [requirements-core.txt](requirements-core.txt):

```sh
python -m pip install -r reproducibility/requirements-core.txt
python -B reproducibility/calculations/canonical_so10_scalar_reconstruction/verify_pq.py
python -B reproducibility/calculations/canonical_so10_direct_gauge_next_order/independent_replay.py
```

The first replay checks charge arithmetic, not representation multiplicities. The second reproduces the older frozen gauge residual with another integration coordinate. It does not calculate thresholds at the new exploratory point. Optional selected tensor replays use Julia 1.12.6; some audit programs need jsonschema or python-flint. Inspect each record's actual dependency and resource requirements.

From the assembled source tree, follow the RECORD.md for a substantive replay. Scientific scripts can write outputs or caches and should run in a disposable copy. Do not overwrite frozen evidence, rerun an optimizer unnecessarily or infer a validated point from a solver success flag. The original Hessian/representation proofs and other inherited dependencies are explicitly reused where recorded.

## Closed portable classical pilot

Copy the entire [portable_dh_v1 directory](portable_dh_v1/README.md) elsewhere, including its compressed data and manifest. In that copy run both commands:

```sh
python -I -S -B run.py --method slot
python -I -S -B run.py --method left
```

This pilot requires **Python 3.11+**, independently of the older Python 3.10 scalar environment. It uses the standard library, relative inputs and exact arithmetic. Each method computes all 99,256 positions of the retained classical gauge-fixing/Hessian identity before reading the expected table. It does not reproduce the scalar mass spectrum, full quantum action, upstream physical assumptions or E5/A5. Both methods are executed in an isolated copy for this release.

## What was checked for this update

The [claim authentication](../provenance/claim_authentication_v3.json) checks the selected completed receipts and their byte, input, external and supplemental SHA-256 maps. Historical policy hashes are authenticated at their recorded Git objects, separately from current AGENTS.md. The [original publication validation](../provenance/packaging_validation_v3.json) records package/member checks, actual short replays, PDF compilation and visual inspection, checks omitted and preserved packaging failures. The [Version 4.1 editorial review](../provenance/editorial_review_v1.json) records the wording correction, current-status comparison and PDF checks; it reuses the unchanged prior scientific replay evidence.

No expensive Hessian, complete contact, quartic, singlet-pole or quantum calculation was repeated for publication. Receipt authentication is not a fresh scientific replay. Full original Git history is absent: historical Git-custody checks cannot be recreated from this flat export alone. Original custody exit 2/seven unresolved references remains unresolved, not PASS.

The archived project_state.json remains a fixed original input at version 113. It creates no second live authority ledger. Earlier failed benchmarks, closed parameter families, blocked quantum stages and paused flavor retain their classifications.

The singlet momentum combinations have different local-subtraction sensitivity from the retained 140% pole shift. The two-loop internal Yukawa carrier supplies a real missing input; no scalar-only truncation is promoted to a complete two-loop error bound. The four primitive amplitude families have different UV/IR completion scopes, not a common fully renormalized threshold status.

The new point's global quartic and contact certificates are classical, point-specific results. Its large singlet correction is a warning against a small-correction expansion, not a reliable predicted mass or an exclusion of every input prescription. Preferred vacuum, quantum control, complete gauge/IR scattering, finite thresholds and realistic phenomenology remain open. Different routes share assumptions, inputs, software and an AI-assisted solo analyst; they are not external verification.

Version 4.1 is an editorial clarification of Version 4: the mismatch and singlet cut are described as calculated/computed, without an experimental connotation. Scientific results and the frozen checkpoint are unchanged. The original Version 4 note is preserved in paper/archive; prior packaging receipts remain historical evidence.
