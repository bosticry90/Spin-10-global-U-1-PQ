"""Labelled background-insertion inventory. No loop integrals or expected tensors."""
from fractions import Fraction as F
from itertools import combinations,permutations,product
from collections import defaultdict
import json,hashlib

def pairings(seq):
 if not seq:yield ();return
 a=seq[0]
 for k,b in enumerate(seq[1:],1):
  for p in pairings(seq[1:k]+seq[k+1:]):yield ((a,b),)+p

def simplify(d):return {w:c for w,c in d.items() if c}

def derivative(poly,label,degrees):
 out=defaultdict(F)
 for word,coef in poly.items():
  for j,(name,jets) in enumerate(word):
   if name.startswith('G'):
    replacement=((name,''),('K'+name[1:],label),(name,''));c=-coef
   elif len(jets)<degrees.get(name,0):
    replacement=((name,''.join(sorted(jets+label))),);c=coef
   else:continue
   out[word[:j]+replacement+word[j+1:]]+=c
 return simplify(out)

def localjets(name,labels,degree):
 if name.startswith('G'):
  if not labels:return [(F(1),((name,''),))]
  K='K'+name[1:]
  if len(labels)==1:return [(F(-1),((name,''),(K,labels),(name,'')))]
  return [(F(1),((name,''),(K,p[0]),(name,''),(K,p[1]),(name,''))) for p in permutations(labels)]+[(F(-1),((name,''),(K,''.join(sorted(labels))),(name,'')))]
 if len(labels)>degree:return []
 return [(F(1),((name,''.join(sorted(labels))),))]

def placements(word,degrees):
 out=defaultdict(F)
 for i in range(len(word)):
  for j in range(len(word)):
   parts=[localjets(n,('h' if i==k else '')+('k' if j==k else ''),degrees.get(n,0)) for k,(n,_) in enumerate(word)]
   for choices in product(*parts):
    coef=F(1);w=()
    for c,p in choices:coef*=c;w+=p
    out[w]+=coef
 return simplify(out)

def build(role):
 rows=[];catalog={}
 families=[('VVVV',2,0,'1/8'),('VVSS',2,0,'1/4'),('SSSS',2,0,'1/8'),
 ('VVV',3,1,'-1/12'),('VVS',3,0,'-1/4'),('VSS',3,1,'-1/4'),('SSS',3,0,'-1/12'),
 ('ghostV',3,1,'1/2'),('ghostS',3,0,'1/2')]
 for name,edges,vbg,weight in families:
  names=['G'+str(k) for k in range(edges)]+(['V0','V1'] if edges==3 else ['V0'])
  degrees={n:2 for n in names if n.startswith('K')}
  degrees.update({'K'+str(k):2 for k in range(edges)})
  degrees.update({'V0':vbg,'V1':vbg})
  word=tuple((n,'') for n in names)
  if role=='primary':d=derivative(derivative({word:F(1)},'h',degrees),'k',degrees)
  else:d=placements(word,degrees)
  entries=[[str(c),[[a,b] for a,b in w]] for w,c in sorted(d.items())]
  catalog[name]=entries
  assert len(entries)==(8 if edges==2 else 29 if vbg else 15)
  rows.append([name,weight,len(entries)])
 word=(('G0',''),('CT',''));degree={'K0':2,'CT':2}
 if role=='primary':ct=derivative(derivative({word:F(1)},'h',degree),'k',degree)
 else:ct=placements(word,degree)
 assert len(ct)==6
 catalog['one_loop_CT']=[[str(c),[[a,b] for a,b in w]] for w,c in sorted(ct.items())]
 if role=='primary':
  pp=list(pairings(tuple(range(6))));sun=[p for p in pp if all((a<3)!=(b<3) for a,b in p)]
  assert len(pp)==15 and len(sun)==6
  assert all(sum((a<3)!=(b<3) for a,b in p)==1 for p in pp if p not in sun)
  q=len(list(pairings(tuple(range(4)))))
 else:
  sun=list(permutations(range(3,6)));dumb=list(product(range(3),range(3,6)))
  assert len(sun)+len(dumb)==15;q=3
 assert q==3
 # All bare valence solutions at L=2, not a cutoff on graph multiplicity.
 valence=[(a,b) for a in range(3) for b in range(2) if a+2*b==2]
 assert sorted(valence)==[(0,1),(2,0)]
 assert sum(r[2] for r in rows)==156
 return {'families':rows,'total_labelled_AA_words':156,'CT_words':6,
 'quartic_pairings':q,'cubic_sunset_pairings':6,'cubic_bridge_pairings':9,
 'boson_sunset_weight':str(-F(6,72)),'boson_quartic_weight':str(F(q,24)),
 'mixed_sunset_weight':str(-F(2,8)),'ghost_sunset_weight':'1/2',
 'valence_solutions':sorted(valence)},catalog

def encoded(data):return (json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
