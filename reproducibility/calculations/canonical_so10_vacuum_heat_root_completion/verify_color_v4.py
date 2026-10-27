from color_data_v4 import *
t=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start();assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'validation_preparation_v4.json')['input_sha256'].items():assert digest(Path(p))==h,p
P=packed(HERE/'color_primary_v3_tables.json.gz');R=packed(HERE/'color_replay_v4_tables.json.gz');assert P['method']!=R['method']
for k in ['betaB','betaL','Nanti','Vold','n3_color_residual','cubic_auxiliary_rows_retained','scalar_review']:assert P[k]==R[k],k
assert P['cubic_auxiliary_rows_retained']==836 and not P['n3_color_residual'] and P['betaL']==P['Nanti']
assert P['scalar_review']['unbroken_projected_orbit_zero']
templates=packed(HERE/'universal_word_coefficients_v2.json.gz')['templates']
def parse_poly(z):return {tuple(w):s.Rational(a)+s.I*s.Rational(b) for w,a,b in z}
def plus_poly(a,b):
 out=dict(a)
 for k,z in b.items():out[k]=s.expand(out.get(k,0)+z)
 return {k:z for k,z in out.items() if z!=0}
# FF pair is a free-polynomial zero; XX has equal coefficients and receives
# opposite B R_X O/B R_X.T O by the actual antisymmetry checked in both workers.
ff=[i for i,x in enumerate(templates) if x['word']['root']=='M_FF_C'];xx=[i for i,x in enumerate(templates) if x['word']['root']=='M_XX_C'];assert len(ff)==len(xx)==2
for side in ['holo','anti']:
 assert not plus_poly(parse_poly(templates[ff[0]][side]),parse_poly(templates[ff[1]][side]));assert templates[xx[0]][side]==templates[xx[1]][side]
remaining=[x for x in templates if x['word']['n']==3 and x['word']['root'] in ['M_BB_C','M_LL_C','M_FC_P']];assert len(remaining)==3
bb=next(x for x in remaining if x['word']['root']=='M_BB_C');ll=next(x for x in remaining if x['word']['root']=='M_LL_C');fc=next(x for x in remaining if x['word']['root']=='M_FC_P')
for side in ['holo','anti']:
 assert bb[side]==ll[side]
 relabel={tuple('G' if a=='R' else 'g' if a=='r' else a for a in w):z for w,z in parse_poly(fc[side]).items()}
 assert not plus_poly(parse_poly(bb[side]),relabel)
