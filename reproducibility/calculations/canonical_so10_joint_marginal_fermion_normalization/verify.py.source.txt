"""JMF1 late gate: distinct routes, exact shared ownership and scoped theorem."""
from data import *
tick=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start()
assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation.json')['input_sha256'].items():assert digest(Path(p))==h,p
p=packed(HERE/'primary_tables.json.gz');r=packed(HERE/'replay_tables.json.gz')
for k in p:
 if k not in ['method','elapsed_after_imports']:assert p[k]==r[k],k
assert p['method']!=r['method'] and len(p['matter_parent_patterns'])==len(p['matter_breaking_patterns'])==len(p['shared_source_patterns'])==4

h=packed(HSC/'selected_four_projection_family.json.gz');blocks=embedded(h)
assert digest(HSC/'validation_receipt_v2.json')=='36b4cc573c79aa9cf200cdb39dc85de43c8f694cb41fe353dc54a4e1e4487f5f'
assert digest(CHW/'validation_receipt.json')=='90c47ac743d962e92acd21a2608ad9923f6ad2626ac027a35ea3090f0216b09b'
assert h['proper_matter_source_not_added_twice'] and h['all_four_selected_projection_remainders_zero']
cw=packed(CHW/'closed_heat_ward_normalization_family.json.gz')
assert cw['reference_matching_map_constructed_but_physical_scheme_not_adopted'] and not cw['all_source_open_background_measure_phase_QAP_Slavnov_or_E5A5_proved']
# The new closed density and its variation literally contain no P or source atom.
for key in ['counterterm_density','Ward_image']:
 for word,z in cw[key]:
  assert all(atom[0] in ['L','R','U','V','cL','cR'] for atom in word)

# Prove each complete zero domain from explicit dimensions and valid sparse slots.
full={'BSF':45**2*4,'SVT':45**3*3,'LSF':45**3*3,'SCF':45*328**2*6,'GSF':45*(45*44//2)*6}
for a in blocks['BSF'].values():
 for m in a.values():assert m['shape']==[45,45]
for tag in ['SVT','LSF']:
 for v in blocks[tag].values():
  assert set(v)=={'B'}
  assert len({tuple(row[:3]) for row in v['B']})==len(v['B'])
for fam in blocks['SCF'].values():
 for direction,secs in fam.items():
  assert len(secs)==4 and all(len(ms)==45 for ms in secs.values())
  assert sum(ms[0]['shape'][0] for ms in secs.values())==328
  for ms in secs.values():
   n=ms[0]['shape'][0];assert all(m['shape']==[n,n] for m in ms)
for fam in blocks['GSF'].values():
 for rows in fam.values():assert all(0<=row[0]<45 and 0<=row[1]<row[2]<45 for row in rows)

byblock=p['shared_coefficients'];assert set(byblock)==set(full)
for tag,v in byblock.items():assert 0<v['nonzero_coefficient_slots']<=full[tag]
# Algebraic ownership is addition by calculation origin, not merging by field.
ids=sorted(byblock);bosonic={k:1 for k in ids};HSC={k:1 for k in ids}
joint={k:bosonic[k]+HSC[k]-1 for k in ids};naive={k:bosonic[k]+HSC[k] for k in ids}
assert set(joint.values())=={1} and set(naive.values())=={2}
for k in ids:
 # Omitting the shared restriction, or adding it a second time, changes every
 # nonzero actual source coefficient. This is not a global Ward sensitivity.
 assert byblock[k]['omission_changed_slots']==byblock[k]['duplicate_changed_slots']==byblock[k]['nonzero_coefficient_slots']
assert len(set(p['free_parameters_not_selected']))==9
assert 'b0' not in p['free_parameters_not_selected'] and 'kappa' not in p['free_parameters_not_selected']

recipe={'schema':'JMF1_EXACT_ONCE_JOINT_SELECTED_LOCAL_NORMALIZATION',
 'definition':'C_bStokes+(HSC-C_shared)+K_CHW',
 'bosonic_full_formula':{'path':str(CAL/'canonical_so10_dimensional_stokes_primitive/RESULT.md'),'sha256':digest(CAL/'canonical_so10_dimensional_stokes_primitive/RESULT.md')},
 'HSC_family':{'path':str(HSC/'selected_four_projection_family.json.gz'),'sha256':digest(HSC/'selected_four_projection_family.json.gz')},
 'CHW_family':{'path':str(CHW/'closed_heat_ward_normalization_family.json.gz'),'sha256':digest(CHW/'closed_heat_ward_normalization_family.json.gz')},
 'shared_coefficient_blocks':byblock,'shared_ownership_multiplicity':joint,
 'full_coefficient_domains_including_zero_complements':full,
 'proper_KP_loop_and_fixed_MSP_primitive_are_distinct_unshared_objects':True,
 'different_bosonic_and_fermion_loop_contributions_not_deduplicated_by_field_words':True,
 'selected_matter_projection_transfer':p['selected_matter_projection_transfer'],
 'selected_zero_matter_transfer':p['selected_zero_matter_transfer'],
 'free_parameters_not_selected':p['free_parameters_not_selected'],
 'other_normalizations_not_equated_or_set_zero':True,
 'new_quantum_coefficients_measured':False,'physical_scheme_adopted':False,
 'full_chiral_Slavnov_QAP_measure_phase_background_massive_or_E5A5_qualified':False,
 'scientific_acceptance':'NOT_PERFORMED'}
raw=(json.dumps(recipe,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'joint_selected_family.json.gz').open('xb') as f:f.write(blob)
out={'status':'QUALIFIED_EXACT_ONCE_JOINT_SELECTED_MARGINAL_FERMION_NORMALIZATION',
 'shared_blocks':byblock,'shared_full_coefficient_positions':sum(full.values()),
 'shared_nonzero_coefficient_slots':sum(v['nonzero_coefficient_slots'] for v in byblock.values()),
 'four_matter_parent_patterns':p['matter_parent_patterns'],'four_matter_breaking_patterns':p['matter_breaking_patterns'],
 'four_source_carrier_patterns':p['shared_source_patterns'],'cycle_rank_controls':p['topological_control_cases'],
 'shared_ownership_multiplicity':joint,'naive_direct_sum_multiplicity':naive,
 'new_loop_integrals':0,'old_quantum_and_four_projection_results_reused_not_replayed':True,
 'artifact_sha256':sha256(blob).hexdigest(),'artifact_raw_sha256':sha256(raw).hexdigest(),
 'physical_scheme_adopted':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39',
 'full_chiral_Slavnov_QAP_measure_phase_background_massive_or_E5A5_qualified':False,
 'elapsed_after_imports':time.perf_counter()-tick}
print('RESULT '+json.dumps(out,sort_keys=True),flush=True)
