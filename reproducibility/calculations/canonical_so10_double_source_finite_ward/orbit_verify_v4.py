from orbit_data_v4 import *
t=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start();assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation_v4.json')['input_sha256'].items():assert digest(Path(p))==h,p
V3=read(HERE/'validation_receipt_v3.json');assert V3['full_Ward_image_nonzero']==708732 and not V3['generic_z_GF_source_degree1_qualified']
P=packed(HERE/'orbit_primary_v4_tables.json.gz');R=packed(HERE/'orbit_replay_v4_tables.json.gz')
for k in ['orbit','source_gradients','Phi_heavy_trace_Gram','generic_witness','h_source_Euler_signs','Dh_GF_signs','bJL_Ja_signs','all_new_w_dependence_in_Lambda_source_scalar_GF_only']:assert P[k]==R[k],k
frozen,ja,frozen_image=frozen_columns();grads=list(map(fromrows,P['source_gradients']));assert sum(len(p) for p in grads)==10940
# Full source-Ja image comparison uses the entire stored local density,
# not one source column or only the anchor.
old=packed(HERE/'primary_v2_tables.json.gz');fullja=fromrows(old['pieces']['source_Ja']);actual=add(*(scale(product(var(f'JAp{i}'),p),-1) for i,p in enumerate(grads)));assert actual==fullja
ev=s.SparseMatrix(45,328,{});off=0;nz=0
for b,(sec,n) in zip(P['orbit'],SECTORS):
 assert b['sector']==sec
 rs=list(map(dec,b['generic_orbit_generators']));assert len(rs)==45
 for i,r in enumerate(rs):
  assert r.shape==(n,n);zero(r+r.T);assert all(co(s.conjugate(z)-z)==0 for z in r.todok().values())
  if i<12:assert not r.todok()
  nz+=len(r.todok())
 ev[:,off:off+n]=dec(b['evaluation_v0']);off+=n
names=[f'x_{sec}_{j}' for sec,n in SECTORS for j in range(n)]
for i in range(45):
 expected={((names[j],()),):co(g*xi*z) for (ii,j),z in ev.todok().items() if ii==i};assert clean(expected)==frozen[i]
gram=dec(P['Phi_heavy_trace_Gram']);assert gram.rank()==33
wit=P['generic_witness'];wcoef=co(wit['coefficient_without_gxi_g4log2_16pi2']);assert wcoef!=0
phases={}
for contour in ['Lorentzian','Euclidean']:
 dh=co(P['Dh_GF_signs'][contour]);sj=co(P['bJL_Ja_signs'][contour]);ha=co(P['h_source_Euler_signs'][contour]);assert co(dh+sj*ha)==0;phases[contour]={'Dh_GF':str(dh),'source_Ja_term':str(sj*ha),'sum':'0'}
wrong=co(1+(-1)*(-1));assert wrong==2 and wrong*wcoef!=0
out={'status':'QUALIFIED_GENERIC_W_SCALAR_SOURCE_WARD_EXTENSION_IN_FACTORED_FORM','elapsed_after_imports':time.perf_counter()-t,'generic_orbit_nonzero_entries':nz,'source_gradient_positions_nonzero':10940,'full_scalar_orbit_positions':45*328**2,'within_sector_positions':45*sum(n*n for sec,n in SECTORS),'cross_sector_zeros_by_types':45*(328**2-sum(n*n for sec,n in SECTORS)),'frozen_v0_source_Euler_positions_matched':14760,'frozen_v0_full_Ward_scalar_image_bridge':'complete orbit factors and full source gradients match; no new expansion of qualified frozen image','generic_w_rule':'bC(w)=bC(v0)+g10*xi*sum_i (x.T*r_i*z)*D_JLambda_i P, times common g10^4*log(2)/(16pi^2)','complete_source_gradients_match_frozen_Ja_descendant':True,'Phi54_heavy_Gram_rank':33,'nonzero_witness':wit,'local_h_consistency':phases,'wrong_contour_source_Euler_multiplier':str(wrong),'wrong_contour_witness_nonzero':str(co(wrong*wcoef)),'generic_z_scalar_dependency_now_explicit':True,'highest_source_Ward_image_unchanged':True,'old708732_term_image_not_rerun':True,'no_full_generic_polynomial_expansion_claimed':True,'full_quantum_two_Q_or_coincidence_QAP_E5A5_qualified':False,'finite_scheme_or_parameters_changed':False,'authority':'34/39','scientific_acceptance':'NOT_PERFORMED'}
raw=(json.dumps({'scope':out,'complete_generic_orbit':P['orbit'],'complete_source_gradients':P['source_gradients'],'Phi_heavy_Gram':P['Phi_heavy_trace_Gram'],'frozen_Ward_parent_artifact':{'path':str(HERE/'selected_contact_Ward_descendants_v3.json.gz'),'sha256':digest(HERE/'selected_contact_Ward_descendants_v3.json.gz')},'factored_contraction_index_rule':'sum_i,j,A r_i[j,A]*x_j*z_A*(D_i P), multiplied by g10*xi and inherited common g10^4log2/16pi2','all_coefficients_defined_without_truncation':True},sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'generic_w_Ward_extension_v4.json.gz').open('xb') as f:f.write(blob)
out.update({'artifact_sha256':sha256(blob).hexdigest(),'artifact_raw_sha256':sha256(raw).hexdigest()});print('RESULT '+json.dumps(out,sort_keys=True),flush=True)
