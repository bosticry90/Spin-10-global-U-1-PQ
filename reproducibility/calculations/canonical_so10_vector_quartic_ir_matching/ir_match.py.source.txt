"""Actual opened curvature kernel and restricted-tree quartic IR matching."""
from pathlib import Path
from itertools import combinations
from functools import lru_cache
from hashlib import sha256
import gzip,json,os,sys,threading,time
import sympy as s
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CAL=ROOT/'calculations'
PAIRS=list(combinations(range(10),2));d=s.Symbol('d',positive=True)
z,ld,zz=s.symbols('z ld zeta2',real=True);hs=s.symbols('h1:5',real=True)
LOC={str(x):x for x in [d,z,ld,zz,*hs]}
ks=[d,s.Rational(1,200),s.Rational(1,40),s.Rational(5,12),s.Rational(253,600)];logs=[ld,*hs]
@lru_cache(None)
def clean(v):return s.cancel(s.expand(v))
def tidy(M):return s.SparseMatrix(M).applyfunc(clean)
def zero(M):assert not tidy(M).todok()
def packed(p):return json.loads(gzip.decompress(p.read_bytes()))
def mat(x):return s.SparseMatrix(*x['shape'],{(i,j):s.sympify(v) for i,j,v in x['entries']})
def enc(M):
    M=tidy(M);return {'shape':list(map(int,M.shape)),'entries':[[int(i),int(j),str(v)] for (i,j),v in sorted(M.todok().items())]}
def vec(entries):return s.SparseMatrix(45,1,{(PAIRS.index(pair),0):v for pair,v in entries})

def light_basis():
    columns=[vec([((2*j,2*j+1),s.Integer(v)/s.sqrt(30)) for j,v in enumerate([-2,-2,-2,3,3])]),
      vec([((6,7),1/s.sqrt(2)),((8,9),-1/s.sqrt(2))]),
      vec([((6,9),-1/s.sqrt(2)),((7,8),1/s.sqrt(2))]),
      vec([((6,8),1/s.sqrt(2)),((7,9),1/s.sqrt(2))]),
      vec([((0,1),1/s.sqrt(2)),((2,3),-1/s.sqrt(2))]),
      vec([((0,1),1/s.sqrt(6)),((2,3),1/s.sqrt(6)),((4,5),-2/s.sqrt(6))])]
    for p,q in combinations(range(3),2):
        columns += [vec([((2*p,2*q+1),-1/s.sqrt(2)),((2*p+1,2*q),1/s.sqrt(2))]),
                    vec([((2*p,2*q),1/s.sqrt(2)),((2*p+1,2*q+1),1/s.sqrt(2))])]
    return tidy(s.SparseMatrix.hstack(*columns))

def tree(B,P0,f,adj):
    V=light_basis();zero(V.T*V-s.eye(12));zero(V*V.T-P0)
    assert isinstance(B['orbit'],list) and len(B['orbit'])==424
    O=s.SparseMatrix(328,45,{(i,j):s.sympify(v) for i,j,v in B['orbit']});zero(O*V)
    fh={};adH=[];parent=[]
    for i in range(12):
        h=tidy(sum((V[a,i]*adj[a] for a in range(45) if V[a,i]),s.zeros(45)))
        image=tidy(h*V);zero((s.eye(45)-P0)*image)
        C=tidy(V.T*image);adH.append(C);parent.append(h)
        for (out,j),value in C.todok().items():fh[i,int(j),int(out)]=value
    for (a,b,c),v in fh.items():assert clean(v+fh.get((b,a,c),0))==0 and clean(v-fh.get((b,c,a),0))==0
    FeH=[s.SparseMatrix(12,12,{(a,b):v for (a,b,k),v in fh.items() if k==e}) for e in range(12)]
    eft=[]
    for idx in [0,1,4]:
        T=adH[idx];X=-sum((s.trace(T*T*F*F) for F in FeH),s.Integer(0))
        L=sum((sum((v*T[a,b] for (a,b),v in F.todok().items()),s.Integer(0))**2 for F in FeH),s.Integer(0))
        Y=-sum((s.trace(F*T*F*T) for F in FeH),s.Integer(0))
        eft.append({k:str(clean(v)) for k,v in [('X',X),('L',L),('Y',Y),('Z',L-Y)]})
    assert [clean(-s.trace(adH[i]*adH[i])) for i in [0,1,4]]==[0,2,3]
    return V,fh,eft,[parent[i] for i in [0,1,4]]

