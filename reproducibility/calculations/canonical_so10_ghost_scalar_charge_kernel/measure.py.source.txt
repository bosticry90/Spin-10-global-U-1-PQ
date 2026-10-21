"""GSK1 orthonormal/highest-state vs full-index/all-irrep-state traces."""
from data import *
def main():
    role=sys.argv[1];assert role in ['primary','replay'];start=begin('preparation.json',600)
    values,fci,scm=inputs(role);action,rho,V,ad,Ps,frame,Q,Qi,E=values;B=basis(frame);assert len(B)==177
    O=dec(action['vacuum']['orbit'])
    Cv=[tidy(-sum((ad[h]*ad[h] for h in hs),s.SparseMatrix(45,45,{}))/len(hs)) for hs in [range(1),range(1,4),range(4,12)]]
    for C in Cv:
        zero(C-C.T)
        for P in Ps:zero(C*P-P*C)
        for A in ad:zero(C*A-A*C)
    for h in range(12):
        Rh=sum((V[a,h]*rho[a] for a in range(45) if V[a,h]),s.SparseMatrix(328,328,{}))
        zero(Rh*O-O*ad[h])
    T=tidy(tensor_table() if role=='primary' else action_tensor(action,rho));assert len(T.todok())==10524
    if role=='primary':
        G=load('gsk_gss',CAL/'canonical_so10_ghost_scalar_support/data.py');Us=[None]+[G.orthogonal_basis(P) for P in Ps[1:]]
        C=[None]+[[tidy(U.T*M*U) for M in Cv] for U in Us[1:]]
        X=Xcolumns(tidy(T*E))
        cs=[[s.sympify(v) for v in row] for row in scm['scalar_Casimir_averages']]
    else:
        Us=Ps;C=[None]+[Cv for _ in range(4)];X=Xcolumns(tidy(T*Q))
        cs=[[red(6*z/b['dimension']) for z in weights(b['label'])] for b in frame['blocks']]
    print('STAGE '+role+'_actual_tensor_and_charge_matrices',flush=True)
    # Project before taking ordered traces. Keep the matrix Cv inside each sector.
    blocks={}
    for r in range(1,5):
        for t in range(1,5):
            blocks[r,t]=[tidy((Us[r].T*M*Us[t]) if role=='primary' else (Ps[r]*M*Ps[t])) for M in X]
    print('STAGE '+role+'_all_projected_ghost_pairs',flush=True)
    ops={};wrong={}
    for r in range(1,5):
        for t in range(r,5):
            direct=[[] for _ in range(7)];bad=[]
            for alpha,b in enumerate(frame['blocks']):
                m=b['multiplicity'];dim=b['dimension'];offset=b['seed_offset'] if role=='primary' else b['offset']
                for i in range(m):
                    for jj in range(m):
                        sums=[s.S.Zero]*7;bad0=s.S.Zero
                        for n in range(1 if role=='primary' else dim):
                            a=offset+(0 if role=='primary' else n*m)+i;c=offset+(0 if role=='primary' else n*m)+jj
                            forms=shapes((C[r],C[t]),blocks[r,t][a].conjugate(),blocks[t,r][a].conjugate())
                            v=coefficient(forms,blocks[t,r][c],blocks[r,t][c])
                            factor=s.S.One if role=='primary' else 1/(s.Integer(dim)*s.sympify(b['state_norms'][n]))
                            sums=[u+factor*z for u,z in zip(sums,v)]
                            if role=='replay':bad0+=v[0]/s.Integer(dim)
                        for k,z in enumerate(sums):direct[k].append(red(z))
                        if role=='replay':bad.append(red(bad0))
            key=f'{r},{t}';ops[key]=direct
            if role=='replay':wrong[key]=bad
            if r!=t:ops[f'{t},{r}']=[direct[0],*direct[4:7],*direct[1:4]]
            print('STAGE '+role+'_ordered_pair_'+key,flush=True)
    for r in range(5):
        for t in range(5):
            if r==0 or t==0:ops[f'{r},{t}']=[[s.S.Zero]*177 for _ in range(7)]
    cas_av=[[str(red(s.trace(P*C)/s.trace(P))) for C in Cv] for P in Ps]
    deviations={}
    for r in range(1,5):
        for t in range(1,5):
            vecs=ops[f'{r},{t}']
            deviations[f'{r},{t}']=[sum(red(v-s.sympify(cas_av[r][i])*raw)!=0 for raw,v in zip(vecs[0],vecs[1+i])) for i in range(3)]
    out={'schema':'GSK1','basis':[list(z) for z in B],'operators':{k:[[str(z) for z in v] for v in vv] for k,vv in ops.items()},
      'operator_names':['raw','ghost_first_U1','ghost_first_SU2','ghost_first_SU3','ghost_second_U1','ghost_second_SU2','ghost_second_SU3'],
      'scalar_Casimir_averages':[[str(z) for z in row] for row in cs],'ghost_Casimir_operators':list(map(enc,Cv)),
      'mass_sector_averaged_Casimir':cas_av,'averaged_Casimir_change_positions':deviations,
      'probes':probes(ops,frame,B,cs,fci),'actual_Rh_O_intertwiners_checked':12,
      'domain_positions':25*7*177,'scalar_dimension':328,'classes':35,'full_model_amplitude_calculated':False,
      'scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED'}
    if role=='replay':out['wrong_dual_raw']={k:[str(z) for z in v] for k,v in wrong.items()}
    save(role,out,start)
if __name__=='__main__':main()
