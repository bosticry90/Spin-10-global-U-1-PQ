"""MGN1 measured five-family sum, then literal old image and Nambu congruence."""
from data import *
start=begin('primary')
def tidy(mat):return s.SparseMatrix(mat).applyfunc(s.simplify)
def zero(mat):assert not tidy(mat).todok()
pg=packed(CAL/'canonical_so10_pure_gauge_matter_vertex_assembly/primary_tables.json.gz');yv=packed(CAL/'canonical_so10_yukawa_dependent_gauge_vertices/primary_tables.json.gz');gkin=packed(CAL/'canonical_so10_fermion_gauge_kinetic_pole/primary_tables.json.gz');ykin=packed(CAL/'canonical_so10_fermion_yukawa_self_energy/primary_tables.json.gz');yct=packed(CAL/'canonical_so10_yukawa_carrier_transport/primary_tables.json.gz');T=list(map(dec,yct['Tminus']));H=dec(yct['H_new'])
loop={chir:[list(map(dec,pg['B_'+chir]))]+[[tidy(dec(a)+dec(b)) for a,b in zip(yv['outputs']['fermion'][chir][index],yv['outputs']['scalar'][chir][index])] for index in range(2)] for chir in ['left','right']}
Aloop={chir:list(map(dec,pg['A_'+chir])) for chir in ['left','right']}
CL=[dec(gkin['gauge_kinetic_left'])]+[dec(row)/2 for row in ykin['internal_left']];CR=[dec(gkin['gauge_kinetic_right'])]+[dec(row)/2 for row in ykin['internal_right']];FL=[-mat/2 for mat in CL];FR=[-mat/2 for mat in CR]
# Only after assembling every loop family, read the fixed older candidate.
oldpath=CAL/'canonical_so10_local_source_primitive/primary_v2_result.json';oldrec=read(oldpath.parent/'validation_receipt.json');assert oldrec['execution_state']=='COMPLETED' and oldrec['input_sha256'][str(oldpath)]==digest(oldpath);old=read(oldpath)
assert old['all643_source_maps_match'] and not old['generator_or_scheme_adopted'] and not old['sourcefree_normalization_matches_known_complete_projector']
DB=[s.zeros(45) for _ in range(4)];ZA=[s.zeros(45,12) for _ in range(4)];rows=old['fixed_generator_components']['gauge'];counts={'B':0,'A':0}
for row in rows:
 word=row['word'];sources=[v for v in word if v.startswith('JB')];fields=[v for v in word if v.startswith(('A','B'))];assert len(word)==2 and len(sources)==len(fields)==1 and row['g']==2
 i,mu=map(int,sources[0][2:].split('_'));j,nu=map(int,fields[0][1:].split('_'));assert mu==nu;kind=fields[0][0];counts[kind]+=1
 target=DB if kind=='B' else ZA;target[mu][i,j]+=s.sympify(row['coefficient'],locals=LOC)
for m in range(1,4):zero(DB[m]-DB[0]);zero(ZA[m]-ZA[0])
Q=dec(read(PK/'frozen_a10_physical_reconciliation/full_primary.json')['C3_plane_to_parent']);Qi=Q.inv();QH=Q[:,:12];RH=tidy((QH.T*QH).inv()*QH.T*H);zero(QH*RH-H);DBplane=tidy(Q*DB[0]*Qi);ZAplane=tidy(Q*ZA[0]*RH)
Bimage=[tidy(-s.I*sum((DBplane[d,c]*T[d] for d in range(45) if DBplane[d,c]),s.zeros(16))/2) for c in range(45)];Aimage=[tidy(-s.I*sum((ZAplane[d,h]*T[d] for d in range(45) if ZAplane[d,h]),s.zeros(16))/2) for h in range(12)]
# SMA1's actual split-Clifford charge transpose proves the chiral congruence.
pa=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)];g4=[s.kronecker_product(pa[1],mat) for mat in pa]+[s.kronecker_product(pa[0],s.eye(2))];g8=[s.kronecker_product(mat,pa[2]) for mat in g4]+[s.kronecker_product(s.eye(4),mat) for mat in pa[:2]];C8=g8[0]*g8[2]*g8[5];charge=s.kronecker_product(C8,pa[1]);Ci=charge.inv();chi=s.kronecker_product(s.diag(1,1,-1,-1),s.eye(4));projectors=[(s.eye(16)+chi)/2,(s.eye(16)-chi)/2];spin_positions=0
for gam in [s.kronecker_product(mat,s.eye(2)) for mat in g8[:4]]:
 for outer in range(2):
  for inner in range(2):
   actual=Ci*projectors[outer].T*charge*gam*projectors[inner];target=gam*projectors[inner] if outer!=inner else s.zeros(16);zero(actual-target);spin_positions+=256
