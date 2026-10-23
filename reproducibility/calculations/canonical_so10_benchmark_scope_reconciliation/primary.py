"""BSR1 actual source selection and resolved finite physical coefficients."""
from data import *
start=begin('primary')
tree=ast.parse((CAL/'canonical_so10_uv_radial_tadpoles/inputs.py').read_bytes())
fn=next(v for v in tree.body if isinstance(v,ast.FunctionDef) and v.name=='coeffs')
strings={v.value for v in ast.walk(fn) if isinstance(v,ast.Constant) and isinstance(v.value,str)}
assert 'canonical_so10_positive_higgs/POINT.json' in strings and 'canonical_so10_scalar_benchmark/STAGE1_POINT.json' in strings
assert 'changed_free_coefficients' in strings
assert 'canonical_so10_coherent_joint_witness/POINT.json' not in strings
assert any(isinstance(v,ast.Call) and isinstance(v.func,ast.Attribute) and v.func.attr=='update' and isinstance(v.func.value,ast.Name) and v.func.value.id=='base' for v in ast.walk(fn))
geom=ast.parse((CAL/'canonical_so10_finite_counterterm_insertion/geometry_v2.py').read_bytes())
assert any(isinstance(v,ast.ImportFrom) and v.module=='inputs' and any(n.name=='coeffs' for n in v.names) for v in geom.body)
old=read(ROOT/OLD_POINT);base=read(CAL/'canonical_so10_scalar_benchmark/STAGE1_POINT.json')['free_coefficients'];base.update(old['changed_free_coefficients'])
new=read(CAL/'canonical_so10_finite_radial_control/primary_result.json')['physical_parameters'];assert F(base['zEta:im'])==0
statuses={};bindings={}
for label,(folder,name) in RECEIPTS.items():
 r=read(CAL/folder/name);statuses[label]=r['status']
 hits=[v[FINITE_POINT] for v in r.values() if isinstance(v,dict) and FINITE_POINT in v]
 if label=='finite_bosonic_warning':
  parent='calculations/canonical_so10_finite_radial_control/validation_receipt.json';packet='calculations/canonical_so10_finite_radial_control/primary_result.json'
  assert r['input_sha256'][parent]==digest(ROOT/parent) and r['input_sha256'][packet]==digest(ROOT/packet)
  scalar=read(ROOT/parent);assert scalar['input_sha256'][FINITE_POINT]==digest(ROOT/FINITE_POINT)
  bindings[label]={'route':'via_scalar_receipt_and_packet','point_sha256':digest(ROOT/FINITE_POINT),'parent_receipt_sha256':digest(ROOT/parent)}
 elif label.startswith('finite_'):
  assert hits and all(h==digest(ROOT/FINITE_POINT) for h in hits);bindings[label]={'route':'direct_point_binding','point_sha256':digest(ROOT/FINITE_POINT)}
r=read(CAL/'canonical_so10_eta_offdiagonal_bound/validation_receipt.json');assert r['fixed_input_eight_quartic_tree_screen_excluded'] and not r['full_Spin10_parameter_space_excluded']
finish('primary',{'schema':'BSR1','old_point_sha256':digest(ROOT/OLD_POINT),'finite_point_sha256':digest(ROOT/FINITE_POINT),
 'old_quartics':{n:str(F(base[n])) for n in NAMES},'finite_quartics':{n:str(F(new[n])) for n in NAMES},
 'old_eta':str(F(base['zEta:re'])),'finite_eta':str(F(new['zEta'])),'receipt_statuses':statuses,
 'C1_static_source_selects_positive_higgs':True,'finite_receipt_point_bindings':bindings,
 'stale_domain_recommendation_requires_correction':True,'old_numerical_results_reinterpreted_as_finite_point':False,'new_physics_or_benchmark_adopted':False},start)
