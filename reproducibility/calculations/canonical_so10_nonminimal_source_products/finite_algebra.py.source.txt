"""Exact finite Gaussian checks; source directions have genuine odd coefficients.

Keys are (commuting amplitude mask, exterior mask, boson-field power).
u,a,b are truncated only after coefficient selection; no boson field is
treated as an odd or nilpotent quantum coordinate. Exterior generators
are theta1,theta2,f0,f1 in that order.
"""
from fractions import Fraction as F

def clean(p):return {k:v for k,v in p.items() if v}
def add(*pp):
    out={}
    for p in pp:
        for k,v in p.items():out[k]=out.get(k,F(0))+v
    return clean(out)
def scale(p,c):return clean({k:v*c for k,v in p.items()})
def mul(p,q,wrong_exterior=False):
    out={}
    for (a,g,z),v in p.items():
        for (b,h,w),x in q.items():
            if a&b or g&h:continue
            inversions=sum((h&((1<<i)-1)).bit_count() for i in range(4) if g&(1<<i))
            sign=1 if wrong_exterior else (-1)**inversions
            key=(a|b,g|h,z+w);out[key]=out.get(key,F(0))+sign*v*x
    return clean(out)
def atom(c=1,a=0,g=0,z=0):return {(a,g,z):F(c)} if c else {}
def derivative(p,field):
    out={}
    for (a,g,z),v in p.items():
        if field==0:
            if z:out[a,g,z-1]=out.get((a,g,z-1),F(0))+z*v
        else:
            bit=1<<(field+1)
            if g&bit:
                key=(a,g^bit,z);out[key]=out.get(key,F(0))+(-1)**((g&(bit-1)).bit_count())*v
    return clean(out)
def hessian(action):
    parity=[0,1,1]
    return [[scale(derivative(derivative(action,j),i),(-1)**(parity[i]*(parity[j]+1))) for j in range(3)] for i in range(3)]
def zero(n,m=None):return [[{} for j in range(n if m is None else m)] for i in range(n)]
def identity(n):return [[atom(int(i==j)) for j in range(n)] for i in range(n)]
def mm(A,B):
    assert len(A[0])==len(B)
    return [[add(*(mul(A[i][k],B[k][j]) for k in range(len(B)))) for j in range(len(B[0]))] for i in range(len(A))]
def plus(A,B):return [[add(x,y) for x,y in zip(a,b)] for a,b in zip(A,B)]
def neg(A):return [[scale(x,-1) for x in row] for row in A]
def product(*AA):
    out=identity(len(AA[0]))
    for A in AA:out=mm(out,A)
    return out
def tr(A,graded=True):return add(*(scale(A[i][i],1 if i==0 or not graded else -1) for i in range(len(A))))
def coefficient(p,mask):return {(0,g,z):v for (a,g,z),v in p.items() if a==mask}
def matrix_coefficient(A,mask):return [[coefficient(p,mask) for p in row] for row in A]
def inverse_nilpotent(A,base_inverse):
    perturb=[[clean({k:v for k,v in p.items() if k[0]}) for p in row] for row in A]
    X=mm(base_inverse,perturb);out=zero(len(A));term=identity(len(A))
    for n in range(4):
        out=plus(out,product(term,base_inverse));term=neg(mm(term,X))
    return out
def log_scalar(value,constant):
    x=add(scale(value,1/constant),atom(-1));term=atom();out={}
    for n in range(1,4):
        term=mul(term,x);out=add(out,scale(term,F((-1)**(n+1),n)))
    assert not mul(term,x)
    return out
def display(p):return [[a,g,z,str(v)] for (a,g,z),v in sorted(p.items())]

def fixture(seed):
    k=F(seed+2);m=F(seed+3)
    action=add(atom(k/2,z=2),atom(m,g=12),
      atom(seed+1,a=1,z=2),atom(seed+2,a=1,g=12),
      atom(seed+3,a=2,g=5,z=1),atom(1,a=2,g=9,z=1),
      atom(seed+4,a=4,g=10,z=1),atom(2,a=4,g=6,z=1),
      atom(seed+1,a=3,g=5,z=1),atom(3,a=3,g=9,z=1),
      atom(seed+2,a=5,g=10,z=1),atom(4,a=5,g=6,z=1),
      atom(seed+5,a=7,g=15))
    H=hessian(action);G=zero(3);G[0][0]=atom(1/k);G[1][2]=atom(1/m);G[2][1]=atom(-1/m)
    base=matrix_coefficient(H,0);assert mm(base,G)==identity(3) and mm(G,base)==identity(3)
    perturb=[[clean({key:v for key,v in p.items() if key[0]}) for p in row] for row in H]
    X=mm(G,perturb);term=identity(3);direct={};ordinary={}
    for n in range(1,4):
        term=mm(term,X);direct=add(direct,scale(tr(term),F((-1)**(n+1),2*n)))
        ordinary=add(ordinary,scale(tr(term,False),F((-1)**(n+1),2*n)))
    assert mm(term,X)==zero(3)
    Ai,Aj,U0,Ui,Uj,Uij=[matrix_coefficient(H,n) for n in [2,4,1,3,5,7]]
    five=[tr(product(G,Uij)),scale(tr(product(G,Uj,G,Ai)),-1),
      scale(tr(product(G,Aj,G,Ui)),-1),tr(product(G,U0,G,Aj,G,Ai)),tr(product(G,Aj,G,U0,G,Ai))]
    answer=scale(add(*five),F(1,2));target=coefficient(direct,7)
    assert target==coefficient(answer,0)
    # Independent block Berezinian, not an ordinary determinant of a supermatrix.
    D=[row[1:] for row in H[1:]];Di0=zero(2);Di0[0][1]=atom(1/m);Di0[1][0]=atom(-1/m)
    Di=inverse_nilpotent(D,Di0)
    schur=add(H[0][0],scale(product([H[0][1:] ],Di,[[H[1][0]],[H[2][0]]])[0][0],-1))
    determinant=add(mul(D[0][0],D[1][1]),scale(mul(D[0][1],D[1][0]),-1))
    berezin=scale(add(log_scalar(schur,k),scale(log_scalar(determinant,m*m),-1)),F(1,2))
    assert coefficient(berezin,7)==target
    reverse=scale(add(tr(product(G,Uij)),scale(tr(product(G,Ui,G,Aj)),-1),
        scale(tr(product(G,Ai,G,Uj)),-1),tr(product(G,U0,G,Ai,G,Aj)),tr(product(G,Ai,G,U0,G,Aj))),F(1,2))
    assert reverse==answer
    assert set(target)<= {(0,3,0)} and target
    omissions=[bool(scale(part,F(1,2))) for part in five]
    assert all(omissions) and coefficient(ordinary,7)!=target
    # Raw odd directions exchange sign; complete even-direction derivatives commute.
    assert mul(atom(g=1),atom(g=2))==scale(mul(atom(g=2),atom(g=1)),-1)
    return {'seed':seed,'source_uab_coefficient':display(target),'five_term_coefficients':[display(scale(x,F(1,2))) for x in five],
      'all_five_omissions_sensitive':omissions,'supertrace_log_equals_Berezinian':True,
      'ordinary_trace_control_sensitive':True,'even_direction_exchange_equal':True,
      'odd_source_components_anticommute':True}
