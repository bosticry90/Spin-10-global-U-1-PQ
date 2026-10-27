from color_data_v4 import *
from itertools import combinations_with_replacement
t=time.perf_counter();timer=threading.Timer(600,lambda:os._exit(124));timer.daemon=True;timer.start();assert __debug__ and hasattr(__import__('sitecustomize'),'DENIED')
for p,h in read(HERE/'preparation_v5.json')['input_sha256'].items():assert digest(Path(p))==h,p
# doubled dimension,ghost,parity,Lorentz-slot parity
TY={'B':(2,0,0,1),'x':(2,0,0,0),'c':(2,1,1,0),'a':(2,-1,1,0),'Lambda':(4,0,0,0),'P':(3,0,1,0),'KP':(3,-1,0,0),'JB':(4,-1,1,1),'Jx':(4,-1,1,0),'JC':(4,-2,0,0),'Ja':(4,0,0,0),'JL':(2,-1,1,0),'d':(2,0,0,1)}
sources={'JB','Jx','JC','Ja','JL','KP'}
def select(rest,marker):
 w=tuple(sorted(rest+(marker,)));nums=[TY[n] for n in rest];dim=sum(n[0] for n in nums)+(2 if marker=='v' else 4);gh=sum(n[1] for n in nums)+(0 if marker=='v' else 1);par=sum(n[2] for n in nums)+(0 if marker=='v' else 1);lor=sum(n[3] for n in nums)
 return dim==8 and gh==0 and par%2==lor%2==0,w
