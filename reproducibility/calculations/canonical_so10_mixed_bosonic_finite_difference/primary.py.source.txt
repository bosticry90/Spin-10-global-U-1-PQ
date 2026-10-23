"""MBF1 explicit split-Clifford witnesses for the complete mixed finite family."""
from data import *
from itertools import product,combinations
start=begin('primary');g=s.Symbol('g10',real=True);h=s.Symbol('h')
pa=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
g4=[s.kronecker_product(pa[0],s.eye(2)),s.kronecker_product(pa[1],s.eye(2)),s.kronecker_product(pa[2],pa[0]),s.kronecker_product(pa[2],pa[1])]
gam=[s.kronecker_product(t,pa[2]) for t in g4]+[s.kronecker_product(s.eye(4),t) for t in pa[:2]]
pair={w:gam[w[0]]*gam[w[1]] for w in product(range(6),repeat=2)}
four={w:s.SparseMatrix(pair[w[:2]]*pair[w[2:]]).todok() for w in product(range(6),repeat=4)}
pair={w:s.SparseMatrix(M).todok() for w,M in pair.items()};cache={}
def tr(w):
 if w not in cache:
  if len(w)==4:cache[w]=s.expand(sum(v for (i,j),v in four[w].items() if i==j)/2)
  else:
   A=four[w[:4]];B=pair[w[4:]];cache[w]=s.expand(sum(v*B.get((j,i),0) for (i,j),v in A.items())/2)
 return cache[w]
def spin(indices,v):
 word=[]
 for k,z in zip(indices,v):
  word.append(k)
  if z>=0:word.append(z)
 return tr(tuple(word))
def canon(w):return min(w[j:]+w[:j] for j in range(len(w)))
def add(out,w,value):
 if value:
  w=canon(w);out[w]=s.expand(out.get(w,0)+value)
def clean(out):return {w:v for w,v in out.items() if v!=0}
def rows(out):return [[[[kind,mu,list(ds)] for kind,mu,ds in w],str(val)] for w,val in sorted(clean(out).items())]
paths=packed(CAL/'canonical_so10_scalar_yukawa_reference/primary_tables.json.gz')['chiral_paths']
def labels(v):
 roles=tuple(int(t>=0) for t in v);n=len(v)
 for labs in product(range(2),repeat=n):
  val=s.sympify(paths[str(n)+'_'+''.join(map(str,roles))+'_'+''.join(map(str,labs))])/4
  if val:yield labs,val
def fields(v,labs):return tuple(('L' if lab==0 else 'R',mu,()) if mu>=0 else ('U' if lab==0 else 'V',-1,()) for mu,lab in zip(v,labs))
raw3={};finite3={}
for pos in range(3):
 for mu,j in product(range(4),repeat=2):
  v=tuple(mu if k==pos else -1 for k in range(3));samples=[]
  for rank in [0,1,2]:
   A=-sum(spin((a,j,a),v) for a in range(4+rank));B=-sum(spin((a,a,j),v) for a in range(4+rank))
   U=2*sum(spin((j,a,a),v)+spin((a,j,a),v)+spin((a,a,j),v) for a in range(4+rank));samples.append([A,B,U])
  for k in range(3):assert samples[2][k]-samples[0][k]==2*(samples[1][k]-samples[0][k])
  poly=[h*(a-b) for a,b in zip(samples[1],samples[0])];raw3[v,j]=poly
  finite3[v,j]=[s.expand(2*s.diff(z,h).subs(h,0)/den) for z,den in zip(poly,[4,4,24])]
def triangle(no_den=False,one_path=False):
 out={}
 for (v,j),vals in finite3.items():
  A,B,U=vals
  if no_den:U=0
  ls=list(labels(v))
  for labs,pweight in (ls[:1] if one_path else ls):
   w=fields(v,labs);phase=-g/6
   for slot,val in [(0,A+B+2*U),(1,B+U)]:
    ww=list(w);kind,mu,ds=ww[slot];ww[slot]=(kind,mu,(j,));add(out,tuple(ww),phase*pweight*(-s.I)*val)
 return clean(out)
box_types=set()
for aa,bb in combinations(range(4),2):
 for mu,nu in product(range(4),repeat=2):box_types.add(tuple(mu if k==aa else nu if k==bb else -1 for k in range(4)))
box_types.add((-1,)*4);pol2={};pol4={}
for v in sorted(box_types):
 samples=[]
 for rank in [0,1,2]:
  vals=[s.S.Zero]*3
  for a,b in product(range(4+rank),repeat=2):
   cat=int(a>=4)+int(b>=4);vals[cat]+=spin((a,a,b,b),v)+spin((a,b,a,b),v)+spin((a,b,b,a),v)
  samples.append(vals)
 assert samples[0][0]==samples[1][0]==samples[2][0] and samples[2][1]==2*samples[1][1]
 pol2[v]=h*samples[1][1];pol4[v]=s.expand(h*samples[1][2]+h*(h-1)*(samples[2][2]-2*samples[1][2])/2)
def boxes(no_four=False,one_path=False):
 out={'YYGG':{},'YYYY':{}}
 for v in sorted(box_types):
  ny=sum(mu<0 for mu in v);ng=4-ny;phase=s.I**ny*g**ng/8
  finite=s.diff(pol2[v]+(0 if no_four else pol4[v]),h).subs(h,0)/12
  ls=list(labels(v))
  for labs,pweight in (ls[:1] if one_path else ls):add(out['YYYY' if ny==4 else 'YYGG'],fields(v,labs),phase*pweight*finite)
 return {k:clean(v) for k,v in out.items()}
B=boxes();bad4=boxes(True);badpath=boxes(False,True)
finish('primary',{'method':'explicit_gamma_witness_hat_polynomials_and_actual_ordered_loop_phases','triangle_density':rows(triangle()),'YYGG_density':rows(B['YYGG']),'YYYY_density':rows(B['YYYY']),'triangle_no_denominator_density':rows(triangle(True)),'triangle_one_path_density':rows(triangle(False,True)),'YYGG_no_four_hat_density':rows(bad4['YYGG']),'YYYY_no_four_hat_density':rows(bad4['YYYY']),'YYGG_one_path_density':rows(badpath['YYGG']),'YYYY_one_path_density':rows(badpath['YYYY']),'raw_triangle_hat_numerators':{','.join(map(str,v))+':'+str(j):list(map(str,z)) for (v,j),z in sorted(raw3.items())},'raw_box_two_hat_numerator':{','.join(map(str,v)):str(z) for v,z in sorted(pol2.items())},'raw_box_four_hat_numerator':{','.join(map(str,v)):str(z) for v,z in sorted(pol4.items())},'witness_spin_trace':8,'witness_to_physical_divisor':2,'physical_spin_trace':4,'gaussian_factor':'1/2','path_trace_factor':'1/2_FOR_EACH_ALLOWED_PATH','family_trace':'FULL48_NO_EXTRA3','hat_rank':'-2epsilon','raw_triangle_positions':48*3,'raw_box_positions':97*2,'new_one_loop_finite_families':3,'new_two_loop_integrals':0,'physical_scheme_adopted':False,'finite_massive_threshold_computed':False},start)