image={chir:[] for chir in ['left','right']};source={chir:[] for chir in ['left','right']};kinetic={chir:[] for chir in ['left','right']};field_only={chir:[] for chir in ['left','right']};tau=s.Symbol('tau');I=s.eye(16)
for grade in range(3):
 lfield=[tidy(s.I*(FR[grade].T*gen+gen*FL[grade])) for gen in T];rfield=[tidy(-s.I*(FL[grade].T*gen.T+gen.T*FR[grade])) for gen in T];field_only['left'].append(lfield);field_only['right'].append(rfield)
 image['left'].append([tidy(mat+(Bimage[c] if grade==0 else s.zeros(16))) for c,mat in enumerate(lfield)]);image['right'].append([tidy(mat+(-Bimage[c].T if grade==0 else s.zeros(16))) for c,mat in enumerate(rfield)])
 source['left'].append([tidy(-((I-tau*FL[grade])*s.I*gen*(I+tau*FL[grade])).diff(tau).subs(tau,0)) for gen in T]);source['right'].append([tidy(-((I-tau*FR[grade])*(-s.I*gen.T)*(I+tau*FR[grade])).diff(tau).subs(tau,0)) for gen in T])
 kinetic['left'].append(tidy(-FL[grade]-FR[grade].T));kinetic['right'].append(tidy(-FR[grade]-FL[grade].T));zero(((I-tau*FL[grade])*(I+tau*FL[grade])).diff(tau).subs(tau,0))
remainder={chir:[[tidy(a-b) for a,b in zip(la,im)] for la,im in zip(loop[chir],image[chir])] for chir in ['left','right']};Arem={'left':[tidy(a-b) for a,b in zip(Aloop['left'],Aimage)],'right':[tidy(a+b.T) for a,b in zip(Aloop['right'],Aimage)]}
finish('primary',{'method':'five_measured_families_then_literal_old_plane_image_and_Nambu_congruence','loop_B':{chir:[list(map(enc,grade)) for grade in loops] for chir,loops in loop.items()},'image_B':{chir:[list(map(enc,grade)) for grade in mats] for chir,mats in image.items()},'field_only_B':{chir:[list(map(enc,grade)) for grade in mats] for chir,mats in field_only.items()},'remainder_B':{chir:[list(map(enc,grade)) for grade in mats] for chir,mats in remainder.items()},'loop_A':{chir:list(map(enc,mats)) for chir,mats in Aloop.items()},'image_A':{'left':list(map(enc,Aimage)),'right':[enc(-mat.T) for mat in Aimage]},'remainder_A':{chir:list(map(enc,mats)) for chir,mats in Arem.items()},'source_image':{chir:[list(map(enc,grade)) for grade in mats] for chir,mats in source.items()},'kinetic_image':{chir:list(map(enc,mats)) for chir,mats in kinetic.items()},'kinetic_loop':{'left':list(map(enc,CL)),'right':list(map(enc,CR))},'F_left':list(map(enc,FL)),'F_right':list(map(enc,FR)),'raw_DB':enc(DB[0]),'raw_ZA':enc(ZA[0]),'plane_DB':enc(DBplane),'plane_ZA':enc(ZAplane),'background_RH':enc(RH),'old_gauge_rows':counts,'spin_congruence_positions_checked':spin_positions,'family_left':[enc(s.eye(3))]+ykin['family_left'],'family_right':[enc(s.eye(3))]+ykin['family_right'],'coefficient_carriers':['g10^2*I3','Y10dagY10','Y126dagY126'],'old_sourcefree_match':False,'source_qK_changed':False,'generator_or_scheme_adopted':False,'new_loop_integrals':0,'new_two_loop_integrals':0},start)
