"""Freeze and review the V1164 evidence in the active D: workspace."""

import ast
import json
import os
import subprocess
import sys
import threading
import time
from hashlib import sha256
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONTROL = Path("D:/Codex-Research/ToE-Next/research-control-records/e5-direct-unmarked-ward-wick-v1-2026-11-09")
PK = ROOT / "tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1"
BASE = "c5202b70105ad496bf863a249c5c750618fb1327"
NAV = ["README.md", "docs/COMMON_RESTORATION_CAMPAIGN_V1.md", "docs/RESEARCH_EXECUTION_HANDOFF_V1164.md"]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def save(name, data):
    raw = (json.dumps(data, sort_keys=True) + "\n").encode()
    if len(raw) > 8 * 1024**2:
        name += ".COMPLETE_OVERFLOW_NOTPASS"
    for folder in (HERE, CONTROL):
        with (folder / name).open("xb") as f:
            f.write(raw)
    assert len(raw) <= 8 * 1024**2


def prepare(phase):
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    assert not git("diff", "--cached", "--name-only")
    if phase == "native":
        assert not git("diff", "--name-only", "HEAD")
        CONTROL.mkdir(exist_ok=False)
        with (CONTROL / "old_git_tree.txt").open("xb") as f:
            f.write(git("ls-tree", "-r", "HEAD"))
        snapshots = ("RECORD.md", "PROOF.md", "direct_unmarked_ward_wick.py", "execute.py")
        owners = {
            "scalar_source_transport_v2": ("source_transport.py", "PROOF.md", "result.json", "validation_receipt.json"),
            "linear_nonminimal_transport_v1": ("nonminimal_transport.py", "PROOF.md", "validation_receipt.json"),
            "joint_nonlinear_source_span_v2": ("joint_nonlinear.py", "PROOF.md", "validation_receipt.json"),
            "ordinary_derivative_ghost_companion_v1": ("PROOF.md", "result.json", "validation_receipt.json"),
            "light_edge_metric_completion_v1": ("PROOF.md", "result.json", "validation_receipt.json"),
            "joint_contact_gauge_square_v1": ("PROOF.md", "result.json", "validation_receipt.json"),
            "isolated_contact_metric_defect_v1": ("PROOF.md", "result.json", "validation_receipt.json"),
            "derivative_ghost_mass_support_v1": ("PROOF.md", "validation_receipt.json"),
            "light_antighost_contact_pair_v1": ("PROOF.md", "result.json", "validation_receipt.json"),
            "regulator_free_inverse_g1_recovery_v1": ("PROOF.md", "native_inverse.json.gz",
                                                     "replay_inverse.json.gz", "validation_receipt.json"),
            "forced_gauge_fixing_companion_v1": ("PROOF.md", "result.json", "validation_receipt.json"),
            "local_ghost_compensation_v1": ("PROOF.md", "validation_receipt.json"),
            "gauge_scalar_seagull_residue_v1": ("seagull_residue.py", "validation_receipt.json"),
            "unprobed_compact_all_coupling_v1": (
                "native_full_current.json.gz", "replay_full_current.json.gz", "validation_receipt.json"),
            "physical_current_input_recovery_g1_v1": (
                "PROOF.md", "validation_receipt.json", "native_v2_coefficients.json.gz", "replay_v4_coefficients.json.gz"),
        }
        owners.update({'mixed_gauge_source_triangle_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'light_edge_metric_completion_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'combined_gauge_color_transport_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'regulator_free_inverse_g1_recovery_v1': ['PROOF.md', 'native_inverse.json.gz', 'replay_inverse.json.gz', 'validation_receipt.json']})
        owners.update({'lower_gauge_source_companion_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'compact_mixed_source_transport_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'heat_mellin_matching': ['DERIVATION.md']})
        owners.update({'lower_gauge_source_companion_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'background_seagull_contacts_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'ordinary_scalar_bubble_span_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'linear_nonminimal_transport_v1': ['PROOF.md', 'validation_receipt.json'], 'lower_gauge_source_companion_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'mixed_scalar_color_companion_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'linked_scalar_kinetic_bubble_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'regulator_free_inverse_g1_recovery_v1': ['PROOF.md', 'native_inverse.json.gz', 'replay_inverse.json.gz', 'validation_receipt.json'], 'heat_mellin_matching': ['DERIVATION.md']})
        owners.update({'ordinary_ghost_kinetic_companion_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'lower_gauge_source_companion_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'mixed_scalar_color_companion_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'scalar_ghost_reference_weights_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'separated_scalar_triangle_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'mass_tag_transport_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'joint_contact_gauge_square_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'mixed_gauge_source_triangle_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'mixed_scalar_color_companion_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'compact_plateau_restriction_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'master_mass_tangent_v2': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'compact_mixed_reference_span_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'lower_gauge_source_companion_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'compact_scalar_reference_complement_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'light_mixed_reference_completion_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'massive_scalar_insertion_transport_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'scalar_plateau_sector_transport_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'linear_nonminimal_transport_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'mixed_first_switch_carrier_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'linked_scalar_kinetic_bubble_v1': ['linked_scalar.py', 'PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'linked_scalar_first_switch_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'massive_scalar_insertion_transport_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'scalar_sector_finite_match_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'physical_current_input_recovery_g1_v1': ['PROOF.md', 'validation_receipt.json', 'native_v2_coefficients.json.gz', 'replay_v4_coefficients.json.gz', 'native_v2_action.json.gz', 'replay_v4_action.json.gz'], 'graded_causal_qap': ['DERIVATION.md', 'RESULT.md'], 'causal_wick_bridge': ['DERIVATION.md', 'RESULT.md']})
        owners.update({'scalar_causal_conversion_check_v3': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'mixed_gauge_source_triangle_v1': ['mixed_triangle.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'mixed_first_switch_carrier_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'gauge_plateau_sector_transport_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'scalar_causal_conversion_check_v3': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'scalar_sector_finite_match_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'scalar_ghost_reference_weights_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'broken_singlet_mass_contrast_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'ghost_switch_transition_v1': ['PROOF.md', 'validation_receipt.json'], 'collapsed_profile_heat_offset_v2': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'auxiliary_switch_inverse_pair_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'gauge_plateau_sector_transport_v2': ['gauge_plateau.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'compact_mixed_source_transport_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'gauge_first_switch_rank_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'marked_regulator_parent_g1_v1': ['PROOF.md', 'validation_receipt.json'], 'gaussian_current_reduction_g1_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'auxiliary_regulator_switch_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'gauge_first_switch_rank_v1': ['first_switch_rank.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'ghost_switch_transition_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'gauge_switch_cubic_profile_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'ghost_source_finite_comparison': ['DERIVATION.md', 'RESULT.md'], 'internal_gauge_switch_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'ghost_source_local_width_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'gauge_first_switch_rank_v1': ['first_switch_rank.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'gauge_plateau_sector_transport_v2': ['gauge_plateau.py', 'PROOF.md', 'validation_receipt.json'], 'auxiliary_regulator_switch_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'regulator_second_switch_profile_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'gauge_switch_cubic_profile_v2': ['cubic_switch_profile.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'gauge_first_switch_rank_v1': ['first_switch_rank.py', 'PROOF.md', 'validation_receipt.json'], 'gauge_plateau_sector_transport_v2': ['gauge_plateau.py', 'PROOF.md', 'validation_receipt.json']})
        owners.update({'regulator_cubic_switch_profile_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'lower_gauge_source_companion_v1': ['PROOF.md', 'validation_receipt.json'], 'ghost_source_local_width_v1': ['PROOF.md', 'validation_receipt.json'], 'heat_mellin_matching': ['DERIVATION.md', 'RESULT.md']})
        owners.update({'longitudinal_heat_transfer_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'auxiliary_regulator_switch_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'regulator_second_switch_profile_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'regulator_cubic_switch_profile_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'ghost_source_local_width_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'transverse_switch_support_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'longitudinal_heat_transfer_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'nonlinear_source_insertion_extension_v1': ['PROOF.md', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['PROOF.md', 'native_full_current.json.gz', 'replay_full_current.json.gz', 'validation_receipt.json'], 'heat_mellin_matching': ['DERIVATION.md', 'RESULT.md']})
        owners.update({'relative_profile_functional_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'current_background_reference_bridge_v1': ['PROOF.md', 'result_a.json', 'result_b.json', 'validation_receipt.json'], 'background_reference_normalization': ['DERIVATION.md', 'RESULT.md', 'validation_receipt_v6.json'], 'gauge_first_switch_rank_v1': ['first_switch_rank.py', 'validation_receipt.json']})
        owners.update({'background_profile_reference_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'compact_switched_master_domain_v1': ['PROOF.md', 'validation_receipt.json'], 'cartan_generator_residual_g1_v1': ['PROOF.md', 'v2_fixed_ward_and_old_affine_endpoints.json.gz', 'validation_receipt.json'], 'ghost_switch_transition_v1': ['PROOF.md', 'validation_receipt.json'], 'connected_marked_master_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'marked_profile_functional_v3': ['marked_profile_functional.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'marked_regulator_parent_g1_v1': ['PROOF.md', 'validation_receipt.json'], 'regulator_free_inverse_g1_recovery_v1': ['PROOF.md', 'native_inverse.json.gz', 'replay_inverse.json.gz', 'validation_receipt.json']})
        owners.update({'marked_regulator_profile_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'marked_profile_functional_v3': ['marked_profile_functional.py', 'PROOF.md', 'validation_receipt.json'], 'connected_marked_master_v1': ['PROOF.md', 'validation_receipt.json'], 'causal_one_loop_sewing': ['DERIVATION.md', 'RESULT.md', 'validation_receipt.json']})
        owners.update({'relative_profile_forest_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'joint_compact_background_geometric_v1': ['RESULT.md', 'validation_receipt.json'], 'current_background_reference_bridge_v1': ['PROOF.md', 'result_a.json', 'validation_receipt.json'], 'background_profile_reference_v2': ['PROOF.md', 'validation_receipt.json'], 'marked_profile_functional_v3': ['PROOF.md', 'validation_receipt.json'], 'marked_regulator_profile_v2': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'affine_profile_regulator_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'current_background_reference_bridge_v1': ['PROOF.md', 'result_a.json', 'result_b.json', 'validation_receipt.json'], 'background_profile_reference_v2': ['PROOF.md', 'validation_receipt.json'], 'heat_mellin_matching': ['DERIVATION.md']})
        owners.update({'covariant_profile_first_edge_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'ordered_multiheat_uv_log': ['DERIVATION.md', 'validation_receipt.json'], 'joint_born_ir_trace_domain': ['DERIVATION.md', 'validation_receipt.json'], 'current_background_reference_bridge_v1': ['PROOF.md', 'result_a.json', 'result_b.json', 'validation_receipt.json'], 'gauge_plateau_sector_transport_v2': ['gauge_plateau.py', 'validation_receipt.json']})
        owners.update({'covariant_relative_conversion_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'covariant_marked_regulator_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'broken_singlet_mass_contrast_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'transverse_scalar_mass_master_v3': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'explicit_contact_metric_v2': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'transverse_gauge_metric_master_v2': ['transverse_gauge_metric_master.py', 'PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'unequal_gauge_metric_master_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'covariant_marked_regulator_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'mixed_background_edge_finite_v1': ['mixed_background_edge_finite.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['native_full_current.json.gz', 'replay_full_current.json.gz', 'validation_receipt.json', 'PROOF.md']})
        owners.update({'background_ABB_finite_sum_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'background_ABB_geometric_cutoff_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'relative_profile_forest_v1': ['relative_profile_forest.py', 'PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'covariant_background_forest_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['native_full_current.json.gz', 'replay_full_current.json.gz', 'PROOF.md', 'validation_receipt.json']})
        owners.update({'local_affine_second_cutoff_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'connected_marked_master_v1': ['marked.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'augmented_metric_lift_v1': ['tensor_0.json.gz', 'tensor_6.json.gz', 'tensor_7.json.gz', 'validation_receipt.json'], 'joint_common_family_applicability_v1': ['native_complete_full_background_extension.json.gz', 'replay_complete_full_background_extension.json.gz', 'validation_receipt.json']})
        owners.update({'background_marked_connected_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'covariant_background_forest_v1': ['covariant_background_forest.py', 'PROOF.md', 'validation_receipt.json'], 'uncut_connected_infrared_v1': ['PROOF.md', 'RESULT.md', 'validation_receipt_v3.json'], 'uncut_vector_boundary_v1': ['PROOF.md', 'RESULT.md', 'validation_receipt_v2.json']})
        owners.update({'uncut_background_bridge_boundary_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'uncut_local_common_primitive_v1': ['PROOF.md', 'RESULT.md', 'validation_receipt.json']})
        owners.update({'uncut_background_core_boundary_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'compact_direct_overlap_v2': ['PROOF.md', 'RESULT.md', 'validation_receipt.json'], 'phi_switching_limit_v1': ['PROOF.md', 'RESULT.md', 'validation_receipt.json']})
        owners.update({'massive_background_feynman_boundary_v1': ['massive_background_feynman_boundary.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'unequal_gauge_metric_master_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'grouped_BB_feynman_boundary_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'ghost_mass_g4_pole': ['primary_v2_result.json', 'replay_v2_result.json', 'validation_receipt.json'], 'ghost_switch_transition_v1': ['PROOF.md', 'validation_receipt.json'], 'full_selected_causal_profile_v1': ['PROOF.md', 'validation_receipt.json'], 'compact_ghost_residue_pair_v2': ['PROOF.md', 'validation_receipt.json'], 'scalar_translation_completion_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_source_necessity_v2': ['yy_source_necessity.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'linear_nonminimal_transport_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_paired_master_transport_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'uncut_ghost_profile_v1': ['PROOF.md', 'validation_receipt.json'], 'causal_one_loop_sewing': ['DERIVATION.md', 'validation_receipt.json']})
        owners.update({'YY_Euler_contact_balance_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_source_necessity_v2': ['yy_source_necessity.py', 'PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_lower_master_contact_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'uncut_ghost_profile_v1': ['PROOF.md', 'ghost_profile.py', 'validation_receipt.json'], 'causal_wick_bridge': ['DERIVATION.md', 'RESULT.md', 'validation_receipt.json'], 'graded_causal_qap': ['DERIVATION.md', 'RESULT.md', 'validation_receipt_v2.json']})
        owners.update({'YY_differentiated_Euler_contact_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'full_selected_causal_profile_v1': ['PROOF.md', 'RESULT.md', 'validation_receipt.json'], 'compact_ghost_residue_pair_v2': ['PROOF.md', 'RESULT.md', 'validation_receipt.json']})
        owners.update({'YY_free_BRST_profile_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_lower_master_contact_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_paired_master_transport_v1': ['PROOF.md', 'validation_receipt.json'], 'gauge_scalar_seagull_residue_v1': ['PROOF.md', 'seagull_residue.py', 'validation_receipt.json']})
        owners.update({'YY_full_quartet_master_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'cartan_generator_residual_g1_v1': ['PROOF.md', 'v2_fixed_ward_and_old_affine_endpoints.json.gz', 'validation_receipt.json'], 'augmented_metric_lift_v1': ['PROOF.md', 'tensor_0.json.gz', 'validation_receipt.json'], 'current_causal_initial_dictionary_v1': ['PROOF.md', 'validation_receipt.json'], 'connected_marked_master_v1': ['PROOF.md', 'validation_receipt.json'], 'phi_switching_limit_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_first_marked_transfer_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_full_quartet_master_v1': ['PROOF.md', 'validation_receipt.json'], 'switched_massive_bridge_v1': ['PROOF.md', 'validation_receipt.json'], 'joint_internal_simple_switch_v1': ['PROOF.md', 'validation_receipt.json'], 'phi_switching_limit_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_compact_quartet_profile_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_first_marked_transfer_v1': ['PROOF.md', 'yy_first_marked_transfer.py', 'validation_receipt.json'], 'connected_marked_master_v1': ['PROOF.md', 'RESULT.md', 'validation_receipt.json']})
        owners.update({'YY_rooted_marked_Euler_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_compact_quartet_profile_v2': ['PROOF.md', 'validation_receipt.json'], 'ghost_two_color_transition_v2': ['PROOF.md', 'validation_receipt.json'], 'scalar_potential_residue_v2': ['PROOF.md', 'validation_receipt.json'], 'internal_gauge_switch_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_mass_difference_plateau_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_Euler_contact_balance_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_free_BRST_profile_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_mass_triangle_fusion_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'mass_tag_transport_v1': ['PROOF.md', 'RESULT.md', 'validation_receipt.json'], 'scalar_translation_completion_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_rooted_marked_Euler_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_anchored_mass_operator_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'derivative_kinetic_residue_v1': ['PROOF.md', 'RESULT.md', 'validation_receipt.json'], 'YY_full_quartet_master_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_kinetic_triangle_jet_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_compact_quartet_profile_v2': ['PROOF.md', 'validation_receipt.json'], 'phi_switching_limit_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_lower_master_contact_v2': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_anchored_switch_master_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_mass_difference_plateau_v1': ['PROOF.md', 'validation_receipt.json'], 'internal_massive_switch_v2': ['PROOF.md', 'validation_receipt.json'], 'exact_outer_ghost_group_v1': ['PROOF.md', 'validation_receipt.json'], 'causal_independent_transfer_v1': ['PROOF.md', 'validation_receipt.json'], 'dressed_exterior_profile_v1': ['PROOF.md', 'validation_receipt.json'], 'switched_massive_bridge_v1': ['PROOF.md', 'validation_receipt.json'], 'joint_internal_simple_switch_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_mass_causal_transfer_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_anchored_mass_operator_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_mass_triangle_fusion_v2': ['PROOF.md', 'validation_receipt.json'], 'mixed_w_transport_v1': ['PROOF.md', 'validation_receipt.json'], 'gauge_endpoint_profiles_v1': ['PROOF.md', 'validation_receipt.json'], 'ghost_internal_switch_sum_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_full_mass_profile_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_first_marked_transfer_v1': ['PROOF.md', 'yy_first_marked_transfer.py', 'validation_receipt.json'], 'dressed_exterior_profile_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_local_mass_probe_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_rooted_marked_Euler_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_first_marked_transfer_v1': ['PROOF.md', 'validation_receipt.json'], 'connected_marked_master_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_rooted_marked_Euler_t4_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'current_background_reference_bridge_v1': ['PROOF.md', 'validation_receipt.json'], 'background_residue_ward_v2': ['PROOF.md', 'validation_receipt.json'], 'scalar_source_transport_v2': ['source_transport.py', 'PROOF.md', 'validation_receipt.json'], 'gauge_scalar_seagull_residue_v1': ['seagull_residue.py', 'PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_fixed_flat_background_v1_v3': ['PROOF.md', 'result.json', 'validation_receipt.json', 'yy_fixed_flat_background.py'], 'background_seagull_contacts_v1': ['seagull_contacts.py', 'PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_ideal_gauge_background_v2': ['yy_ideal_gauge_background.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'seagull_forced_companions_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'maxwell_switch_companion_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_ideal_gauge_switch_v2': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_ideal_gauge_marked_ports_v1': ['yy_ideal_gauge_marked_ports.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_paired_master_transport_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_ideal_gauge_master_probe_v2': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_ideal_gauge_joint_rank_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'linear_nonminimal_transport_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_first_marked_transfer_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_ideal_scalar_source_rank_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'scalar_source_transport_v2': ['PROOF.md', 'result.json', 'validation_receipt.json', 'source_transport.py']})
        owners.update({'YY_ideal_source_nilpotency_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_source_necessity_v2': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_ideal_ghost_triangle_span_v2': ['yy_ideal_ghost_triangle_span.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_ideal_gauge_joint_rank_v1': ['yy_ideal_gauge_joint_rank.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_ideal_scalar_source_rank_v1': ['yy_ideal_scalar_source_rank.py', 'PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_joint_symbolic_log_rank_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_paired_master_transport_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_auxiliary_orbit_source_support_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_ideal_ghost_triangle_span_v2': ['yy_ideal_ghost_triangle_span.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'graded_causal_qap': ['DERIVATION.md', 'validation_receipt_v2.json']})
        owners.update({'YY_both_odd_triangle_image_v1': ['yy_both_odd_triangle_image.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_joint_symbolic_log_rank_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_ghost_spectral_image_v1': ['yy_ghost_spectral_image.py', 'PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_Sigma_null_spectral_rank_v1': ['yy_sigma_null_spectral_rank.py', 'PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_mixed_spectral_Ward_master_v1': ['yy_mixed_spectral_ward_master.py', 'PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_Sigma_active_mixed_witness_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_mixed_spectral_Ward_master_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_mixed_spectral_free_trace_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_mixed_spectral_Ward_master_v1': ['yy_mixed_spectral_ward_master.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_ghost_spectral_image_v1': ['yy_ghost_spectral_image.py', 'PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_alternate_common_log_ordinary_v1': ['yy_alternate_common_log_ordinary.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_both_odd_triangle_image_v1': ['yy_both_odd_triangle_image.py', 'PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_shared_marked_source_images_v1': ['yy_shared_marked_source_images.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'connected_marked_master_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_shared_low_proper_marked_transfer_v1': ['yy_shared_low_proper_marked_transfer.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_auxiliary_orbit_source_support_v1': ['yy_auxiliary_orbit_source_support.py', 'PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_shared_higher_proper_marked_transfer_v1': ['yy_shared_higher_proper_marked_transfer.py', 'PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_alternate_common_log_ordinary_v1': ['yy_alternate_common_log_ordinary.py', 'PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_shared_higher_marked_freedoms_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['PROOF.md', 'native_full_current.json.gz', 'replay_full_current.json.gz', 'validation_receipt.json'], 'compact_switched_master_domain_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_shared_low_compact_marked_transfer_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'connected_marked_master_v1': ['PROOF.md', 'marked.py', 'validation_receipt.json'], 'connected_compact_master_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'connected_marked_defect_pullback_v2': ['PROOF.md', 'validation_receipt.json'], 'YY_shared_low_compact_marked_transfer_v1': ['yy_shared_low_compact_marked_transfer.py', 'PROOF.md', 'validation_receipt.json'], 'YY_free_BRST_profile_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_linked_switch_ghost_trace_v1': ['yy_linked_switch_ghost_trace.py', 'PROOF.md', 'validation_receipt.json'], 'YY_shared_higher_marked_freedoms_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_trace_zero_ordinary_family_v1': ['yy_trace_zero_ordinary_family.py', 'PROOF.md', 'validation_receipt.json'], 'gauge_feynman_shear_v1': ['PROOF.md', 'validation_receipt.json'], 'connected_marked_master_v1': ['PROOF.md', 'marked.py', 'validation_receipt.json']})
        owners.update({'YY_separated_low_vector_root_v1': ['yy_separated_low_vector_root.py', 'PROOF.md', 'validation_receipt.json'], 'YY_trace_zero_ordinary_family_v1': ['yy_trace_zero_ordinary_family.py', 'PROOF.md', 'validation_receipt.json'], 'YY_shared_low_compact_marked_transfer_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_crossed_low_vector_lift_v1': ['yy_crossed_low_vector_lift.py', 'PROOF.md', 'validation_receipt.json'], 'physical_current_input_recovery_g1_v1': ['native_v2_action.json.gz', 'replay_v4_action.json.gz', 'PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_full_switch_low_connected_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_shared_higher_proper_marked_transfer_v1': ['yy_shared_higher_proper_marked_transfer.py', 'PROOF.md', 'validation_receipt.json'], 'connected_marked_defect_pullback_v2': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_higher_source_euler_bundle_v1': ['yy_higher_source_euler_bundle.py', 'PROOF.md', 'validation_receipt.json'], 'regulator_free_inverse_g1_recovery_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_crossed_low_vector_lift_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_higher_early_switch_mark_v3': ['yy_higher_early_switch_mark.py', 'PROOF.md', 'validation_receipt.json'], 'YY_crossed_low_vector_lift_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_higher_source_euler_bundle_v1': ['yy_higher_source_euler_bundle.py', 'PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_higher_internal_vector_euler_v1': ['yy_higher_internal_vector_euler.py', 'PROOF.md', 'validation_receipt.json'], 'YY_higher_early_switch_mark_v3': ['yy_higher_early_switch_mark.py', 'PROOF.md', 'validation_receipt.json'], 'YY_crossed_low_vector_lift_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_equal_profile_higher_root_v1': ['PROOF.md', 'validation_receipt.json'], 'connected_marked_master_v1': ['PROOF.md', 'validation_receipt.json'], 'connected_marked_defect_pullback_v2': ['PROOF.md', 'validation_receipt.json'], 'causal_one_loop_sewing': ['DERIVATION.md', 'validation_receipt.json'], 'graded_causal_qap': ['DERIVATION.md', 'validation_receipt_v2.json']})
        owners.update({'YY_higher_causal_target_taylor_v1': ['PROOF.md', 'validation_receipt.json'], 'causal_second_product': ['DERIVATION.md', 'validation_receipt_v2.json'], 'heat_mellin_matching': ['DERIVATION.md', 'validation_receipt.json'], 'regulator_free_inverse_g1_recovery_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_higher_early_switch_mark_v3': ['yy_higher_early_switch_mark.py', 'PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_higher_raw_rooted_bubble_v1': ['PROOF.md', 'validation_receipt.json'], 'nonlinear_source_insertion_extension_v1': ['PROOF.md', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['PROOF.md', 'validation_receipt.json'], 'heat_mellin_matching': ['DERIVATION.md', 'validation_receipt.json']})
        owners.update({'YY_higher_direct_regulator_clock_v1': ['PROOF.md', 'validation_receipt.json'], 'causal_wick_bridge': ['DERIVATION.md', 'RESULT.md', 'validation_receipt.json'], 'marked_regulator_profile_v2': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_higher_tadpole_regulator_dictionary_v2': ['PROOF.md', 'validation_receipt.json'], 'YY_equal_profile_higher_root_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_alternate_common_log_ordinary_v1': ['yy_alternate_common_log_ordinary.py', 'validation_receipt.json'], 'scalar_source_transport_v2': ['source_transport.py', 'validation_receipt.json'], 'physical_current_input_recovery_g1_v1': ['native_v2_coefficients.json.gz', 'replay_v4_coefficients.json.gz', 'PROOF.md', 'validation_receipt.json', 'native_v2_action.json.gz', 'replay_v4_action.json.gz', 'physical_v4.py']})
        owners.update({'YY_separated_scalar_second_root_v1': ['PROOF.md', 'RESULT.md', 'result.json', 'validation_receipt.json'], 'current_causal_initial_dictionary_v1': ['PROOF.md', 'validation_receipt.json'], 'connected_marked_defect_pullback_v2': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_separated_scalar_dictionary_transport_v1': ['PROOF.md', 'validation_receipt.json'], 'nonlinear_source_insertion_extension_v1': ['PROOF.md', 'validation_receipt.json'], 'connected_marked_master_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_paired_covariance_structural_v2': ['PROOF.md', 'RESULT.md', 'validation_receipt.json'], 'YY_equal_profile_higher_root_v1': ['yy_equal_profile_higher_root.py', 'PROOF.md', 'validation_receipt.json'], 'YY_ghost_spectral_image_v1': ['yy_ghost_spectral_image.py', 'PROOF.md', 'validation_receipt.json'], 'local_affine_second_cutoff_v1': ['PROOF.md', 'validation_receipt.json'], 'background_marked_connected_v1': ['PROOF.md', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['PROOF.md', 'native_full_current.json.gz', 'replay_full_current.json.gz', 'validation_receipt.json']})
        owners.update({'YY_neutral_center_background_lift_v1': ['PROOF.md', 'yy_neutral_center_background_lift.py', 'validation_receipt.json'], 'YY_equal_profile_higher_root_v1': ['PROOF.md', 'yy_equal_profile_higher_root.py', 'validation_receipt.json'], 'YY_crossed_low_vector_lift_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_higher_direct_regulator_clock_v1': ['yy_higher_direct_regulator_clock.py', 'validation_receipt.json'], 'covariant_background_forest_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_center_returning_ward_inventory_v1': ['PROOF.md', 'RESULT.md', 'result.json', 'validation_receipt.json'], 'affine_profile_regulator_v1': ['PROOF.md', 'validation_receipt.json'], 'covariant_marked_regulator_v1': ['PROOF.md', 'validation_receipt.json'], 'local_affine_second_cutoff_v1': ['PROOF.md', 'validation_receipt.json'], 'background_marked_connected_v1': ['PROOF.md', 'validation_receipt.json'], 'geometric_marked_contact_support_v1': ['PROOF.md', 'validation_receipt.json'], 'covariant_background_forest_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_geometric_finite_map_transport_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_center_returning_ward_inventory_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_crossed_low_vector_lift_v1': ['PROOF.md', 'validation_receipt.json'], 'physical_current_input_recovery_g1_v1': ['PROOF.md', 'native_v2_action.json.gz', 'replay_v4_action.json.gz', 'validation_receipt.json']})
        owners.update({'YY_single_mark_geometric_support_v2': ['PROOF.md', 'validation_receipt.json'], 'YY_center_returning_ward_inventory_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_neutral_center_background_lift_v1': ['yy_neutral_center_background_lift.py', 'PROOF.md', 'validation_receipt.json'], 'covariant_relative_conversion_v1': ['PROOF.md', 'validation_receipt.json'], 'mass_tag_transport_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_reference_spectator_agreement_v2': ['PROOF.md', 'validation_receipt.json'], 'YY_single_mark_geometric_support_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_center_returning_ward_inventory_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'connected_fixed_background_ward_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_higher_internal_vector_euler_v1': ['PROOF.md', 'validation_receipt.json'], 'connected_marked_defect_pullback_v2': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_separated_geometric_master_mark_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_center_returning_ward_inventory_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_reference_spectator_agreement_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_crossed_low_vector_lift_v1': ['PROOF.md', 'validation_receipt.json'], 'covariant_background_forest_v1': ['PROOF.md', 'validation_receipt.json'], 'causal_one_loop_sewing': ['DERIVATION.md', 'RESULT.md']})
        owners.update({'YY_four_cycle_homogeneous_moment_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_center_returning_ward_inventory_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'current_background_reference_bridge_v1': ['PROOF.md', 'validation_receipt.json'], 'covariant_marked_regulator_v1': ['PROOF.md', 'validation_receipt.json'], 'covariant_background_forest_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_four_cycle_homogeneous_moment_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_split_mixed_reference_contact_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_center_returning_ward_inventory_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_reference_spectator_agreement_v2': ['PROOF.md', 'validation_receipt.json'], 'causal_one_loop_sewing': ['DERIVATION.md', 'RESULT.md']})
        owners.update({'YY_four_cycle_balanced_port_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_split_mixed_reference_contact_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_neutral_center_background_lift_v1': ['yy_neutral_center_background_lift.py', 'PROOF.md', 'validation_receipt.json'], 'physical_current_input_recovery_g1_v1': ['PROOF.md', 'native_v2_action.json.gz', 'replay_v4_action.json.gz', 'validation_receipt.json'], 'mixed_background_edge_finite_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_four_cycle_maxwell_contact_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_equal_profile_higher_root_v1': ['yy_equal_profile_higher_root.py', 'PROOF.md', 'validation_receipt.json'], 'YY_trace_zero_ordinary_family_v1': ['yy_trace_zero_ordinary_family.py', 'PROOF.md', 'validation_receipt.json'], 'YY_higher_early_switch_mark_v3': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_higher_tadpole_regulator_dictionary_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_single_mark_geometric_support_v2': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_neutral_rank_two_rebase_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_equal_profile_higher_root_v1': ['yy_equal_profile_higher_root.py', 'PROOF.md', 'validation_receipt.json'], 'YY_higher_internal_vector_euler_v1': ['yy_higher_internal_vector_euler.py', 'PROOF.md', 'validation_receipt.json'], 'YY_higher_source_euler_bundle_v1': ['yy_higher_source_euler_bundle.py', 'PROOF.md', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['PROOF.md', 'native_full_current.json.gz', 'replay_full_current.json.gz', 'validation_receipt.json'], 'YY_reference_spectator_agreement_v2': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_neutral_rank_two_ordinary_W3_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_neutral_rank_two_rebase_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_equal_profile_higher_root_v1': ['yy_equal_profile_higher_root.py', 'PROOF.md', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_neutral_two_pair_ordinary_W3_v1': ['PROOF.md', 'result.json', 'yy_neutral_two_pair_ordinary_W3.py', 'validation_receipt.json'], 'YY_neutral_rank_two_rebase_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_neutral_rank_two_ordinary_W3_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_trace_zero_ordinary_family_v1': ['PROOF.md', 'yy_trace_zero_ordinary_family.py', 'validation_receipt.json'], 'YY_alternate_common_log_ordinary_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'unprobed_compact_all_coupling_v1': ['PROOF.md', 'RESULT.md', 'native_full_current.json.gz', 'replay_full_current.json.gz', 'validation_receipt.json'], 'YY_paired_covariance_structural_v2': ['PROOF.md', 'yy_paired_covariance_structural.py', 'result.json', 'validation_receipt.json'], 'YY_neutral_full_ideal_rank_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_three_row_paired_target_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_higher_source_euler_bundle_v1': ['PROOF.md', 'yy_higher_source_euler_bundle.py', 'result.json', 'validation_receipt.json'], 'YY_shared_marked_source_images_v1': ['PROOF.md', 'yy_shared_marked_source_images.py', 'validation_receipt.json'], 'YY_ideal_gauge_marked_ports_v1': ['yy_ideal_gauge_marked_ports.py', 'validation_receipt.json'], 'YY_ideal_ghost_triangle_span_v2': ['yy_ideal_ghost_triangle_span.py', 'validation_receipt.json']})
        owners.update({'YY_charged_source_ordinary_pair_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_crossed_low_vector_lift_v1': ['PROOF.md', 'yy_crossed_low_vector_lift.py', 'result.json', 'validation_receipt.json'], 'YY_reference_spectator_agreement_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_neutral_center_background_lift_v1': ['PROOF.md', 'yy_neutral_center_background_lift.py', 'validation_receipt.json']})
        owners.update({'YY_charged_crossed_reference_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_charged_source_ordinary_pair_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_neutral_two_pair_ordinary_W3_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_equal_profile_higher_root_v1': ['yy_equal_profile_higher_root.py', 'PROOF.md', 'validation_receipt.json'], 'YY_higher_internal_vector_euler_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_other_W_T3_proper_rows_v3': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_separated_low_vector_root_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_full_switch_low_connected_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_higher_internal_vector_euler_v1': ['PROOF.md', 'yy_higher_internal_vector_euler.py', 'result.json', 'validation_receipt.json'], 'YY_ghost_spectral_image_v1': ['yy_ghost_spectral_image.py', 'validation_receipt.json']})
        owners.update({'YY_charged_rebase_marked_gate_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_four_cycle_balanced_port_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_charged_crossed_reference_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_balanced_charged_pure_contact_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'covariant_background_forest_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'covariant_marked_regulator_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_charged_crossed_reference_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_pure_relative_reference_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_charged_rebase_marked_gate_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_split_mixed_reference_contact_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_four_cycle_maxwell_contact_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_charged_mixed_reference_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_balanced_charged_pure_contact_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_charged_crossed_reference_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_charged_common_trace_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_charged_mixed_reference_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_split_mixed_reference_contact_v1': ['PROOF.md', 'yy_split_mixed_reference_contact.py', 'validation_receipt.json'], 'covariant_background_forest_v1': ['PROOF.md', 'validation_receipt.json'], 'covariant_marked_regulator_v1': ['PROOF.md', 'validation_receipt.json'], 'heat_mellin_matching': ['DERIVATION.md', 'validation_receipt.json']})
        owners.update({'YY_regulated_mixed_endpoint_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_free_BRST_profile_v1': ['PROOF.md', 'yy_free_brst_profile.py', 'validation_receipt.json'], 'YY_charged_common_trace_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_reverse_endpoint_identity_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_regulated_mixed_endpoint_v2': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_complete_endpoint_traces_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_higher_source_euler_bundle_v1': ['PROOF.md', 'yy_higher_source_euler_bundle.py', 'validation_receipt.json'], 'YY_higher_internal_vector_euler_v1': ['PROOF.md', 'yy_higher_internal_vector_euler.py', 'validation_receipt.json'], 'YY_geometric_finite_map_transport_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_literal_cut_color_space_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_balanced_charged_pure_contact_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_source_and_pure_contact_support_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_polarized_endpoint_class_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_neutral_rank_two_ordinary_W3_v1': ['PROOF.md', 'yy_neutral_rank_two_ordinary_W3.py', 'validation_receipt.json']})
        owners.update({'YY_charged_mixed_master_companions_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_crossed_low_vector_lift_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_other_W_T3_proper_rows_v3': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_like_ghost_source_return_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_alternate_common_log_ordinary_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_ideal_ghost_triangle_span_v2': ['PROOF.md', 'validation_receipt.json'], 'physical_current_input_recovery_g1_v1': ['PROOF.md', 'validation_receipt.json', 'native_v2_action.json.gz', 'replay_v4_action.json.gz']})
        owners.update({'YY_proper_scalar_edge_support_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_charged_mixed_master_companions_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_charged_four_cycle_inventory_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_four_cycle_maxwell_contact_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_like_ghost_source_return_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_source_YM_BB_collapse_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_charged_mixed_master_companions_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_complete_B_euler_group_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_split_mixed_reference_contact_v1': ['PROOF.md', 'yy_split_mixed_reference_contact.py', 'validation_receipt.json'], 'YY_regulated_mixed_endpoint_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_charged_mixed_master_companions_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_differentiated_F_euler_v4': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_F_H_euler_closure_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_F_endpoint_allocation_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_charged_four_cycle_inventory_v2': ['PROOF.md', 'result.json', 'validation_receipt.json', 'yy_charged_four_cycle_inventory.py'], 'YY_like_ghost_source_return_v1': ['PROOF.md', 'result.json', 'validation_receipt.json', 'yy_like_ghost_source_return.py']})
        owners.update({'YY_H_mixed_support_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_charged_mixed_reference_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_higher_source_euler_bundle_v1': ['PROOF.md', 'yy_higher_source_euler_bundle.py', 'validation_receipt.json'], 'YY_higher_internal_vector_euler_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_like_ghost_normalization_tests_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_F_endpoint_allocation_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'causal_second_product': ['DERIVATION.md', 'validation_receipt_v2.json'], 'heat_mellin_matching': ['DERIVATION.md', 'validation_receipt.json'], 'collapsed_profile_heat_offset_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'relative_profile_functional_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_H_lower_tensor_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_H_mixed_support_v1': ['PROOF.md', 'result.json', 'validation_receipt.json', 'yy_H_mixed_support.py'], 'YY_reference_spectator_agreement_v2': ['PROOF.md', 'yy_reference_spectator_agreement.py', 'validation_receipt.json'], 'YY_charged_mixed_master_companions_v1': ['PROOF.md', 'yy_charged_mixed_master_companions.py', 'validation_receipt.json']})
        owners.update({'YY_all_mixed_ordered_phases_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_source_YM_BB_collapse_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_charged_mixed_master_companions_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_F_balanced_contact_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_free_BRST_profile_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_ideal_ghost_triangle_span_v2': ['PROOF.md', 'yy_ideal_ghost_triangle_span.py', 'validation_receipt.json'], 'graded_causal_qap': ['DERIVATION.md', 'validation_receipt_v2.json']})
        owners.update({'YY_H_ghost_composite_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_pure_relative_reference_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_split_mixed_reference_contact_v1': ['PROOF.md', 'yy_split_mixed_reference_contact.py', 'validation_receipt.json']})
        owners.update({'YY_H_ghost_reference_split_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_H_ghost_composite_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_F_balanced_contact_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_charged_mixed_master_companions_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_H_ghost_split_allocation_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_H_lower_tensor_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_geometric_finite_map_transport_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_H_ghost_lower_transfer_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_F_H_euler_closure_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_H_lower_tensor_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_H_ghost_lower_euler_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_H_ghost_split_allocation_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_H_ghost_composite_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_charged_crossed_reference_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_paired_center_split_v2': ['PROOF.md', 'result.json', 'validation_receipt.json', 'yy_paired_center_split.py']})
        owners.update({'YY_neutral_color_channels_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_H_ghost_lower_euler_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_H_ghost_lower_transfer_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_charged_crossed_reference_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_source_YM_BB_collapse_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_lower_HL_compact_balance_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_neutral_color_channels_v1': ['PROOF.md', 'result.json', 'validation_receipt.json', 'yy_neutral_color_channels.py'], 'YY_paired_center_split_v2': ['PROOF.md', 'result.json', 'validation_receipt.json', 'yy_paired_center_split.py']})
        owners.update({'YY_full_reverse_color_map_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_H_ghost_composite_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_H_mixed_support_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_reference_spectator_agreement_v2': ['PROOF.md', 'yy_reference_spectator_agreement.py', 'validation_receipt.json']})
        owners.update({'YY_full_reverse_euler_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_literal_cut_color_space_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_higher_early_switch_mark_v3': ['PROOF.md', 'result.json', 'validation_receipt.json', 'yy_higher_early_switch_mark.py']})
        owners.update({'YY_reverse_source_root_support_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_H_ghost_lower_euler_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_split_mixed_reference_contact_v1': ['PROOF.md', 'yy_split_mixed_reference_contact.py', 'validation_receipt.json']})
        owners.update({'YY_width_one_compact_euler_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_paired_covariance_structural_v2': ['PROOF.md', 'result.json', 'validation_receipt.json', 'yy_paired_covariance_structural.py'], 'YY_higher_early_switch_mark_v3': ['PROOF.md', 'validation_receipt.json', 'yy_higher_early_switch_mark.py'], 'connected_marked_defect_pullback_v2': ['PROOF.md', 'validation_receipt.json'], 'connected_marked_master_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_fifth_paired_marked_target_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_full_reverse_euler_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_full_reverse_color_map_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_reverse_width_quartic_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_width_one_compact_euler_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_F_balanced_contact_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_width_reference_five_cycle_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_fifth_paired_marked_target_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_neutral_two_pair_ordinary_W3_v1': ['PROOF.md', 'validation_receipt.json'], 'physical_current_input_recovery_g1_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_marked_cutoff_removal_bound_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_fifth_paired_marked_target_v1': ['PROOF.md', 'validation_receipt.json'], 'physical_current_input_recovery_g1_v1': ['PROOF.md', 'native_v2_action.json.gz', 'replay_v4_action.json.gz', 'validation_receipt.json']})
        owners.update({'YY_raw_critical_root_core_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'connected_marked_master_v1': ['PROOF.md', 'validation_receipt.json'], 'augmented_metric_lift_v1': ['PROOF.md', 'tensor_0.json.gz', 'validation_receipt.json']})
        owners.update({'YY_separated_first_raw_mark_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_fifth_paired_marked_target_v1': ['PROOF.md', 'result.json', 'validation_receipt.json']})
        owners.update({'YY_higher_raw_root_support_v1': ['PROOF.md', 'yy_higher_raw_root_support.py', 'validation_receipt.json'], 'YY_linked_switch_ghost_trace_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_full_switch_low_connected_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_lower_raw_transfer_moments_v4': ['PROOF.md', 'validation_receipt.json'], 'YY_raw_critical_root_core_v2': ['PROOF.md', 'yy_raw_critical_root_core.py', 'result.json', 'validation_receipt.json'], 'YY_width_reference_five_cycle_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_raw_marked_eta_square_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_higher_causal_target_taylor_v1': ['PROOF.md', 'validation_receipt.json'], 'connected_marked_defect_pullback_v2': ['PROOF.md', 'validation_receipt.json'], 'graded_causal_qap': ['DERIVATION.md', 'RESULT.md', 'validation_receipt_v2.json']})
        owners.update({'YY_width_one_compact_euler_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_H_ghost_lower_euler_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_H_ghost_lower_transfer_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_H_lower_tensor_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_geometric_finite_map_transport_v1': ['PROOF.md', 'validation_receipt.json'], 'connected_marked_master_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_width_compact_lower_companion_v3': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_auxiliary_orbit_source_support_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_linked_switch_ghost_trace_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_lower_source_companion_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'YY_higher_source_euler_bundle_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_higher_raw_rooted_bubble_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'YY_auxiliary_source_inverse_companion_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'causal_second_product': ['DERIVATION.md', 'validation_receipt_v2.json'], 'graded_causal_qap': ['DERIVATION.md', 'validation_receipt_v2.json']})
        owners.update({'YY_all_source_composite_collapse_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_width_compact_lower_companion_v3': ['PROOF.md', 'validation_receipt.json'], 'YY_raw_critical_root_core_v2': ['PROOF.md', 'yy_raw_critical_root_core.py', 'validation_receipt.json'], 'YY_lower_raw_transfer_moments_v4': ['PROOF.md', 'validation_receipt.json']})
        owners.update({})
        owners.update({'ghost_one_coupling_torsion_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_g0_affine_ward_gauge_source_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'uncut_local_common_primitive_v1': ['PROOF.md', 'validation_receipt.json'], 'uncut_connected_geometric_v3': ['PROOF.md', 'validation_receipt.json'], 'YY_paired_covariance_structural_v2': ['PROOF.md', 'validation_receipt.json'], 'graded_causal_qap': ['DERIVATION.md', 'validation_receipt_v2.json'], 'YY_geometric_finite_map_transport_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'causal_one_loop_sewing': ['DERIVATION.md', 'validation_receipt.json'], 'graded_causal_qap': ['DERIVATION.md', 'validation_receipt_v2.json'], 'e5_compact_phi_quartic_insertion_v2': ['PROOF.md', 'validation_receipt.json'], 'uncut_local_common_primitive_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'e5_compact_phi_causal_collar_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_paired_covariance_structural_v2': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'e5_causal_master_contact_split_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_compact_phi_causal_collar_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_compact_phi_quartic_insertion_v2': ['PROOF.md', 'validation_receipt.json'], 'causal_one_loop_sewing': ['DERIVATION.md', 'validation_receipt.json'], 'graded_causal_qap': ['DERIVATION.md', 'validation_receipt_v2.json']})
        owners.update({'e5_phi_first_local_contact_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_causal_master_contact_split_v1': ['PROOF.md', 'validation_receipt.json'], 'uncut_local_common_primitive_v1': ['PROOF.md', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'e5_scalar_potential_local_contact_v1': ['PROOF.md', 'validation_receipt.json'], 'physical_current_input_recovery_g1_v1': ['PROOF.md', 'native_v2_action.json.gz', 'replay_v4_action.json.gz', 'validation_receipt.json'], 'g1_current_profile_applicability_v1': ['PROOF.md', 'validation_receipt_v2.json'], 'unprobed_compact_all_coupling_v1': ['PROOF.md', 'native_full_current.json.gz', 'replay_full_current.json.gz', 'validation_receipt.json'], 'regulator_free_inverse_g1_recovery_v1': ['PROOF.md', 'native_inverse.json.gz', 'replay_inverse.json.gz', 'validation_receipt.json']})
        owners.update({'e5_mixed_phi_g2_local_regulator_v4': ['PROOF.md', 'mixed_phi_g2_local_regulator.py', 'validation_receipt.json'], 'YY_literal_collapsed_width_trace_v1': ['PROOF.md', 'validation_receipt.json'], 'YY_higher_direct_regulator_clock_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'e5_mixed_phi_g3_critical_contact_v1': ['PROOF.md', 'mixed_phi_g3_critical_contact.py', 'result.json', 'validation_receipt.json'], 'common_conversion_carrier_v1': ['PROOF.md', 'validation_receipt.json'], 'scalar_causal_conversion_check_v3': ['PROOF.md', 'validation_receipt.json'], 'causal_one_loop_sewing': ['DERIVATION.md', 'validation_receipt.json'], 'graded_causal_qap': ['DERIVATION.md', 'validation_receipt_v2.json']})
        owners.update({'e5_phi_g3_causal_local_contact_v2': ['PROOF.md', 'validation_receipt.json'], 'current_background_reference_bridge_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_mixed_phi_g3_critical_contact_v1': ['PROOF.md', 'mixed_phi_g3_critical_contact.py', 'validation_receipt.json']})
        owners.update({'e5_phi_gauge_first_jet_contact_v2': ['PROOF.md', 'phi_gauge_first_jet_contact.py', 'validation_receipt.json'], 'joint_common_family_applicability_v1': ['PROOF.md', 'native_complete_full_background_extension.json.gz', 'replay_complete_full_background_extension.json.gz', 'validation_receipt.json'], 'YY_geometric_finite_map_transport_v1': ['PROOF.md', 'validation_receipt.json'], 'current_background_reference_bridge_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'e5_phi_gauge_geometric_contact_v2': ['PROOF.md', 'phi_gauge_geometric_contact.py', 'validation_receipt.json'], 'e5_phi_gauge_first_jet_contact_v2': ['PROOF.md', 'validation_receipt.json'], 'e5_compact_phi_quartic_insertion_v2': ['PROOF.md', 'validation_receipt.json'], 'e5_causal_master_contact_split_v1': ['PROOF.md', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['PROOF.md', 'native_full_current.json.gz', 'replay_full_current.json.gz', 'validation_receipt.json']})
        owners.update({'e5_phi_switched_joint_contact_v3': ['PROOF.md', 'validation_receipt.json'], 'e5_phi_g3_causal_local_contact_v2': ['PROOF.md', 'validation_receipt.json'], 'uncut_local_common_primitive_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_mixed_phi_g3_critical_contact_v1': ['PROOF.md', 'mixed_phi_g3_critical_contact.py', 'validation_receipt.json']})
        owners.update({'e5_phi_local_source_exclusion_v2': ['PROOF.md', 'validation_receipt.json'], 'e5_phi_switched_joint_contact_v3': ['PROOF.md', 'validation_receipt.json'], 'e5_mixed_phi_g3_critical_contact_v1': ['PROOF.md', 'mixed_phi_g3_critical_contact.py', 'validation_receipt.json'], 'uncut_local_common_primitive_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'e5_phi_saturated_ordinary_contact_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_phi_g3_causal_local_contact_v2': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'e5_mixed_phi_g3_critical_contact_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'e5_mixed_phi_g2_local_regulator_v4': ['PROOF.md', 'validation_receipt.json'], 'regulator_free_inverse_g1_recovery_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'e5_phi_symbolic_switch_orbit_v1': ['PROOF.md', 'validation_receipt.json', 'result.json'], 'e5_phi_saturated_ordinary_contact_v1': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'e5_phi_local_source_exclusion_v2': ['PROOF.md', 'result.json', 'validation_receipt.json', 'result.json'], 'e5_phi_switched_joint_contact_v3': ['PROOF.md', 'validation_receipt.json', 'result.json'], 'joint_common_family_applicability_v1': ['PROOF.md', 'native_complete_full_background_extension.json.gz', 'replay_complete_full_background_extension.json.gz', 'validation_receipt.json'], 'regulator_free_inverse_g1_recovery_v1': ['PROOF.md', 'native_inverse.json.gz', 'replay_inverse.json.gz', 'validation_receipt.json']})
        owners.update({'e5_phi_complete_local_ward_v1': ['PROOF.md', 'validation_receipt.json'], 'current_causal_initial_dictionary_v1': ['PROOF.md', 'validation_receipt.json'], 'uncut_local_common_primitive_v1': ['PROOF.md', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['PROOF.md', 'validation_receipt.json'], 'causal_one_loop_sewing': ['DERIVATION.md', 'validation_receipt.json'], 'graded_causal_qap': ['DERIVATION.md', 'validation_receipt_v2.json']})
        owners.update({'e5_fixed_flat_local_qme_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_phi_complete_local_ward_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_causal_master_contact_split_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_compact_phi_causal_collar_v1': ['PROOF.md', 'validation_receipt.json'], 'causal_one_loop_sewing': ['DERIVATION.md', 'validation_receipt.json'], 'graded_causal_qap': ['DERIVATION.md', 'validation_receipt_v2.json']})
        owners.update({'e5_phi_local_bv_collar_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_fixed_flat_local_qme_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_phi_complete_local_ward_v1': ['PROOF.md', 'validation_receipt.json'], 'current_background_reference_bridge_v1': ['PROOF.md', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['PROOF.md', 'native_full_current.json.gz', 'replay_full_current.json.gz', 'validation_receipt.json']})
        owners.update({'e5_compact_background_causal_bv_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_phi_local_bv_collar_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_phi_complete_local_ward_v1': ['PROOF.md', 'validation_receipt.json'], 'causal_one_loop_sewing': ['DERIVATION.md', 'validation_receipt.json'], 'graded_causal_qap': ['DERIVATION.md', 'validation_receipt_v2.json']})
        owners.update({'e5_two_scalar_probe_contact_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_phi_local_bv_collar_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_compact_background_causal_bv_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_mixed_phi_g3_critical_contact_v1': ['PROOF.md', 'mixed_phi_g3_critical_contact.py', 'validation_receipt.json'], 'regulator_free_inverse_g1_recovery_v1': ['PROOF.md', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'e5_compact_width_quantum_transport_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_phi_local_bv_collar_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_fixed_flat_local_qme_v1': ['PROOF.md', 'validation_receipt.json'], 'ghost_one_coupling_torsion_v1': ['PROOF.md', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['PROOF.md', 'native_full_current.json.gz', 'replay_full_current.json.gz', 'validation_receipt.json']})
        owners.update({'e5_phi_local_class_nontrivial_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_two_scalar_probe_contact_v1': ['PROOF.md', 'validation_receipt.json'], 'current_background_reference_bridge_v1': ['PROOF.md', 'validation_receipt.json'], 'causal_one_loop_sewing': ['DERIVATION.md', 'validation_receipt.json']})
        owners.update({'e5_phi_kinetic_mixed_contact_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_compact_background_causal_bv_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_phi_switched_joint_contact_v3': ['PROOF.md', 'validation_receipt.json'], 'e5_mixed_phi_g3_critical_contact_v1': ['PROOF.md', 'mixed_phi_g3_critical_contact.py', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'e5_phi_covariant_kinetic_probe_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_phi_kinetic_mixed_contact_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_two_scalar_probe_contact_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_phi_gauge_geometric_contact_v2': ['PROOF.md', 'validation_receipt.json'], 'e5_mixed_phi_g3_critical_contact_v1': ['PROOF.md', 'mixed_phi_g3_critical_contact.py', 'validation_receipt.json'], 'e5_phi_g3_causal_local_contact_v2': ['PROOF.md', 'validation_receipt.json'], 'e5_compact_width_quantum_transport_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_fixed_flat_local_qme_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'e5_phi_covariant_kinetic_quartic_v1': ['PROOF.md', 'phi_covariant_kinetic_quartic.py', 'validation_receipt.json'], 'e5_compact_width_quantum_transport_v1': ['PROOF.md', 'compact_width_quantum_transport.py', 'validation_receipt.json'], 'e5_phi_local_bv_collar_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_fixed_flat_local_qme_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'uncut_background_core_boundary_v2': ['PROOF.md', 'RESULT.md', 'validation_receipt.json'], 'uncut_background_bridge_boundary_v1': ['PROOF.md', 'RESULT.md', 'validation_receipt.json'], 'grouped_BB_feynman_boundary_v1': ['PROOF.md', 'RESULT.md', 'validation_receipt.json'], 'uncut_ghost_boundary_v1': ['PROOF.md', 'RESULT.md', 'validation_receipt_v3.json'], 'full_selected_causal_profile_v1': ['PROOF.md', 'RESULT.md', 'validation_receipt.json']})
        owners.update({'compact_retained_source_functional_v1': ['PROOF.md', 'RESULT.md', 'validation_receipt.json'], 'e5_fixed_flat_local_qme_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_compact_background_causal_bv_v1': ['PROOF.md', 'validation_receipt.json'], 'uncut_connected_geometric_v3': ['PROOF.md', 'RESULT.md', 'validation_receipt.json'], 'e5_phi_covariant_kinetic_quartic_v1': ['PROOF.md', 'validation_receipt.json'], 'unprobed_compact_all_coupling_v1': ['PROOF.md', 'native_full_current.json.gz', 'replay_full_current.json.gz', 'validation_receipt.json']})
        owners.update({'uncut_connected_marked_v1': ['PROOF.md', 'connected_marked.py', 'validation_receipt.json'], 'augmented_metric_lift_v1': ['tensor_10.json.gz', 'validation_receipt.json'], 'common_conversion_carrier_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_absolute_compact_ward_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_first_background_core_feynman_v1': ['PROOF.md', 'validation_receipt.json'], 'free_feynman_boundary': ['BOUNDARY_PROOF.md', 'validation_receipt.json']})
        owners.update({'e5_marked_ghost_feynman_v3': ['PROOF.md', 'result.json', 'validation_receipt.json'], 'uncut_connected_marked_v1': ['PROOF.md', 'connected_marked.py', 'validation_receipt.json'], 'uncut_connected_ward_v1': ['PROOF.md', 'validation_receipt.json']})
        owners.update({'paired_w6_source_replacement_v1': ['PROOF.md', 'source_replacement.py', 'validation_receipt.json'], 'e5_compact_formal_width_equivalence_v1': ['PROOF.md', 'validation_receipt.json'], 'e5_absolute_compact_ward_v1': ['PROOF.md', 'validation_receipt.json'], 'full_jet_source_master_bridge': ['primary_inputs.json.gz', 'replay_inputs.json.gz', 'final_review_validation_receipt.json']})
        names = {'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_e5_full_hessian/replay.json', 'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_bv_master/primary.json', 'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_e5_quotient/replay.json', 'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_bv_master/replay.json', 'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_e2_transport/primary.json', 'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_e2_transport/replay.json', 'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_e5_quotient/primary.json', 'tools/two_loop_qft_compiler_v1/m08_independent_replay_package_v1/frozen_a10_e5_full_hessian/primary.json'} | {"AGENTS.md", "CHARTER.md", "project_state.json",
                 "docs/RESEARCH_EXECUTION_HANDOFF_V1163.md",
                 "calculations/canonical_so10_causal_one_loop_sewing/DERIVATION.md",
                 "calculations/canonical_so10_causal_one_loop_sewing/RESULT.md",
                 "calculations/canonical_so10_mass_tag_transport_v1/PROOF.md"}
        for owner_input in ("primary.json", "replay.json", "bindings.json", "validation_receipt.json"):
            names.add((PK / "frozen_a10_cotangent_adapter" / owner_input).relative_to(ROOT).as_posix())
        names.add((PK / "source_convention_control.py").relative_to(ROOT).as_posix())
        names.add((PK / "A10_E3_SYMMETRY_CONTRACT_V1.md").relative_to(ROOT).as_posix())
        names.add((PK / "A10_E5_QUANTUM_FUNCTIONAL_SPEC_V1.md").relative_to(ROOT).as_posix())
        names.add((PK / "frozen_a10_e5_quantum_contract/bindings.json").relative_to(ROOT).as_posix())
        names.update(("calculations/canonical_so10_original_Ja_ghost_bubble/algebra.py",
                      "calculations/canonical_so10_intrinsic_full_source_descent/coefficient_ring.py"))
        for path in ("export_a10_e5_antighost_vector.py",
                     "frozen_a10_physical_reconciliation/full_primary.json",
                     "frozen_a10_physical_reconciliation/full_replay.json"):
            names.add((PK / path).relative_to(ROOT).as_posix())
        names.update((PK / p).relative_to(ROOT).as_posix() for p in ['frozen_a10_e5_coupling_ring/primary.json', 'frozen_a10_e5_coupling_ring/replay.json', 'frozen_a10_e5_coupling_ring/validation_receipt.json', 'frozen_a10_e5_coupling_ring/bindings.json', 'frozen_a10_e5_regularity/primary.json', 'frozen_a10_e5_regularity/replay.json', 'frozen_a10_e5_regularity/validation_receipt.json', 'frozen_a10_e3_symmetry/primary.json', 'frozen_a10_e3_symmetry/replay.json', 'frozen_a10_e3_symmetry/validation_receipt.json', 'frozen_a10_e5_nonminimal_retract/validation_receipt.json', 'frozen_a10_executable_reconciliation/M08_PHYSICAL_ACTION_COVARIANT_EXECUTABLE_V1.json', 'A10_E5_COUPLING_RING_RESULT.md', 'A10_E5_REGULARITY_DERIVATION_V1.md', 'A10_E5_NONMINIMAL_RETRACT_DERIVATION_V1.md', 'A10_E3_SYMMETRY_RESULT.md', 'A10_E5_RENORMALIZATION_POLICY_ANALYSIS_V1.md'])
        names.update((PK / p).relative_to(ROOT).as_posix() for p in ['frozen_a10_e5_minimal_target/primary.json', 'frozen_a10_e5_minimal_target/replay.json', 'frozen_a10_e5_minimal_target/validation_receipt.json', 'A10_E5_MINIMAL_TARGET_RESULT.md'])
        for owner, paths in owners.items():
            names.update(f"calculations/canonical_so10_{owner}/{path}" for path in paths)
    else:
        assert phase == "validation"
        assert set(git("diff", "--name-only", "HEAD").decode().splitlines()) == set(NAV[:2])
        for name, backup in zip(NAV[:2], ("README_before_final.bytes", "campaign_before_final.bytes")):
            assert (CONTROL / backup).read_bytes().replace(b"\r\n", b"\n") == git("show", "HEAD:" + name)
        first = read(HERE / "preparation_native.json")
        for name, expected in first["sha256"].items():
            assert digest(ROOT / name) == expected, name
        names = set(first["sha256"]) | set(NAV) | {"docs/LOCAL_RESEARCH_CONVENTIONS_V1.md"}
        snapshots = ("RESULT.md",)
    for name in snapshots:
        raw = (HERE / name).read_bytes()
        if name.endswith(".py"):
            ast.parse(raw)
        with (HERE / (name + ".source.txt")).open("xb") as f:
            f.write(raw)
    names.update(path.relative_to(ROOT).as_posix() for path in HERE.iterdir() if path.is_file())
    save(f"preparation_{phase}.json", {
        "base_HEAD": BASE, "sha256": {name: digest(ROOT / name) for name in sorted(names)},
        "scientific_acceptance": "NOT_PERFORMED",
        "limits": {"seconds": 120 if phase == "native" else 180, "e4_seconds": 120,
                   "sampled_private_bytes": 8 * 1024**3, "minimum_available_commit_bytes": 350 * 1024**2,
                   "artifact_bytes": 8 * 1024**2, "packet_bytes": 32 * 1024**2},
    })


def run_worker(check, phase):
    started = time.perf_counter()
    prep = read(HERE / f"preparation_{phase}.json")
    timer = threading.Timer(prep["limits"]["seconds"], lambda: os._exit(124))
    timer.daemon = True
    timer.start()
    assert git("rev-parse", "HEAD").decode().strip() == BASE == prep["base_HEAD"]
    for name, expected in prep["sha256"].items():
        assert digest(ROOT / name) == expected, name
    if phase == "native":
        save("result.json", {"execution_state": "COMPLETED", "checks": check("native")})
        print("STAGE E5 unmarked direct Ward continuation controls checked", flush=True)
    else:
        review(check, prep, started)
    timer.cancel()


def review(check, prep, started):
    assert not git("diff", "--cached", "--name-only")
    assert git("ls-tree", "-r", "HEAD") == (CONTROL / "old_git_tree.txt").read_bytes()
    for name in ("preparation_native.json", "capture_native.json", "result.json"):
        assert (HERE / name).read_bytes() == (CONTROL / name).read_bytes()
    cap = read(HERE / "capture_native.json")
    assert cap["calculation_completed"] and cap["post_run_observations_qualified"]
    for source in HERE.glob("*.source.txt"):
        assert source.read_bytes() == (HERE / source.name.removesuffix(".source.txt")).read_bytes()
    owners = sorted(n for n in prep["sha256"] if "validation_receipt" in Path(n).name and n.endswith(".json"))
    for name in owners:
        owner = read(ROOT / name)
        if name == "calculations/canonical_so10_full_jet_source_master_bridge/final_review_validation_receipt.json":
            assert owner["schema"] == "FJB_FINAL_REVIEW_VALIDATION_V1"
            assert owner["evidence_validation"] == "PASS_BOUNDED_FJB1_FJB2_FJB3"
            assert owner["scientific_acceptance"] == "NOT_PERFORMED"
            assert owner["e4_step_exits"] == [0,0,0,0,0,2]
        elif name == "calculations/canonical_so10_mixed_Ward_positive_coupling/validation_receipt.json":
            assert owner["schema"] == "MWP5_INDEPENDENT_FULL_POSITIVE_COUPLING_REVIEW"
            assert owner["evidence_validation"] == "PASS_SELECTED_G1_REFERENCE_WARD_FINITE_PART_WITH_NONZERO_FIXED_HEAT_RESPONSE"
            assert owner["scientific_acceptance"] == "NOT_PERFORMED"
        elif name == "calculations/canonical_so10_mixed_Ward_positive_coupling/final_review_validation_receipt.json":
            assert owner["schema"] == "MWP_FINAL_VALIDATION_AND_NEW_BYTE_SEAL"
            assert owner["evidence_validation"] == "PASS_SELECTED_G1_REFERENCE_RESPONSE_WITH_RHS_AND_FINITE_NORMALIZATION_OPEN"
            assert owner["scientific_acceptance"] == "NOT_PERFORMED"
            assert owner["E4_step_exits"] == [0,0,0,0,0,2]
        elif "execution_state" in owner:
            assert owner["execution_state"] == "COMPLETED", name
        else:
            assert owner["status"].startswith("PASS_BOUNDED_"), name
    result = read(HERE / "result.json")
    assert result["execution_state"] == "COMPLETED"
    checks = result["checks"]
    assert checks == check("replay")
    assert checks["fixed_chart_phase_products"] == [553,90]
    assert checks["even_affine_and_source_rows"] == [48,7800,48960]
    assert checks["normalized_ellipsoid_mixed_derivative"] == "1/4"
    assert checks["first_dimension_jet_matches_anisotropic_finite_part"]
    assert checks["common_shell_metric_and_reference_controls"]
    print("STAGE E5 unmarked direct Ward continuation replay agrees", flush=True)

    command = [sys.executable, "-B", "tools/research_check.py", "e4", "--historical-context",
               "D:/Codex-Research/ToE-Next/research-evidence/e4-context-v4"]
    try:
        e4 = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=120)
    except subprocess.TimeoutExpired as err:
        save("e4_timeout.json", {"command": command, "state": "INCOMPLETE_TIMEOUT",
                                 "stdout": (err.stdout or b"").decode("utf-8", errors="replace"),
                                 "stderr": (err.stderr or b"").decode("utf-8", errors="replace")})
        raise
    save("e4_capture.json", {"exit_code": e4.returncode, "stdout": e4.stdout, "stderr": e4.stderr})
    events = [json.loads(line) for line in e4.stdout.splitlines() if line.strip()]
    steps = [event for event in events if event.get("event") == "step_finished"]
    exits = [event["exit_code"] for event in steps]
    assert e4.returncode == 0 and exits == [0, 0, 0, 0, 0, 2]
    custody = next(event for event in steps if event["step"] == "historical_custody")
    assert custody["stdout"].count("RECORDED_DIGEST_UNRESOLVED:") == 7
    hist = git("show", "ef70f255a667b9a81e37b344dc78967ada4ed896:README.md")
    assert sha256(hist).hexdigest() == "4a00e15665bebfc23fb0ae9338770c22d1260610bde6435415c09e21a5a43792"
    assert (ROOT / "README.md").read_bytes().replace(b"\r\n", b"\n").endswith(hist)
    state = digest(ROOT / "project_state.json")
    assert state == "d610f07422ff491118a0303c4773661e96bc0d76cf73d9e1a2ec8d148c0977c8"
    for name, expected in prep["sha256"].items():
        assert digest(ROOT / name) == expected, name
    files = [p for p in HERE.iterdir() if p.is_file()] + [ROOT / name for name in NAV]
    save("validation_receipt.json", {"base_HEAD": BASE, "execution_state": "COMPLETED",
         "evidence_validation": "PASS_BOUNDED_E5_DIRECT_UNMARKED_WARD_WICK",
         "scientific_acceptance": "NOT_PERFORMED", "state_sha256": state,
         "E4_step_exits": exits, "historical_custody": "SEVEN_UNRESOLVED_NOTPASS", "owner_receipts": owners,
         "checks": checks,
         "files_excluding_pending_receipt_capture": {p.relative_to(ROOT).as_posix(): digest(p) for p in files},
         "elapsed_after_imports": time.perf_counter() - started})


def main():
    phase = sys.argv[1]
    prepare(phase)
    sys.path.insert(0, str(PK))
    from export_a10_e5_antighost_vector import capture

    report = capture([sys.executable, "-B", str(HERE / "direct_unmarked_ward_wick.py"), phase])
    save(f"capture_{phase}.json", report)
    print(report["stdout_and_stderr"], end="")
    assert report["calculation_completed"] and report["post_run_observations_qualified"]
    assert sum(p.stat().st_size for p in HERE.iterdir() if p.is_file()) <= 32 * 1024**2


if __name__ == "__main__":
    main()
