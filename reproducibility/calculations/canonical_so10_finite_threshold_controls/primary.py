"""FCT1 spectral logs, analytic cubic derivatives and full congruence tests."""
from data import *
start=begin('primary');mp.mp.dps=90
F=packed(CAL/'canonical_so10_finite_assembly_nielsen/primary_tables.json.gz')
S=packed(CAL/'canonical_so10_scalar_cubic_spectral_measure/primary_tables.json.gz')
Q=packed(CAL/'canonical_so10_scalar_quartic_charge_projection/primary_tables.json.gz')['class_values']
T=s.eye(12);T[0,1]=s.I/3;T[4,0]=s.Rational(2,5);T[1,4]=s.Rational(1,7);T[11,11]=s.Rational(3,2)
Ti=T.inv();Z=T.T*T;Bmetric=T.H*T;groups=[(0,1),(1,4),(4,12)]
Cs=[s.diag(*[int(a<=j<b) for j in range(12)]) for a,b in groups]
tensor_checks=0
for g,rows in F['finite_lambda2_fixed_xi'].items():
    for power in range(2):
        N=sum((s.Rational(rows[i][power])*Cs[i] for i in range(3)),s.zeros(12))
        Np=T.T*N*T
        zero(Ti.T*Np*Ti-N)
        for i,(a,b) in enumerate(groups):
            zero(s.Matrix([[s.trace(Ti*Cs[i]*T*Z.inv()*Np)/(b-a)-s.Rational(rows[i][power])]]))
        assert Np!=T.H*N*T
        assert Z.inv()*Np!=Np
        tensor_checks+=1
charge_checks=0;wrong_gram=[]
for obj in F['charges']:
    B=dec(obj);Bp=T.H*B*T;zero(Ti.H*Bp*Ti-B)
    zero(s.Matrix([[s.trace(Bmetric.inv()*Bp)-s.trace(B)]]))
    wrong=T.T*B*T-Bp
    if B.todok():assert wrong.todok();wrong_gram.append(len(wrong.todok()))
    charge_checks+=1
H=packed(CAL/'canonical_so10_heavy_tadpole_bridge/primary_v3_tables.json.gz')
M=dec(H['raw_Hessian']);Mi=dec(H['raw_Hessian_inverse']);R=dec(H['Rminus2_tadpole_linear_map'])
U=s.Matrix([[1,s.I/3,0],[0,2,s.Rational(1,5)],[s.Rational(1,7),0,1]])
zero(M*Mi-s.eye(3));zero(R*U*(U.T*M*U).inv()*U.T-R*Mi)
assert R*U*(U.H*M*U).inv()*U.T!=R*Mi

TS=[s.S(0)]*3;scalar=[mp.mpf(0)]*3;count=0
for b in S['blocks']:
    for mode in b['modes']:
        if mode['type']!=0:continue
        weight=b['dimension']*mode['rank'];count+=weight;m=mp.mpf(mode['reference_mass_squared']);assert m>0
        for i in range(3):
            c=s.Rational(Q[i][b['block']])*weight;TS[i]+=c;scalar[i]+=mp.re(num(c))*mp.log(m/60)/2
assert count==290 and TS==[s.Rational(377,5),77,79]
TV=[]
for r in range(4):
    B=dec(F['charges'][r]);TV.append([s.trace(Cs[i]*B)/(b-a) for i,(a,b) in enumerate(groups)])
lams=[s.Rational(3,10),s.Rational(3,2),s.S(25),s.Rational(253,10)]
one={}
for gs in ['1/2','3/4','1']:
    g2=mp.re(num(gs));cases=[]
    for LL in ['0','2/7']:
        L=mp.re(num(LL));cases.append([fmt(scalar[i]-mp.re(num(TS[i]))*L/2+mp.fsum(mp.re(num(TV[r][i]))*(1-mp.mpf(21)/2*(mp.log(g2*mp.re(num(lams[r]))/60)-L)) for r in range(4))) for i in range(3)])
    one[gs]=cases

unit=load('fct_s3u',CAL/'canonical_so10_scalar_cubic_units/data.py');old,functions=unit.helpers();master=old.old_master();compiled,_=unit.analytic_backend(master)
masscases=[['1','1','1'],['2','2','2'],['1','1.00000001','.99999999']]
kernels=[]
for v in masscases:
    vals,guard,leak=unit.positive_unit(list(map(mp.mpf,v)),master,compiled);kernels.append([fmt(z) for z in vals])
ratios=['1','1.00000001','.99999999','2']
elementary=[[fmt(functions.kinetic(r)),fmt(functions.f_weight(r))] for r in ratios]
pseudo=[fmt(master.sunset(1,1,mp.mpf(z),q2=1,method='dilog')) for z in ['4','4.00000001','3.99999999']]
finish('primary',{'schema':'FCT1','basis':{'finite_tensors':tensor_checks,'charge_grams':charge_checks,'wrong_transpose_nonzero_positions':wrong_gram,'heavy_bridge':True},
 'physical_directions':count,'scalar_indices':list(map(str,TS)),'vector_indices':[[str(x) for x in row] for row in TV],
 'scalar_lambda1_L0':list(map(fmt,scalar)),'lambda1':one,'cubic_units':kernels,'elementary':elementary,'pseudothreshold':pseudo,
 'full_nine_family_basis':'STRUCTURAL_CONTRACTION_PROOF','positive_heavy_coincidence':'FIXED_GAP_FOREST_PROOF','two_loop_arbitrary_g':False},start)
