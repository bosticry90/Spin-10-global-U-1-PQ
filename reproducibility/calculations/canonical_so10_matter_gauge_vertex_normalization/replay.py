"""MGN1 independent raw-coordinate Euler images and component field/source sums."""
from data import *
start=begin('replay')
def tidy(mat):return s.SparseMatrix(mat).applyfunc(s.simplify)
def zero(mat):assert not tidy(mat).todok()
pg=packed(CAL/'canonical_so10_pure_gauge_matter_vertex_assembly/replay_tables.json.gz');yv=packed(CAL/'canonical_so10_yukawa_dependent_gauge_vertices/replay_tables.json.gz');gkin=packed(CAL/'canonical_so10_fermion_gauge_kinetic_pole/replay_tables.json.gz');ykin=packed(CAL/'canonical_so10_fermion_yukawa_self_energy/replay_tables.json.gz');yct=packed(CAL/'canonical_so10_yukawa_carrier_transport/replay_tables.json.gz');T=list(map(dec,yct['Tminus']));H=dec(yct['H_new'])
loops={chir:[list(map(dec,pg['B_'+chir]))]+[[tidy(dec(a)+dec(b)) for a,b in zip(yv['outputs']['fermion'][chir][index],yv['outputs']['scalar'][chir][index])] for index in range(2)] for chir in ['left','right']};Aloop={chir:list(map(dec,pg['A_'+chir])) for chir in ['left','right']}
CL=[dec(gkin['gauge_kinetic_left'])]+[dec(row)/2 for row in ykin['internal_left']];CR=[dec(gkin['gauge_kinetic_right'])]+[dec(row)/2 for row in ykin['internal_right']];FL=[-mat/2 for mat in CL];FR=[-mat/2 for mat in CR]
oldpath=CAL/'canonical_so10_local_source_primitive/replay_v2_result.json';oldrec=read(oldpath.parent/'validation_receipt.json');assert oldrec['execution_state']=='COMPLETED' and oldrec['input_sha256'][str(oldpath)]==digest(oldpath);old=read(oldpath);assert old['all643_source_maps_match'] and not old['generator_or_scheme_adopted'] and not old['sourcefree_normalization_matches_known_complete_projector']
DB=[{} for _ in range(4)];ZA=[{} for _ in range(4)];counts={'B':0,'A':0}
for row in old['fixed_generator_components']['gauge']:
 source=next(name for name in row['word'] if name.startswith('JB'));field=next(name for name in row['word'] if name.startswith(('A','B')));assert len(row['word'])==2 and row['g']==2
 i,mu=map(int,source[2:].split('_'));j,nu=map(int,field[1:].split('_'));assert mu==nu;kind=field[0];counts[kind]+=1;target=DB if kind=='B' else ZA;target[mu][i,j]=target[mu].get((i,j),0)+s.sympify(row['coefficient'],locals=LOC)
DBm=[s.SparseMatrix(45,45,rows) for rows in DB];ZAm=[s.SparseMatrix(45,12,rows) for rows in ZA]
for mu in range(1,4):zero(DBm[mu]-DBm[0]);zero(ZAm[mu]-ZAm[0])
Q=dec(read(PK/'frozen_a10_physical_reconciliation/full_replay.json')['C3_plane_to_parent']);Qi=Q.inv();QH=Q[:,:12];RH=tidy((QH.T*QH).inv()*QH.T*H);zero(QH*RH-H)
raw_current=[tidy(sum((Q[d,a]*T[d] for d in range(45) if Q[d,a]),s.zeros(16))) for a in range(45)]
# Even B direction=-old coefficient. Old32 units become16 units through1/2.
raw_image={kind:{chir:[] for chir in ['left','right']} for kind in ['B','A']}
for kind,oldmap,dim in [('B',DB[0],45),('A',ZA[0],12)]:
 for chir in ['left','right']:
  charges=raw_current if chir=='left' else [-mat.T for mat in raw_current]
  for c in range(dim):
   current=s.zeros(16)
   for (i,j),value in oldmap.items():
    if j==c:current+=s.I*charges[i]*(-value/2)
   raw_image[kind][chir].append(tidy(current))
