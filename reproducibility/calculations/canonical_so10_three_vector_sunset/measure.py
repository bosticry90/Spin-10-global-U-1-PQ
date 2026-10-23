"""V3A1 distinct full ordered and canonical real-vector contractions."""
from data import *
def main():
    role=sys.argv[1];assert role in ['primary','replay'];start=begin();mp.mp.dps=130 if role=='primary' else 160
    masses,rows,src=source(role);assert len(rows)==125
    wanted=sorted({canonical(row['roles'])[0] if role=='primary' else ','.join(map(str,row['roles'])) for row in rows if kind(row)=='positive'})
    assert len(wanted)==(3 if role=='primary' else 12);helper=Units(role);units={};hom={}
    for key in wanted:
        ids=list(map(int,key.split(',')));mm=[masses[k] for k in ids];vals=helper.value(mm)
        units[key]={'masses':list(map(str,mm)),'finite':list(map(lambda v:mp.nstr(v,100),vals[0])),
          'scale_J':list(map(str,vals[1])),'scale_J2':list(map(str,vals[2])),'pole2':list(map(str,vals[3])),'pole1':list(map(str,vals[4])),'pole1_J':list(map(str,vals[5]))}
        if ids==sorted(ids):
            scaled=helper.value([v*R(7,5) for v in mm]);ll=mp.log(mp.mpf(7)/5)
            err=max(abs(v-f+num(s1)*ll-num(s2)*ll*ll)/(1+abs(f)) for v,f,s1,s2 in zip(scaled[0],vals[0],vals[1],vals[2]));assert err<mp.mpf('1e-70')
            assert all(clean(a-b+2*c*s.log(R(7,5)))==0 for a,b,c in zip(scaled[1],vals[1],vals[2]));assert scaled[2:]==vals[2:];hom[key]=mp.nstr(err,45)
        print('STAGE '+role+'_positive_'+key,flush=True)
    totalF=[mp.mpf(0)]*3;tot=[[s.S.Zero]*3 for k in range(5)];full=[s.S.Zero]*3;soft=[s.S.Zero]*3;eft2=[s.S.Zero]*3;eft1=[s.S.Zero]*3;softpole=[s.S.Zero]*3
    grouped={};gh={};gs={};profiles=[];counts={k:0 for k in ['zero','positive','one_light','all_light']}
    def unit(row):
        if kind(row)=='one_light':return hard_light(row['roles'],masses)
        if role=='primary':key,order=canonical(row['roles']);inverse=[order.index(i) for i in range(3)]
        else:key=','.join(map(str,row['roles']));inverse=list(range(3))
        u=units[key];return tuple([[mp.mpf(u['finite'][i]) if k==0 else expr(u[field][i]) for i in inverse] for k,field in enumerate(['finite','scale_J','scale_J2','pole2','pole1','pole1_J'])])
    for row in rows:
        typ=kind(row);counts[typ]+=1;ww=weights(row);con=[mp.mpf(0)]*3;vv=[[s.S.Zero]*3 for k in range(5)]
        if typ in ['positive','one_light']:
            data=unit(row)
            for i,ws in enumerate(ww):
                con[i]=sum(q(w/2)*v for w,v in zip(ws,data[0]))
                for k in range(5):vv[k][i]=clean(sum(w*v/2 for w,v in zip(ws,data[k+1])))
            if role=='primary':
                totalF=[v+w for v,w in zip(totalF,con)];tot=[[clean(v+w) for v,w in zip(a,b)] for a,b in zip(tot,vv)]
            else:
                key,order=canonical(row['roles']);old=grouped.setdefault(key,[[s.S.Zero]*3 for i in range(3)])
                grouped[key]=[[clean(v+ws[k]) for v,k in zip(prev,order)] for prev,ws in zip(old,ww)]
            if typ=='one_light':
                light=row['roles'].index(0);cc=next(masses[k] for k in row['roles'] if k)
                softpole=[clean(v+ww[i][light]*(24*(J-s.log(cc))-R(4,3))/2) for i,v in enumerate(softpole)]
        elif typ=='all_light':
            eft2=[clean(sum(ws)*(-12)/2) for ws in ww];eft1=[clean(sum(ws)*R(61,6)/2) for ws in ww]
        if role=='primary':
            cf,cs=full_forest(row,masses);full=[clean(v+w) for v,w in zip(full,cf)];soft=[clean(v+w) for v,w in zip(soft,cs)]
        else:
            ms=[d,*masses[1:]]
            for i,ws in enumerate(ww):
                for k,slot in enumerate(row['roles']):
                    mass=ms[slot];other=sum(ms[r] for j,r in enumerate(row['roles']) if j!=k)
                    coef=clean(ws[k]*(-24/eps+R(67,6)+15*other/mass+eps*(R(19,18)+3*other/(2*mass)))/2)
                    gh[i,slot]=clean(gh.get((i,slot),0)+coef)
                    if slot==0:gs[i,slot]=clean(gs.get((i,slot),0)+coef)
        profiles.append({'roles':row['roles'],'kind':typ,'finite':list(map(lambda v:mp.nstr(v,90),con)),
          **{field:list(map(str,values)) for field,values in zip(['scale_J','scale_J2','pole2','pole1','pole1_J'],vv)}})
    if role=='replay':
        for key,ww in sorted(grouped.items()):
            row={'roles':list(map(int,key.split(','))),'norm':'1'};data=unit(row)
            for i,ws in enumerate(ww):
                totalF[i]+=sum(q(w/2)*v for w,v in zip(ws,data[0]))
                for k in range(5):tot[k][i]=clean(tot[k][i]+sum(w*v/2 for w,v in zip(ws,data[k+1])))
        full=[clean(sum(gh.get((i,k),0)*Hs[k] for k in range(5))) for i in range(3)];soft=[clean(sum(gs.get((i,k),0)*Hs[k] for k in range(5))) for i in range(3)]
    hard=[clean(a-b) for a,b in zip(full,soft)];assert all(not v.has(Hs[0]) for v in hard);hard0=[clean(v.subs(d,0)) for v in hard]
    diagnostics=[]
    for g2 in [R(1,2),s.S.One]:
        for LL in [s.S.Zero,R(2,7)]:
            JJ=mp.log(60/q(g2))+q(LL);ff=[f+num(a)*JJ+num(b)*JJ*JJ for f,a,b in zip(totalF,tot[0],tot[1])]
            diagnostics.append({'g10_squared':str(g2),'L':str(LL),'finite_inside_g10_squared':list(map(lambda v:mp.nstr(v,90),ff)),
              'pole1_inside_g10_squared':[str(clean(a+b*(s.log(60)-s.log(g2)+LL))) for a,b in zip(tot[3],tot[4])]})
    save(role,{'schema':'V3A1_COMPLETE_PRIMITIVE','units':units,'homogeneity_errors':hom,'working_digits':mp.mp.dps,'Kallen_fallbacks':helper.fallbacks,
      'max_imaginary_leak':mp.nstr(helper.leak,45),'counts':counts,'profiles':profiles,'finite_F0':list(map(lambda v:mp.nstr(v,90),totalF)),
      **{field:list(map(str,values)) for field,values in zip(['scale_J','scale_J2','pole2','pole1','pole1_J'],tot)},
      'all_light_EFT_pole2':list(map(str,eft2)),'all_light_EFT_pole1':list(map(str,eft1)),'mixed_soft_pole1_J_polynomial':list(map(str,softpole)),
      'forest_full_prefactor_H':list(map(str,full)),'forest_soft_prefactor_H':list(map(str,soft)),'forest_hard_before_limit':list(map(str,hard)),
      'forest_hard_limit':list(map(str,hard0)),'diagnostics':diagnostics,'original_family_ownership_preserved':True,
      'mandatory_hard_forest_correction_sha256':sha256((CAL/'canonical_so10_three_vector_soft_matching/hard_forest_correction_receipt.json').read_bytes()).hexdigest(),
      'full_C1_or_E5_qualified':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED'},start)
if __name__=='__main__':main()
