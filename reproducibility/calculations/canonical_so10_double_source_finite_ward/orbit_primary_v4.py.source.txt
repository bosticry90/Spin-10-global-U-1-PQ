from orbit_data_v4 import *
t=begin4('primary');P=get_parent();grads=[EL(P,f'JLp{i}') for i in range(45)];A,SP,Ci,Cp,sub=charts('primary');phy=read(PK/'frozen_a10_physical_reconciliation/full_primary.json');FM=dec(read(PK/'frozen_a10_e1_fermion/primary.json')['charts']['blocks']['heavy_dual']['field_embedding']);v=dec(phy['vacuum']['VEV']);frozen,ja,_=frozen_columns();out=[];off=0;phi=None;G=None
for sec,n in SECTORS:
 rho=list(map(dec,phy['representation_matrices'][sec]));raw=[s.SparseMatrix(n,n,{}) for _ in range(12)]+[tidy(sum((FM[b,a]*rho[b] for b in range(45) if FM[b,a]),s.SparseMatrix(n,n,{}))) for a in range(33)];rs=[tidy(sum((A[r,i]*raw[r] for r in range(45) if A[r,i]),s.SparseMatrix(n,n,{}))) for i in range(45)]
 for r in rs:zero(r+r.T)
 ev=s.SparseMatrix.vstack(*[(r*v[off:off+n,0]).T for r in rs]);out.append({'sector':sec,'generic_orbit_generators':list(map(enc,rs)),'evaluation_v0':enc(ev)});off+=n
 if sec=='Phi':phi=rs;G=s.SparseMatrix(33,33,lambda i,j:co(-(rs[12+i]*rs[12+j]).trace()))
 print('STAGE RAW_GENERIC_ORBIT',sec,flush=True)
left_a=(-1)**1;lorentz=-left_a;euclidean=left_a;assert lorentz==1 and euclidean==-1
finish4('primary',{'method':'raw_heavy_dual_canonical_source_transport_and_full_left_gradients','orbit':out,'source_gradients':[serial(p) for p in grads],'Phi_heavy_trace_Gram':enc(G),'generic_witness':contraction_witness(phi,grads),'h_source_Euler_signs':{'Lorentzian':lorentz,'Euclidean':euclidean},'Dh_GF_signs':{'Lorentzian':'1','Euclidean':'I'},'bJL_Ja_signs':{'Lorentzian':'-1','Euclidean':'I'},'all_new_w_dependence_in_Lambda_source_scalar_GF_only':True},t)