Bimage={chir:[tidy(sum((Qi[c,d]*raw_image['B'][chir][c] for c in range(45) if Qi[c,d]),s.zeros(16))) for d in range(45)] for chir in ['left','right']};Aimage={chir:[tidy(sum((RH[c,h]*raw_image['A'][chir][c] for c in range(12) if RH[c,h]),s.zeros(16))) for h in range(12)] for chir in ['left','right']}
image={chir:[] for chir in ['left','right']};fields={chir:[] for chir in ['left','right']};sources={chir:[] for chir in ['left','right']};kinetic={chir:[] for chir in ['left','right']}
for grade in range(3):
 fieldL=[];fieldR=[];sourceL=[];sourceR=[]
 for gen in T:
  left=s.zeros(16);right=s.zeros(16);sl=s.zeros(16);sr=s.zeros(16)
  for i in range(16):
   for j in range(16):
    for k in range(16):
     left[i,j]+=s.I*(FR[grade][k,i]*gen[k,j]+gen[i,k]*FL[grade][k,j]);right[i,j]+=-s.I*(FL[grade][k,i]*gen.T[k,j]+gen.T[i,k]*FR[grade][k,j])
     sl[i,j]+=-s.I*(gen[i,k]*FL[grade][k,j]-FL[grade][i,k]*gen[k,j]);sr[i,j]+=-s.I*((-gen.T[i,k])*FR[grade][k,j]-FR[grade][i,k]*(-gen.T[k,j]))
  fieldL.append(tidy(left));fieldR.append(tidy(right));sourceL.append(tidy(sl));sourceR.append(tidy(sr))
 for chir,field,src in [('left',fieldL,sourceL),('right',fieldR,sourceR)]:
  fields[chir].append(field);sources[chir].append(src);image[chir].append([tidy(mat+(Bimage[chir][c] if grade==0 else s.zeros(16))) for c,mat in enumerate(field)])
 kinetic['left'].append(tidy(-FL[grade]-FR[grade].T));kinetic['right'].append(tidy(-FR[grade]-FL[grade].T))
remainder={chir:[[tidy(a-b) for a,b in zip(lp,im)] for lp,im in zip(loops[chir],image[chir])] for chir in ['left','right']};Arem={chir:[tidy(a-b) for a,b in zip(Aloop[chir],Aimage[chir])] for chir in ['left','right']}
finish('replay',{'method':'independent_qualified_routes_raw_even_field_Euler_and_internal_component_congruence','loop_B':{chir:[list(map(enc,grade)) for grade in mats] for chir,mats in loops.items()},'image_B':{chir:[list(map(enc,grade)) for grade in mats] for chir,mats in image.items()},'field_only_B':{chir:[list(map(enc,grade)) for grade in mats] for chir,mats in fields.items()},'remainder_B':{chir:[list(map(enc,grade)) for grade in mats] for chir,mats in remainder.items()},'loop_A':{chir:list(map(enc,mats)) for chir,mats in Aloop.items()},'image_A':{chir:list(map(enc,mats)) for chir,mats in Aimage.items()},'remainder_A':{chir:list(map(enc,mats)) for chir,mats in Arem.items()},'source_image':{chir:[list(map(enc,grade)) for grade in mats] for chir,mats in sources.items()},'kinetic_image':{chir:list(map(enc,mats)) for chir,mats in kinetic.items()},'kinetic_loop':{'left':list(map(enc,CL)),'right':list(map(enc,CR))},'F_left':list(map(enc,FL)),'F_right':list(map(enc,FR)),'raw_DB':enc(DBm[0]),'raw_ZA':enc(ZAm[0]),'plane_DB':enc(tidy(Q*DBm[0]*Qi)),'plane_ZA':enc(tidy(Q*ZAm[0]*RH)),'background_RH':enc(RH),'old_gauge_rows':counts,'family_left':[enc(s.eye(3))]+ykin['family_left'],'family_right':[enc(s.eye(3))]+ykin['family_right'],'coefficient_carriers':['g10^2*I3','Y10dagY10','Y126dagY126'],'old_sourcefree_match':False,'source_qK_changed':False,'generator_or_scheme_adopted':False,'new_loop_integrals':0,'new_two_loop_integrals':0},start)