def enum1(marker):
 found=[];names=sorted(TY)
 def walk(j,rest,cost):
  if cost>8:return
  if j==len(names):
   ok,w=select(tuple(rest),marker)
   if ok:found.append(w)
   return
  n=names[j]
  for k in range((8-cost)//TY[n][0]+1):walk(j+1,rest+[n]*k,cost+TY[n][0]*k)
 walk(0,[],2 if marker=='v' else 4);return sorted(set(found))
def enum2(marker):
 found=[];names=sorted(TY);bound=(8-(2 if marker=='v' else 4))//2
 for k in range(bound+1):
  for rest in combinations_with_replacement(names,k):
   ok,w=select(rest,marker)
   if ok:found.append(w)
 return sorted(set(found))
census={}
for marker in ['v','h']:
 a,b=enum1(marker),enum2(marker);assert a==b;census[marker]={'matter':[list(w) for w in a if w.count('P')>=2],'sources':[list(w) for w in a if any(n in sources for n in w)]}
assert census['v']['matter']==[['P','P','v']]
# Lower-case c is the actual ghost token; compare sets to avoid lexical-order claims.
assert {tuple(x) for x in census['v']['sources']}=={tuple(sorted(z)) for z in [('Jx','c','v'),('Ja','v','x'),('JL','c','v','x')]}
assert {tuple(x) for x in census['h']['sources']}=={tuple(sorted(z)) for z in [('Jx','h'),('JL','h','x')]}
JMF=CAL/'canonical_so10_joint_marginal_fermion_normalization';old=packed(JMF/'joint_selected_family.json.gz');assert old['definition']=='C_bStokes+(HSC-C_shared)+K_CHW' and not old['physical_scheme_adopted']
for key in ['bosonic_full_formula','HSC_family','CHW_family']:assert digest(Path(old[key]['path']))==old[key]['sha256']
GOR=packed(CAL/'canonical_so10_ghost_vertex_order_reconciliation/order_corrected_vacuum_family.json.gz');heat=packed(HERE/'complete_selected_vacuum_heat_response_v4.json.gz');Y=packed(CAL/'canonical_so10_yukawa_carrier_transport/primary_tables.json.gz');T=list(map(dec,Y['Tminus']));K=dec(packed(CAL/'canonical_so10_vacuum_tangent_source_finite/selected_vacuum_source_relative_member.json.gz')['kernel_chi4']);v=dec(read(PK/'frozen_a10_physical_reconciliation/full_primary.json')['vacuum']['VEV']);Lt=dec(GOR['source']['total']);Lo=dec(GOR['source']['orbit']);models=[];positions=0
for idx,carrier in enumerate(['10','126']):
 B=dec(Y['B'+carrier]);D=s.Matrix(16,16,list(B*K*v));new={'chi4':-D,'log3over2':-D,'fixed':s.zeros(16)}
 for p in new:
  split=dec(GOR['models'][idx]['mass_extra_by_finite_part'][p])+(D/2 if p=='fixed' else s.zeros(16));assert not (new[p]-split).applyfunc(co).todok()
 for side,BB,tt,dd in [('holo',B,T,D),('anti',s.conjugate(B),[-z.T for z in T],s.conjugate(D))]:
  for c,tc in enumerate(tt):
   for p in new:
    dm=new[p] if side=='holo' else s.conjugate(new[p]);source=BB*(Lt if p=='chi4' else Lo if p=='log3over2' else s.zeros(328,45));image=s.I*(tc.T*dm+dm*tc)+s.Matrix(16,16,list(source[:,c]));hh=dec(heat['models'][idx]['heat_log3over2'][side][c]) if p=='log3over2' else s.zeros(16);assert not (hh+image).applyfunc(co).todok();positions+=256
 models.append({'carrier':carrier,'extra_mass_kernel_by_part':{p:{'shape':[16,16],'entries':[[int(i),int(j),str(co(z))] for (i,j),z in sorted(s.SparseMatrix(m).todok().items()) if co(z)!=0]} for p,m in new.items()}})
recipe={'schema':'VHR1_EXACT_ONCE_SELECTED_JOINT_VACUUM_TANGENT_EXTENSION','old_joint_family':{'path':str(JMF/'joint_selected_family.json.gz'),'sha256':digest(JMF/'joint_selected_family.json.gz')},'old_joint_definition':old['definition'],'additional_terms_only':['mass kernel -(g10^2*xi/(16*pi^2))*(chi4+log(3/2))*B_R*K*v with its conjugate','+(g10^2*xi/(16*pi^2))*chi4*Jx.T*K*h'],'proper_JxCv_ownership':'ALREADY_IN_C_bStokes; NO_SECOND_COPY','ordinary_Yukawa_mass_at_v_ownership':'ALREADY_IN_HSC; ADD_CM_MINUS_CYv_PLUS_Cv_ONLY','source_Jh_kernel_chi4':{'path':str(CAL/'canonical_so10_vacuum_tangent_source_finite/selected_vacuum_source_relative_member.json.gz'),'sha256':digest(CAL/'canonical_so10_vacuum_tangent_source_finite/selected_vacuum_source_relative_member.json.gz')},'models':models,'old_four_selected_projection_transfer':'EXTERNAL_LABEL_AND_COEFFICIENT_DIMENSION_TRIANGULARITY; AUTHENTICATED_HSC_JMF_NOT_REPLAYED','old_zero_matter_h0_transfer':'NEW_MASS_HAS_P;NEW_Jh_VANISHES_AT_h0','new_zero_matter_h_and_full_source_extension_qualified':False,'six_selected_physical_fermionic_projections_compatible':True,'census':census,'free_parameters_not_selected':old['free_parameters_not_selected'],'physical_scheme_adopted':False,'full_QAP_E5A5_qualified':False,'scientific_acceptance':'NOT_PERFORMED'}
raw=(json.dumps(recipe,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(raw,mtime=0)
with (HERE/'selected_joint_vacuum_extension_v5.json.gz').open('xb') as f:f.write(blob)
out={'status':'QUALIFIED_EXACT_ONCE_SELECTED_JOINT_VACUUM_TANGENT_EXTENSION','new_ghost_identity_positions':positions,'census':census,'old_four_selected_projections_preserved_by_grade_and_support':True,'proper_JxCv_added_twice':False,'new_zero_matter_h_and_full_source_extension_qualified':False,'free_parameters_selected':False,'physical_scheme_adopted':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39','artifact_sha256':sha256(blob).hexdigest(),'artifact_raw_sha256':sha256(raw).hexdigest(),'elapsed_after_imports':time.perf_counter()-t}
print('RESULT '+json.dumps(out,sort_keys=True),flush=True)