def slot_matrices(M,fused):
    choices=list(combinations(range(4),2));remaining=[[k for k in range(4) if k not in ij] for ij in choices]
    md=M.todok();out=[s.SparseMatrix(45,45,{}) for _ in range(6)]
    for colors,value in fused.items():
        for j,((a,b),(c,e)) in enumerate(zip(choices,remaining)):
            v=md.get((colors[c],colors[e]),0)
            if v:out[j][colors[a],colors[b]]+=value*v
    return list(map(tidy,out))

def density(slots,L,alpha,beta):
    N=L.rows;out=s.zeros(45);choices=list(combinations(range(4),2))
    for S,(i,j) in zip(slots,choices):
        rem=[k for k in range(4) if k not in [i,j]];weights=[]
        for a,b in [(alpha,beta),(beta,alpha)]:
            w=0
            for mu in range(N):
                for nu in range(N):
                    lor=[mu,nu,mu,nu]
                    if lor[i]==a and lor[j]==b:w+=L[lor[rem[0]],lor[rem[1]]]
            weights.append(w)
        out+=s.Rational(1,4)*(weights[0]*S+weights[1]*S.T)
    return tidy(out)

def actual_operators(role,B,P,f,Fe,probes):
    def K(M):return tidy(-sum((F*M*F for F in Fe),s.zeros(45)))
    def J(M):
        return tidy(sum((F*sum((v*M[a,b] for (a,b),v in F.todok().items()),s.Integer(0)) for F in Fe),s.zeros(45)))
    fused={}
    if role=='replay':
        for F in Fe:
            for (a,b),v in F.todok().items():
                for (c,e),u in F.todok().items():fused[a,b,c,e]=fused.get((a,b,c,e),0)+u*v
        fused={k:clean(v) for k,v in fused.items() if clean(v)}
    mass=[]
    for Q in P:
        if role=='primary':M=K(Q)
        else:
            slots=slot_matrices(Q,fused);M=tidy(density(slots,s.eye(4),0,0)/3)
            zero(density(slots,s.eye(6),0,0)-5*M)
        mass.append(M)
    first=[];second=[];traces=[]
    for i,T in enumerate(probes):
        print('STAGE curvature_'+role+'_'+str(i),flush=True);bb=[];cc=[];row=[]
        for r,Q in enumerate(P):
            U=tidy(Q*T);S=tidy(Q*T*T)
            if role=='primary':b=tidy(J(U)+K(U));c=K(S)
            else:
                su=slot_matrices(U,fused);ss=slot_matrices(S,fused);b=None;c=None
                for N in [4,6]:
                    F=s.zeros(N);F[0,1]=1;F[1,0]=-1;L2=s.eye(N)/6+2*F*F
                    bN=density(su,F,0,1)
                    if b is None:b=bN
                    zero(bN-b);zero(density(su,F,1,0)+b)
                    cN=tidy(-s.Rational(2,3)*density(ss,L2,0,0)) if N==4 else c
                    if c is None:c=cN
                    zero(density(ss,L2,0,0)-s.Rational(N-13,6)*c)
                    zero(density(ss,L2,2,2)-s.Rational(N-25,6)*c)
            zero(b+b.T);zero(c-c.T);bb.append(b);cc.append(c)
            a=clean(s.trace(P[0]*T*T*mass[r]));v=clean(s.trace(P[0]*T*b));u=clean(s.trace(P[0]*c))
            row.append([str(a),str(v),str(u)])
        first.append(bb);second.append(cc);traces.append(row)
    return mass,first,second,traces

def coeff(x,zv,r,t):
    j=2*z-logs[r]-logs[t];ratio=ks[t]/ks[r]
    return {-2:-12*zv,-1:-30*x*ratio-12*zv*j,
            0:x*ratio*(-13-30*j)-12*zv*(j*j/2+zz)}

