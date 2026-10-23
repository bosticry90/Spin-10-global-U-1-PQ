"""MSU1 independent actual-plane Lie reconstruction of the fixed ghost maps."""
from data import *
from collections import defaultdict
start=begin('replay')
Q=dec(read(PK/'frozen_a10_physical_reconciliation/full_replay.json')['C3_plane_to_parent']);Qi=Q.inv();yc=packed(CAL/'canonical_so10_yukawa_carrier_transport/replay_tables.json.gz');T=list(map(dec,yc['Tminus']));H=dec(yc['H_new']);f={(a,b,c):s.sympify(v) for a,b,c,v in packed(HERE/'qualified_lie_constants.json.gz')['plane_f']};FA=[s.SparseMatrix(45,45,{(c,b):v for (aa,b,c),v in f.items() if aa==a}) for a in range(45)]
def tidy(M):return s.SparseMatrix(M).applyfunc(s.simplify)
CA=tidy(-sum((A*A for A in FA),s.zeros(45)));FH=[tidy(sum((H[a,h]*FA[a] for a in range(45) if H[a,h]),s.zeros(45))) for h in range(12)];CH=tidy(-sum((A*A for A in FH),s.zeros(45)));PM=s.eye(45)-H*H.T
N1=tidy(xi*PM*(CA-2*CH)*PM);N2=tidy(-eta*CH-xi*PM*(CA-CH)*PM);norm={};left={};right={}
for label,N in [('leading_ghost',N1),('ordinary_ghost',N2)]:
 norm[label]={'raw':enc(Qi*N*Q),'plane':enc(N)}
 left[label]=[tidy(-s.I*sum((N[a,c]*T[a] for a in range(45) if N[a,c]),s.zeros(16))/2) for c in range(45)];right[label]=[-A.T for A in left[label]]
field=packed(CAL/'canonical_so10_matter_field_source_image/replay_tables.json.gz');EL=list(map(dec,field['source_pole_image_left']));ER=list(map(dec,field['source_pole_image_right']));fullL=[tidy(a+b) for a,b in zip(left['ordinary_ghost'],EL)];fullR=[tidy(a+b) for a,b in zip(right['ordinary_ghost'],ER)]
finish('replay',{'method':'qualified_scalar_Lie_constants_actual_H_projectors_and_current_images','ghost_matrices':norm,'adjoint_Casimir':enc(CA),'H_adjoint_Casimir':enc(CH),'auxiliary_left':list(map(enc,left['leading_ghost'])),'auxiliary_right':list(map(enc,right['leading_ghost'])),'ordinary_ghost_left':list(map(enc,left['ordinary_ghost'])),'ordinary_ghost_right':list(map(enc,right['ordinary_ghost'])),'ordinary_complete_left':list(map(enc,fullL)),'ordinary_complete_right':list(map(enc,fullR)),'pole_unit_factor':'1/2','new_loop_integrals':0,'source_qK_changed':False,'generator_or_scheme_adopted':False},start)
