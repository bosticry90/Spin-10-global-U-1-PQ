from orbit_data_v4 import *
t=begin4('replay');phy=read(PK/'frozen_a10_physical_reconciliation/full_replay.json');EM=dec(read(PK/'frozen_a10_e5_ghost_normalization/replay.json')['ghost_metric']['real_heavy_frame']);v=dec(phy['vacuum']['VEV']);P=get_parent();grads=[{} for _ in range(45)]
for w,z in P.items():
 i,j=int(w[0][0][3:]),int(w[1][0][3:]);addto(grads[i],w[1:],z);addto(grads[j],(w[0],)+w[2:],-z)
grads=list(map(clean,grads));out=[];off=0;phi=None;G=None
for sec,n in SECTORS:
 rho=list(map(dec,phy['representation_matrices'][sec]));rs=[s.SparseMatrix(n,n,{}) for _ in range(12)]+[tidy(sum((EM[b,a]*rho[b] for b in range(45) if EM[b,a]),s.SparseMatrix(n,n,{}))) for a in range(33)];ev=s.SparseMatrix(45,n,{})
 for i,r in enumerate(rs):
  for (j,a),z in r.todok().items():ev[i,j]+=z*v[off+a,0]
 out.append({'sector':sec,'generic_orbit_generators':list(map(enc,rs)),'evaluation_v0':enc(tidy(ev))});off+=n
 if sec=='Phi':
  phi=rs;dd=[r.todok() for r in rs[12:]];G=s.SparseMatrix(33,33,lambda i,j:co(sum(z*dd[j].get(ab,0) for ab,z in dd[i].items())))
 print('STAGE PARENT_GENERIC_ORBIT',sec,flush=True)
# Independent right/left conversion for the odd a derivative of an even Sh.
right_sign=1;left_conversion=-1;left=right_sign*left_conversion
finish4('replay',{'method':'orthonormal_parent_representation_signed_pair_gradients_and_entry_Gram','orbit':out,'source_gradients':[serial(p) for p in grads],'Phi_heavy_trace_Gram':enc(G),'generic_witness':contraction_witness(phi,grads),'h_source_Euler_signs':{'Lorentzian':-left,'Euclidean':left},'Dh_GF_signs':{'Lorentzian':'1','Euclidean':'I'},'bJL_Ja_signs':{'Lorentzian':'-1','Euclidean':'I'},'all_new_w_dependence_in_Lambda_source_scalar_GF_only':True},t)