def polynomial(role,old,eft,traces):
    rows=[]
    for i,group in enumerate(['U1','SU2','SU3']):
        mixed={q:0 for q in [-2,-1,0]}
        for r in range(1,5):
            a,b,c=list(map(s.sympify,traces[i][r]))
            # Mixed closure, from the independently opened kernel. In coeff's
            # convention the two BB orderings contribute -24 Z0r = +24 b.
            A=coeff(a,-b,0,r);C=coeff(c,0,r,0);BB=coeff(0,-b,0,r)
            for q in mixed:mixed[q]+=A[q]+C[q]+BB[q]
        pure=coeff(s.sympify(eft[i]['X']),s.sympify(eft[i]['Z']),0,0)
        full={int(q):s.sympify(v,locals=LOC) for q,v in old['amplitudes'][i]['Laurent'].items()}
        if role=='primary':hard={q:s.expand(full[q]-mixed[q]-pure[q]) for q in full}
        else:
            X=old['color'][i]['X'];Z=old['color'][i]['Z'];hard={q:0 for q in full}
            for r in range(1,5):
                for t in range(1,5):
                    c=coeff(s.sympify(X[r][t]),s.sympify(Z[r][t]),r,t)
                    for q in hard:hard[q]+=c[q]
            hard={q:s.expand(v) for q,v in hard.items()}
        for q,v in hard.items():
            assert not ({d,ld}&v.free_symbols)
            assert clean(full[q]-mixed[q]-pure[q]-v)==0
        # Genuine negative controls; hypercharge's pure-light graph is0.
        assert any(clean(v)!=0 for v in mixed.values())
        if i>0:
            assert any(clean(v)!=0 for v in pure.values())
            assert s.expand(full[0]-mixed[0]/2-pure[0]-hard[0])!=0
        rows.append({'group':group,'full':{str(q):str(s.expand(v)) for q,v in full.items()},
          'mixed_closure':{str(q):str(s.expand(v)) for q,v in mixed.items()},
          'EFT_pure_light':{str(q):str(s.expand(v)) for q,v in pure.items()},
          'hard_bare_remainder':{str(q):str(s.expand(v)) for q,v in hard.items()}})
    return rows

def main():
    role=sys.argv[1];assert role in ['primary','replay'];start=time.perf_counter()
    timer=threading.Timer(180,lambda:os._exit(124));timer.daemon=True;timer.start()
    B=packed(CAL/'canonical_so10_background_threshold_inputs'/f'{role}_tables.json.gz')
    P=list(map(mat,packed(CAL/'canonical_so10_width_hard_projection'/f'{role}_tables.json.gz')['projectors']))
    old=packed(CAL/'canonical_so10_vector_quartic_primitive'/f'{role}_v2_tables.json.gz')
    f={(a,b,c):s.sympify(v) for a,b,c,v in B['f']}
    Fe=[s.SparseMatrix(45,45,{(a,b):v for (a,b,k),v in f.items() if k==e}) for e in range(45)]
    adj=[s.SparseMatrix(45,45,{(out,b):v for (a,b,out),v in f.items() if a==h}) for h in range(45)]
    print('STAGE restricted_tree_'+role,flush=True);V,fh,eft,probes=tree(B,P[0],f,adj)
    mass,first,second,traces=actual_operators(role,B,P,f,Fe,probes)
    for i in range(3):
        for r in range(5):
            a,b,c=list(map(s.sympify,traces[i][r]));assert clean(a-s.sympify(old['color'][i]['X'][0][r]))==0
            assert clean(b+s.sympify(old['color'][i]['Z'][0][r]))==0
            assert clean(c-s.sympify(old['color'][i]['X'][r][0]))==0
        for key in ['X','L','Y','Z']:assert clean(s.sympify(eft[i][key])-s.sympify(old['color'][i][key][0][0]))==0
    polys=polynomial(role,old,eft,traces)
    payload={'schema':'C1_VECTOR_QUARTIC_IR_MATCHING_TABLES_V1','light_embedding':enc(V),
      'restricted_f':[[a,b,c,str(v)] for (a,b,c),v in sorted(fh.items())],'restricted_f_shape':[12,12,12],
      'mass_operators':list(map(enc,mass)),'first_curvature_operators':[list(map(enc,r)) for r in first],
      'second_curvature_operators':[list(map(enc,r)) for r in second],
      'closure_traces':traces,'EFT_color':eft,'polynomials':polys,
      'normalization':'output Lambda2/g10**2, ell=hbar/(16*pi**2), same VQP1 convention',
      'UV_forests_or_complete_C1_qualified':False,'finite_conditions_adopted':False}
    raw=json.dumps(payload,sort_keys=True,separators=(',',':')).encode();data=gzip.compress(raw,mtime=0)
    with (HERE/(role+'_tables.json.gz')).open('xb') as out:out.write(data)
    result={'schema':'C1_VECTOR_QUARTIC_IR_MATCHING_NATIVE_V1','execution_state':'COMPLETED','route':role,
      'open_45x45_matrices':35,'light_brackets_checked':144,'restricted_nonzero_f':len(fh),
      'hard_double_poles':[p['hard_bare_remainder']['-2'] for p in polys],
      'tables_sha256':sha256(raw).hexdigest(),'packed_sha256':sha256(data).hexdigest(),
      'table_bytes':len(raw),'packed_bytes':len(data),'elapsed_after_imports':time.perf_counter()-start}
    print('RESULT '+json.dumps(result,sort_keys=True,separators=(',',':')),flush=True);timer.cancel()
if __name__=='__main__':main()
