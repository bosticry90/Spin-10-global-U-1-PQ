from data import *
t=begin('primary');E,QC,chart=columns('primary');print('STAGE DIRECT_GF_SOURCE_EULER',flush=True);P=get_parent();pieces={tag:{} for tag in GROUPS+['qC']};wrong={}
for w,z in P.items():
 prefix=0
 for k,(n,jets) in enumerate(w):
  assert not jets
  images={tag:E[tag][int(n[3:])] for tag in GROUPS} if n.startswith('JLp') else {'qC':QC[int(n[2:])]}
  for tag,ps in images.items():
   for image,v in ps.items():
    word,ph=mulword(w[:k],image,w[k+1:])
    if ph:addto(pieces[tag],word,z*v*ph*(-1)**prefix);addto(wrong,word,z*v*ph)
  prefix+=odd(n)
pieces={tag:clean(p) for tag,p in pieces.items()};total=add(*pieces.values());bad=add(clean(wrong),scale(total,-1));print('STAGE GRADED_PARENT_IMAGE',summary(total),flush=True)
finish('primary',{'method':'literal_full_GF_source_Euler_and_prefix_differentiation_of_measured_parent','source_columns':{tag:[serial(p) for p in ps] for tag,ps in E.items()},'qC_columns':[serial(p) for p in QC],'charts':chart,'pieces':{tag:serial(p) for tag,p in pieces.items()},'total':serial(total),'controls':{'wrong_even_replacement_changed_positions':len(bad),'source0_before_variation_changed_positions':len(total),'omit_all_source_Euler_changed_positions':len(add(*(pieces[tag] for tag in GROUPS)))},'parent':summary(P),'image':summary(total)},t)
