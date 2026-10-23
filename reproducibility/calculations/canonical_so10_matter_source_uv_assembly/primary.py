"""MSU1 literal fixed old ghost generator and direct raw-coordinate new image."""
from data import *
start=begin('primary');oldpath=CAL/'canonical_so10_local_source_primitive/primary_v2_result.json';old=read(oldpath);receipt=read(oldpath.parent/'validation_receipt.json');assert receipt['execution_state']=='COMPLETED' and receipt['input_sha256'][str(oldpath)]==digest(oldpath)
assert old['all643_source_maps_match'] and not old['generator_or_scheme_adopted'] and not old['sourcefree_normalization_matches_known_complete_projector']
Q=dec(read(PK/'frozen_a10_physical_reconciliation/full_primary.json')['C3_plane_to_parent']);Qi=Q.inv();T=list(map(dec,packed(CAL/'canonical_so10_yukawa_carrier_transport/primary_tables.json.gz')['Tminus']));TR=[sum((Q[d,a]*T[d] for d in range(45) if Q[d,a]),s.zeros(16)) for a in range(45)]
def tidy(M):return s.SparseMatrix(M).applyfunc(s.simplify)
norm={};left={};right={};counts={}
for label,gp in [('leading_ghost',1),('ordinary_ghost',2)]:
 raw=s.zeros(45);rows=old['fixed_generator_components'][label];counts[label]=len(rows)
 for r in rows:
  assert r['g']==gp and len(r['word'])==2;c,j=r['word'];assert c.startswith('C') and j.startswith('JC') and '__' not in c
  co=s.sympify(r['coefficient'],locals={'reference_width_H':eta,'reference_width_M':xi});assert co.free_symbols<={eta,xi};raw[int(j[2:]),int(c[1:])]+=co
 raw=s.SparseMatrix(raw);norm[label]={'raw':enc(raw),'plane':enc(Q*raw*Qi)}
 rawL=[sum((-s.I*raw[a,b]*TR[a]/2 for a in range(45) if raw[a,b]),s.zeros(16)) for b in range(45)]
 left[label]=[tidy(sum((Qi[b,c]*rawL[b] for b in range(45) if Qi[b,c]),s.zeros(16))) for c in range(45)];right[label]=[-A.T for A in left[label]]
field=packed(CAL/'canonical_so10_matter_field_source_image/primary_tables.json.gz');EL=list(map(dec,field['source_pole_image_left']));ER=list(map(dec,field['source_pole_image_right']));fullL=[tidy(a+b) for a,b in zip(left['ordinary_ghost'],EL)];fullR=[tidy(a+b) for a,b in zip(right['ordinary_ghost'],ER)]
finish('primary',{'method':'literal_old_fixed_generator_raw_coordinate_new_matter_image','old_generator_counts':counts,'ghost_matrices':norm,'auxiliary_left':list(map(enc,left['leading_ghost'])),'auxiliary_right':list(map(enc,right['leading_ghost'])),'ordinary_ghost_left':list(map(enc,left['ordinary_ghost'])),'ordinary_ghost_right':list(map(enc,right['ordinary_ghost'])),'ordinary_complete_left':list(map(enc,fullL)),'ordinary_complete_right':list(map(enc,fullR)),'old_complete_source_maps_match':True,'old_sourcefree_normalization_match':False,'old_quantum_A5_obligations':old['quantum_A5_obligations'],'pole_unit_factor':'1/2','new_loop_integrals':0,'source_qK_changed':False,'generator_or_scheme_adopted':False},start)