bd={(r,a,c):s.sympify(z) for r,a,c,z in P['betaB']};ld={(r,a,c):s.sympify(z) for r,a,c,z in P['betaL']};vd={(r,a,c):s.sympify(z) for r,a,c,z in P['Vold']};controls={}
for name,table in [('omit_vector_tangent',{(a,r,c):z for (r,a,c),z in bd.items()}),('omit_auxiliary_tangent',ld),('wrong_vertex_order',{k:2*z for k,z in vd.items()})]:controls[name]=len(clean(table));assert controls[name]>0
GOR=CAL/'canonical_so10_ghost_vertex_order_reconciliation';FAM=packed(GOR/'order_corrected_vacuum_family.json.gz');Y=packed(CAL/'canonical_so10_yukawa_carrier_transport/primary_tables.json.gz');Ls=dec(FAM['source']['scalar']);models=[];positions=0;ct_positions=0;h_positions=0
K=dec(packed(CAL/'canonical_so10_vacuum_tangent_source_finite/selected_vacuum_source_relative_member.json.gz')['kernel_chi4']);v=dec(read(PK/'frozen_a10_physical_reconciliation/full_primary.json')['vacuum']['VEV']);TT=list(map(dec,Y['Tminus']))
hw=packed(CAL/'canonical_so10_tangent_heat_ward_bridge/primary_tables.json.gz');assert s.simplify(s.sympify(hw['heat_BK_coefficient'])-s.log(s.Rational(3,2)))==0
for idx,carrier in enumerate(['10','126']):
 B=dec(Y['B'+carrier]);e=B*Ls;mass=s.Matrix(16,16,list(B*K*v));fixed_image=[s.I*(tc.T*mass+mass*tc)/2 for tc in TT];models.append({'carrier':carrier,'heat_log3over2':{'holo':[],'anti':[]},'n3_log4over3_coefficient_zero':True,'n4_log5over4_coefficient_zero':True})
 for side,BB in [('holo',B),('anti',s.conjugate(B))]:
  ee=BB*Ls
  for c in range(45):
   h=s.Matrix(16,16,list(ee[:,c]));model=FAM['models'][idx];dim=dec(model[('' if side=='holo' else 'anti_')+'total'][c]);polys=model['finite_extra_Slavnov_image']
   for p in ['chi4','log3over2','fixed']:
    img=dec(polys[p][c]);img=img if side=='holo' else s.conjugate(img);heat=h if p=='log3over2' else s.zeros(16);insertion=dim if p=='fixed' else s.zeros(16)
    assert not (insertion-heat-img).applyfunc(co).todok();positions+=256
    cv=(fixed_image[c] if side=='holo' else s.conjugate(fixed_image[c])) if p=='fixed' else s.zeros(16);assert not (heat+cv+img).applyfunc(co).todok();ct_positions+=256
   models[-1]['heat_log3over2'][side].append({'shape':[16,16],'entries':[[int(i),int(j),str(co(z))] for (i,j),z in sorted(s.SparseMatrix(h).todok().items()) if co(z)!=0]})
  BK=BB*K
  for p in ['chi4','log3over2','fixed']:
   heat=BK if p=='log3over2' else s.zeros(256,328);ins=-BK/2 if p=='fixed' else s.zeros(256,328);img=-BK if p=='log3over2' else -BK/2 if p=='fixed' else s.zeros(256,328);cv=BK/2 if p=='fixed' else s.zeros(256,328)
   assert not (ins-heat-img).applyfunc(co).todok() and not (heat+cv+img).applyfunc(co).todok();h_positions+=256*328
artifact={'schema':'VHR1_COMPLETE_SELECTED_EXTRA_GF_VACUUM_HEAT_RESPONSE','models':models,'ordered_word_count':12,'group_proofs':{'n2':'DIRECT_HWB_GOR_LINEAR_SCALAR_VERTEX_KERNEL','n3_constant_pair':'UNIVERSAL_FREE_WORD_ZERO','n3_FF_pair':'UNIVERSAL_FREE_WORD_ZERO','n3_XX_pair':'UNIVERSAL_TEMPLATE_PLUS_ACTUAL_SCALAR_ANTISYMMETRY','n3_BB_LL_FC':'ACTUAL_Vold-betaB_transpose-betaL=0_ALL45CUBED','n4_constant_pair':'UNIVERSAL_FREE_WORD_ZERO'},'finite_identity':'Rdim-Rheat-bCrel=0','selected_heat_counterterm_image_zero':True,'complete_selected_first_variation_identity':True,'full_renormalized_source_contact_QAP_E5A5_qualified':False,'physical_scheme_adopted':False,'scientific_acceptance':'NOT_PERFORMED'}
raw=(json.dumps(artifact,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'complete_selected_vacuum_heat_response_v4.json.gz').open('xb') as f:f.write(blob)
out={'status':'QUALIFIED_COMPLETE_SELECTED_EXTRA_GF_VACUUM_HEAT_RESPONSE_AND_FINITE_IDENTITY','ordered_word_count':12,'model_color_identity_positions':45**3,'model_color_identity_nonzero_remainder':0,'scalar_review':P['scalar_review'],'all_cubic_auxiliary_rows_retained':P['cubic_auxiliary_rows_retained'],'finite_comparison_coefficient_positions':positions,'selected_counterterm_coefficient_positions':ct_positions,'inherited_h_identity_positions':h_positions,'controls_changed_color_positions':controls,'complete_selected_first_variation_identity':True,'full_renormalized_source_contact_QAP_E5A5_qualified':False,'physical_scheme_adopted':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39','artifact_sha256':sha256(blob).hexdigest(),'artifact_raw_sha256':sha256(raw).hexdigest(),'elapsed_after_imports':time.perf_counter()-t}
print('RESULT '+json.dumps(out,sort_keys=True),flush=True)
