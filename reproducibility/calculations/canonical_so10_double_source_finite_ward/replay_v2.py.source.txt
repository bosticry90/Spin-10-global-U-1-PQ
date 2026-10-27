from data_v2 import *
t=begin('replay');E,QC,chart=columns('replay');print('STAGE FULL_E2_COTANGENT_COLUMNS',flush=True);d=read(CAL/'canonical_so10_double_auxiliary_source_pole/actual_replay_v2_result.json')['actual_tensors'];S={i:{(a,b):co(z) for a,b,z in rows} for i,rows in d['S']};F={i:{(a,b):co(z) for a,b,z in rows} for i,rows in d['F']};mat={}
for i in range(45):
 for k in range(45):
  mm=defaultdict(lambda:s.S.Zero)
  for (a,h),z in S.get(i,{}).items():
   for (hh,b),v in F.get(k,{}).items():
    if h==hh:mm[a,b]+=z*v
  if clean(mm):mat[i,k]=clean(mm)
bucket=defaultdict(list)
for lab,m in mat.items():
 for (a,b),z in m.items():bucket[a,b].append((lab,z))
gram=defaultdict(lambda:s.S.Zero)
for (a,b),ls in bucket.items():
 for x,z in ls:
  for y,v in bucket.get((b,a),[]):gram[x,y]+=z*v
gram=clean(gram);print('STAGE MARKED_SF_LOOP_GRAM',len(gram),flush=True);pieces={tag:{} for tag in GROUPS+['qC']}
for ((i,k),(j,l)),z in gram.items():
 left=((f'JLp{i}',()),(f'Cp{k}',()))
 for tag in GROUPS:
  for w,v in E[tag][j].items():
   word,ph=mulword(left,w,((f'Cp{l}',()),))
   if ph:addto(pieces[tag],word,ph*z*v)
 for w,v in QC[l].items():
  word,ph=mulword(left,((f'JLp{j}',()),),w)
  if ph:addto(pieces['qC'],word,-ph*z*v)
pieces={tag:clean(p) for tag,p in pieces.items()};total=add(*pieces.values());print('STAGE PRECONTRACTION_WARD_IMAGE',summary(total),flush=True)
finish('replay',{'method':'full_E2_columns_and_source_marked_SF_Gram_before_trace_contraction','source_columns':{tag:[serial(p) for p in ps] for tag,ps in E.items()},'qC_columns':[serial(p) for p in QC],'charts':chart,'pieces':{tag:serial(p) for tag,p in pieces.items()},'total':serial(total),'image':summary(total),'color_gram_nonzero_pairs':len(gram),'new_measured_parent_or_primary_image_read':False},t)
