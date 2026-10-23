"""FCT1 parent Hessian matrix log, positive bubble integrals and raised tensors."""
from data import *
start=begin('replay');mp.mp.dps=100
frame=packed(CAL/'canonical_so10_scalar_sm_frame/replay_tables.json.gz')
fci=packed(CAL/'canonical_so10_finite_counterterm_insertion/replay_v3_tables.json.gz')
charges=packed(CAL/'canonical_so10_scalar_quartic_charge_projection/replay_tables.json.gz')['class_values']
from inputs import coeffs
cc=coeffs()[1];scalar=[mp.mpf(0)]*3;TS=[s.S(0)]*3;count=0
for n,b in enumerate(fci['blocks']):
    H=s.zeros(b['H']['shape'][0])
    for slot,block in zip(frame['slots'],frame['parent_blocks'][n]):
        key,_,part=slot.partition(':');c=s.im(cc[key]) if part=='im' else s.re(cc[key])
        if c and block['entries']:H+=c*dec(block)
    H=tidy(H);zero(H-dec(b['H']));P=dec(b['physical']);zero(H*(s.eye(H.rows)-P));zero(P*P-P)
    rank=int(red(s.trace(P)));weight=b['dimension'];count+=weight*rank
    A=mat(H+s.eye(H.rows)-P);Pm=mat(P);ev,V=mp.eighe(A);assert min(ev)>0
    logA=V*mp.diag([mp.log(ev[j]) for j in range(A.rows)])*V.H
    trace=mp.fsum((Pm*logA)[j,j] for j in range(A.rows))-rank*mp.log(60)
    for i in range(3):
        c=s.Rational(charges[i][n])*weight;TS[i]+=c*rank;scalar[i]+=mp.re(num(c))*trace/2
assert count==290 and TS==[s.Rational(377,5),77,79]
TV=[[s.Rational(x) for x in row] for row in fci['vector_indices']];lams=[s.Rational(x) for x in fci['vector_mass_eigenvalues']]
one={}
for gs in ['1/2','3/4','1']:
    one[gs]=[]
    for LL in ['0','2/7']:
        v=[scalar[i]-mp.re(num(TS[i]))*mp.re(num(LL))/2 for i in range(3)]
        for lam,index in zip(lams,TV):
            logarithm=mp.log(mp.re(num(gs))*mp.re(num(lam))/60)-mp.re(num(LL))
            for i in range(3):v[i]+=mp.re(num(index[i]))*(1-21*logarithm/2)
        one[gs].append(list(map(fmt,v)))

F=packed(CAL/'canonical_so10_finite_assembly_nielsen/replay_v2_tables.json.gz')
T=s.eye(12);T[0,1]=s.I/3;T[4,0]=s.Rational(2,5);T[1,4]=s.Rational(1,7);T[11,11]=s.Rational(3,2)
I=T.inv();groups=[(0,1),(1,4),(4,12)];tensor_checks=0
for gs,rows in F['finite_lambda2_fixed_xi'].items():
    for power in [0,1]:
        N=s.diag(*[s.Rational(rows[0 if j==0 else 1 if j<4 else 2][power]) for j in range(12)])
        Z=T.T*T;Np=T.T*N*T;raised=Z.inv()*Np
        zero(raised-I*N*T);zero(T*raised*I-N)
        assert Np!=T.H*N*T and raised!=Np;tensor_checks+=1
wrong_gram=[]
for obj in F['charges']:
    B=dec(obj);raised=(T.H*T).inv()*(T.H*B*T);zero(raised-I*B*T)
    wrong=T.T*B*T-T.H*B*T
    if B.todok():assert wrong.todok();wrong_gram.append(len(wrong.todok()))
H=packed(CAL/'canonical_so10_heavy_tadpole_bridge/replay_v3_tables.json.gz');M=dec(H['raw_Hessian']);R=dec(H['Rminus2_tadpole_linear_map']);Mi=dec(H['raw_Hessian_inverse'])
U=s.Matrix([[1,s.I/3,0],[0,2,s.Rational(1,5)],[s.Rational(1,7),0,1]])
inverse=U.inv()*Mi*U.inv().T;zero(inverse*(U.T*M*U)-s.eye(3));zero(R*U*inverse*U.T-R*Mi)
assert R*U*(U.H*M*U).inv()*U.T!=R*Mi

unit=load('fct_replay_s3u',CAL/'canonical_so10_scalar_cubic_units/data.py');old,functions=unit.helpers();master=old.old_master()
kernels=[]
for v in [['1','1','1'],['2','2','2'],['1','1.00000001','.99999999']]:
    masses=list(map(mp.mpf,v));row=[]
    for axis in range(3):
        other=[masses[j] for j in range(3) if j!=axis];val,err=functions.bubble_unit(masses[axis],*other,10)
        assert err<mp.mpf('1e-55');row.append(fmt(val-mp.log(60)/(6*masses[axis])))
    kernels.append(row)
elementary=[]
for r in map(mp.mpf,['1','1.00000001','.99999999','2']):
    k=mp.quad(lambda u:u*(1-u)/(1+(r-1)*u),[0,1]);f=mp.quad(lambda u:u*(1-u)*mp.log1p((r-1)*u),[0,1]);elementary.append([fmt(k),fmt(f)])
pseudo=[]
for z in map(mp.mpf,['4','4.00000001','3.99999999']):
    pseudo.append(fmt(master.sunset(1,1,z,q2=1,method='angular' if z<4 else 'integral')))
finish('replay',{'schema':'FCT1','basis':{'finite_tensors':tensor_checks,'charge_grams':len(F['charges']),'wrong_transpose_nonzero_positions':wrong_gram,'heavy_bridge':True},
 'physical_directions':count,'scalar_indices':list(map(str,TS)),'vector_indices':[[str(x) for x in row] for row in TV],
 'scalar_lambda1_L0':list(map(fmt,scalar)),'lambda1':one,'cubic_units':kernels,'elementary':elementary,'pseudothreshold':pseudo,
 'full_nine_family_basis':'STRUCTURAL_CONTRACTION_PROOF','positive_heavy_coincidence':'FIXED_GAP_FOREST_PROOF','two_loop_arbitrary_g':False},start)
