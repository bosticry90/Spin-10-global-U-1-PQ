"""VHR1 direct rooted walks, actual GF grade audit and Frullani weights."""
from data import *
t=begin('primary');counts=gf_audit();M=roots('primary');edges=[(a,b,gt+'/'+vt,degree) for a,k,gt in G for kk,b,vt,degree in V if k==kk];words=[]
for out,inn,root,degree in M:
 def walk(node,path,deg):
  if node==out and deg==TARGET:
   n=len(path);words.append({'root':root,'n':n,'path':path,'sign':(-1)**n,'heat_lengths':[2*n,2*n+2]})
  if len(path)==sum(TARGET[i] for i in [0,1,5]):return
  for a,b,tag,d in edges:
   nd=plus(deg,d)
   if a==node and allowed(nd):walk(b,path+[tag],nd)
 walk(inn,[],degree)
words.sort(key=lambda x:(x['n'],x['root'],x['path']));a=s.Symbol('a',positive=True);rad={str(n):str(s.expand_log(s.integrate(1/a,(a,2*n,2*n+2)),force=True)) for n in sorted({w['n'] for w in words})}
finish('primary',{'method':'direct_ordered_rooted_depth_first_walks_and_actual_GF_polynomial_grade','words':words,'actual_GF_counts':counts,'all_actual_roots':[list(x) for x in M],'target_degree':list(TARGET),'n_bound_from_external_labels':4,'radial_weights':rad,'nonzero_roots':sorted({w['root'] for w in words})},t)
