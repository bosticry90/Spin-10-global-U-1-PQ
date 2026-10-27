from data import *
t=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start();assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation.json')['input_sha256'].items():assert digest(Path(p))==h,p
P=packed(HERE/'primary_tables.json.gz');R=packed(HERE/'replay_tables.json.gz');assert P['method']!=R['method']
for k in ['words','all_actual_roots','target_degree','n_bound_from_external_labels','nonzero_roots']:assert P[k]==R[k],k
for n,z in P['radial_weights'].items():assert s.simplify(s.sympify(z)-s.sympify(R['radial_weights'][n]))==0
assert P['actual_GF_counts']=={'GF_CaX_v':6688,'GF_LX_v':432};assert P['words'] and all(1<=w['n']<=4 for w in P['words'])
counts=Counter(w['n'] for w in P['words']);byroot=Counter(w['root'] for w in P['words']);controls={}
for token in ['M_BC_none_d','M_aL_none','M_FF_C','M_XX_C','M_LL_C','M_BB_C','M_FC_P']:
 controls['omit_'+token]=sum(w['root']==token for w in P['words'])
assert controls['omit_M_BC_none_d'] and controls['omit_M_aL_none'] and controls['omit_M_XX_C'] and controls['omit_M_LL_C']
assert all(not any('xiC_' in z for z in w['path']) for w in P['words'])
artifact={'schema':'VHR1_COMPLETE_EXTRA_GF_VACUUM_ORDERED_HEAT_ROOT_SUPPORT','target_degree':P['target_degree'],'words':P['words'],'actual_roots':P['all_actual_roots'],'actual_GF_counts':P['actual_GF_counts'],'radial_weights':P['radial_weights'],'n_counts':dict(counts),'root_counts':dict(byroot),'complete_support_only':True,'group_coefficients_calculated':False,'complete_regulated_identity_qualified':False,'scientific_acceptance':'NOT_PERFORMED'}
raw=(json.dumps(artifact,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'complete_ordered_root_support.json.gz').open('xb') as f:f.write(blob)
out={'status':'QUALIFIED_COMPLETE_EXTRA_GF_VACUUM_ORDERED_HEAT_ROOT_SUPPORT','ordered_word_count':len(P['words']),'n_counts':dict(counts),'root_counts':dict(byroot),'omission_controls_lost_words':controls,'actual_GF_counts':P['actual_GF_counts'],'group_coefficients_calculated':False,'complete_regulated_identity_qualified':False,'physical_scheme_adopted':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39','artifact_sha256':sha256(blob).hexdigest(),'artifact_raw_sha256':sha256(raw).hexdigest(),'elapsed_after_imports':time.perf_counter()-t}
print('RESULT '+json.dumps(out,sort_keys=True),flush=True)
