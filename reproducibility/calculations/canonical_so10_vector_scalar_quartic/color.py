"""VSP1 literal full products versus independent seed Gram contractions."""
from data import *
def main():
    start=begin();role=sys.argv[1];assert role in ['primary','replay']
    d,rho,V,ad,Ps,frame,Q,Qi,E=inputs(role);I=s.eye(328)
    print('STAGE literal_color_and_normalized_H',flush=True)
    Ss=[tidy(sum((ad[h]*ad[h] for h in rr),s.SparseMatrix(45,45,{}))/len(rr)) for rr in [range(1),range(1,4),range(4,12)]]
    for P in Ps:
        for T in ad:zero(P*T-T*P)
    for S in Ss:
        for T in ad:zero(S*T-T*S)
    Ms=Ps+[tidy(P*S) for P in Ps for S in Ss]
    for M in Ms:zero(M-M.T)
    if role=='primary':
        pairs=set((int(a),int(b)) for M in Ms for a,b in M.todok())
        products={(a,b):rho[a]*rho[b] for a,b in sorted(pairs)}
    else:Ks=[R*E for R in rho]
    full=[];small=[];seed_offset=[sum(b['multiplicity'] for b in frame['blocks'][:j]) for j in range(35)]
    for j,M in enumerate(Ms):
        if role=='primary':
            L=tidy(-sum((z*products[int(a),int(b)] for (a,b),z in M.todok().items()),s.SparseMatrix(328,328,{})))
            H=tidy(E.H*L*E)
        else:
            H=tidy(sum((z*(Ks[a].H*Ks[b]) for (a,b),z in M.todok().items()),s.SparseMatrix(65,65,{})))
        bs=[tidy(H[o:o+b['multiplicity'],o:o+b['multiplicity']]) for b,o in zip(frame['blocks'],seed_offset)]
        S=s.diag(*bs);zero(H-S)
        rebuilt=tidy(Q*inflate(frame['blocks'],bs)*Qi)
        if role=='primary':zero(L-rebuilt)
        else:L=rebuilt;zero(E.H*L*E-H)
        zero(L-L.H)
        full.append(enc(L));small.append(list(map(enc,bs)))
        if j%5==4:print('STAGE color_operator_'+str(j+1),flush=True)
    cas=s.diag(*([10]*54+[s.Rational(25,2)]*252+[s.Rational(9,2)]*20+[0]*2))
    zero(sum((dec(z) for z in full[:5]),s.SparseMatrix(328,328,{}))-cas)
    fci=packed(CAL/'canonical_so10_finite_counterterm_insertion'/f'{role}_v3_tables.json.gz')
    soft=[];gauge=dec(d['vacuum']['orbit']);v=dec(d['vacuum']['VEV'])
    Soft=tidy(Q*inflate(frame['blocks'],[dec(b['soft']) for b in fci['blocks']])*Qi)
    for h in range(12):
        rh=tidy(sum((V[a,h]*rho[a] for a in range(45)),s.SparseMatrix(328,328,{})))
        zero(rh*v);zero(rh*Soft-Soft*rh);zero(gauge.T*rh*Soft)
    # Actual soft module contractions, not charges used as definitions.
    for j in [0,5,6,7]:
        vals=[]
        for b,bl in zip(frame['blocks'],fci['blocks']):
            P=dec(bl['soft']);Higgs=dec(bl['Higgs']);M=dec(small[j][bl['block']]);dim=b['dimension']
            target=s.Rational(9,10) if j==0 else (-s.Rational(1,2) if j==6 else 0)
            zero(P*M*P-target*Higgs);vals.append(str(red(dim*s.trace(P*M))))
        soft.append(vals)
    # Bad full-frame adjoint is not the inverse; expose this even if an invariant happens to commute.
    wrong=tidy(Q*inflate(frame['blocks'],list(map(dec,small[0])))*Q.H-dec(full[0]))
    assert wrong.todok()
    save(role,'color',{'schema':'VSP1_COLOR','full':full,'blocks':small,
      'operator_order':['A'+str(r) for r in range(5)]+['B'+str(r)+'_'+str(i) for r in range(5) for i in range(3)],
      'small_block_dimensions':[b['multiplicity'] for b in frame['blocks']],
      'full_domain':20*328**2,'full_nonzero':[len(x['entries']) for x in full],
      'M_color':list(map(enc,Ms)),'soft_actual_traces':soft,'soft_heavy_exchange_vertex_zero':True,
      'bad_Q_adjoint_control_changes':len(wrong.todok()),'finite_C1_qualified':False},start)
if __name__=='__main__':main()
