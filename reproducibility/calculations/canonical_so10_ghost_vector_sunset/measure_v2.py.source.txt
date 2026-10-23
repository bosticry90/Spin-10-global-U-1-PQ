"""GVA1 distinct complete contractions and absolute derivative evaluations."""
from data_v2 import *
def main():
    role=sys.argv[1];assert role in ['primary','replay'];start=begin('v2_preparation.json');mp.mp.dps=130 if role=='primary' else 160
    src=source(role);masses=list(map(expr,src['mass_coefficients']));rows=src['rows'];assert len(rows)==125
    heavy=[r for r in rows if kind(r)=='positive'];assert len(heavy)==12
    wanted=sorted({canonical(r)[0] for r in heavy}) if role=='primary' else sorted({key_of(r) for r in heavy});assert len(wanted)==(7 if role=='primary' else 12)
    helper=Units(role);units={};scale_checks={}
    for key in wanted:
        a,b,r=map(int,key.split(','));mm=[masses[a],masses[b],masses[r]];ff,ss,pp=helper.value(mm)
        units[key]={'masses':list(map(str,mm)),'finite':list(map(lambda v:mp.nstr(v,100),ff)),'scale':list(map(str,ss)),'pole':list(map(str,pp))}
        if a<=b:
            scaled,ssl,ppl=helper.value([v*s.Rational(7,5) for v in mm]);assert ss==ssl and pp==ppl
            error=max(abs(v-f+q(slope)*mp.log(mp.mpf(7)/5))/(1+abs(f)) for v,f,slope in zip(scaled,ff,ss));assert error<mp.mpf('1e-70');scale_checks[key]=mp.nstr(error,45)
        print('STAGE',role,key,flush=True)
    full=[s.S.Zero]*3;soft=[s.S.Zero]*3;profile=[];totF=[mp.mpf(0)]*3;totS=[s.S.Zero]*3;totP=[s.S.Zero]*3;eftP=[s.S.Zero]*3;counts={k:0 for k in ['zero','positive','one_light','all_light']}
    grouped={};grouped_h={};grouped_soft={}
    for row in rows:
        typ=kind(row);counts[typ]+=1;r,a,b=ids(row);ww=weights(row);pref=s.Rational(3,4);contrib=[mp.mpf(0)]*3;pole=[s.S.Zero]*3;sc=[s.S.Zero]*3
        if typ not in ['zero','all_light']:
            if typ=='positive':
                key,swap=canonical(row);u=units[key];ff=list(map(mp.mpf,u['finite']));ss=list(map(expr,u['scale']));pp=list(map(expr,u['pole']))
                if swap:ff[0],ff[1]=ff[1],ff[0];ss[0],ss[1]=ss[1],ss[0];pp[0],pp[1]=pp[1],pp[0]
            else:ff,ss=light_kernel(row,masses);pp=[-s.S.One,-s.S.One,-s.Rational(1,3)]
            for i in range(3):
                contrib[i]=sum(q(pref*w)*v for w,v in zip(ww[i],ff));pole[i]=clean(pref*sum(w*v for w,v in zip(ww[i],pp)));sc[i]=clean(pref*sum(w*v for w,v in zip(ww[i],ss)))
            if role=='primary':
                totF=[v+w for v,w in zip(totF,contrib)];totP=[clean(v+w) for v,w in zip(totP,pole)];totS=[clean(v+w) for v,w in zip(totS,sc)]
            else:
                key,swap=canonical(row);gw=[list(ws) for ws in ww]
                if swap:
                    for ws in gw:ws[0],ws[1]=ws[1],ws[0]
                if key not in grouped:grouped[key]=[[s.S.Zero]*3 for i in range(3)]
                grouped[key]=[[clean(v+w) for v,w in zip(old,new)] for old,new in zip(grouped[key],gw)]
        elif typ=='all_light':
            eftP=[clean(pref*sum(w*v for w,v in zip(ws,[-1,-1,-s.Rational(1,3)]))) for ws in ww]
        if role=='primary':
            f,sf=full_forest(row,masses);full=[clean(v+w) for v,w in zip(full,f)];soft=[clean(v+w) for v,w in zip(soft,sf)]
        else:
            # Sum the independently grouped original closing-sector operators.
            ms=[d,*masses[1:]]
            for i,ws in enumerate(ww):
                terms=[(a,-pref*ws[0]/3),(b,-pref*ws[1]/3),(r,pref*ws[2]*(-1-eps/9+(s.Rational(10,3)+eps/3)*(ms[a]+ms[b])/ms[r]))]
                for slot,coef in terms:
                    grouped_h[i,slot]=clean(grouped_h.get((i,slot),0)+coef)
                    if slot==0:grouped_soft[i,slot]=clean(grouped_soft.get((i,slot),0)+coef)
        profile.append({'roles':list(ids(row)),'kind':typ,'finite':list(map(lambda v:mp.nstr(v,90),contrib)),'scale':list(map(str,sc)),'pole':list(map(str,pole))})
    if role=='replay':
        for key,ww in sorted(grouped.items()):
            a,b,r=map(int,key.split(','));row={'vector':r,'antighost_edge':a,'ghost_edge':b}
            if a>0 and r>0:u=units[key];ff=list(map(mp.mpf,u['finite']));ss=list(map(expr,u['scale']));pp=list(map(expr,u['pole']))
            else:ff,ss=light_kernel(row,masses);pp=[-s.S.One,-s.S.One,-s.Rational(1,3)]
            for i,ws in enumerate(ww):
                totF[i]+=sum(q(s.Rational(3,4)*w)*v for w,v in zip(ws,ff));totP[i]=clean(totP[i]+s.Rational(3,4)*sum(w*v for w,v in zip(ws,pp)));totS[i]=clean(totS[i]+s.Rational(3,4)*sum(w*v for w,v in zip(ws,ss)))
        full=[clean(sum(grouped_h.get((i,k),0)*Hs[k] for k in range(5))) for i in range(3)]
        soft=[clean(sum(grouped_soft.get((i,k),0)*Hs[k] for k in range(5))) for i in range(3)]
    hard=[clean(v-w) for v,w in zip(full,soft)];assert all(not v.has(Hs[0]) for v in hard)
    hard0=[clean(v.subs(d,0)) for v in hard];diagnostics=[]
    for g2 in [s.Rational(1,2),s.S.One]:
        C=[v+q(b)*mp.log(60/q(g2)) for v,b in zip(totF,totS)]
        for LL in [s.S.Zero,s.Rational(2,7)]:diagnostics.append({'g10_squared':str(g2),'L':str(LL),'coefficient_inside_g10_squared':[mp.nstr(v+q(LL)*q(b),90) for v,b in zip(C,totS)]})
    save('primary_v2' if role=='primary' else 'replay',{'schema':'GVA1_MEASURED_PRIMITIVE','units':units,'homogeneity_errors':scale_checks,'Kallen_fallbacks':helper.fallbacks,'working_digits':mp.mp.dps,
      'max_imaginary_leak':mp.nstr(helper.leak,40),'counts':counts,'profiles':profile,'exchange_grouped_weights':{k:list(map(lambda ws:list(map(str,ws)),v)) for k,v in grouped.items()},
      'finite_F0':list(map(lambda v:mp.nstr(v,90),totF)),'scale_J':list(map(str,totS)),'remaining_pole':list(map(str,totP)),'all_light_EFT_pole':list(map(str,eftP)),
      'forest_full_prefactor_H':list(map(str,full)),'forest_soft_prefactor_H':list(map(str,soft)),'forest_hard_before_limit':list(map(str,hard)),
      'forest_hard_limit':list(map(str,hard0)),'diagnostics':diagnostics,'original_full_family_ownership_preserved':True,
      'full_C1_or_E5_qualified':False,'scientific_acceptance':'NOT_PERFORMED','authority':'34/39_UNCHANGED'},start)
if __name__=='__main__':main()
