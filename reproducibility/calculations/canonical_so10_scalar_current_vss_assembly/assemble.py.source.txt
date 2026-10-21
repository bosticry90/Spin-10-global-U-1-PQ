"""VSSA1 five complete graph-matched VSS sectors at one common scale."""
from data import *

FILES=[('canonical_so10_r0_scalar_current','validation_receipt_v3.json'),('canonical_so10_r1_scalar_current','validation_receipt_v2.json'),
 ('canonical_so10_neutral_current_matching','validation_receipt_v2.json'),('canonical_so10_r3_scalar_current','validation_receipt_v13.json'),
 ('canonical_so10_r4_scalar_current','validation_receipt.json')]
def read_sources():return [json.loads((CAL/d/f).read_bytes()) for d,f in FILES]
def q(v):
    v=str(v)
    if '/' in v:
        x=s.Rational(v);return mp.mpf(int(x.p))/int(x.q)
    return mp.mpf(v)

def main():
    start=begin('preparation.json',300);mp.mp.dps=110;rs=read_sources();fci=packed(CAL/'canonical_so10_finite_counterterm_insertion/primary_v3_tables.json.gz')
    lam=[s.S.Zero]+list(map(s.sympify,fci['vector_mass_eigenvalues']));assert lam==[0,s.Rational(3,10),s.Rational(3,2),25,s.Rational(253,10)]
    t=packed(CAL/'canonical_so10_scalar_current_sm_kernel/primary_tables.json.gz');coverage=[]
    for r in range(5):
        rows=[v for v in t['physical_probes']['profiles'] if v['r']==r]
        nonzero=[v for v in rows if s.sympify(v['raw'])!=0]
        f2=[v for v in nonzero if any(s.sympify(x)!=0 for k in ['q1_squared','q2_squared','qv_squared'] for x in v[k])]
        coverage.append({'r':r,'total_type_slots':len(rows),'raw_nonzero':len(nonzero),'F2_nonzero':len(f2),
          'zerocharge_raw_profiles':[[v['left'],v['right']] for v in nonzero if v not in f2],
          'domain_disposition':'all-soft common tree EFT cancels;equal positive scalar mass;charged light vector CLM' if r==0 else 'positive/single-soft/two-soft NCM;vector-charge zero' if r==2 else 'CCK positive/MSM one-soft/TSM two-soft' if r==1 else 'CCK positive/MSM one-soft;no both-soft support'})
    cases={};r0=rs[0]['coefficients']['Rprime_matched']
    for gs in ['0.5','1.0']:
        g2=mp.mpf(gs);parts=[]
        for r,src in enumerate(rs):
            rows=r0 if r==0 else src['cases'][gs]['coefficients'];component=[]
            for ideal,line in enumerate(rows):
                if r==0:
                    pole=s.sympify(line[0]);finite=q(line[1])+q(line[3])*mp.log(g2);scale=q(line[2]);blind=finite
                else:
                    pole=s.sympify(line[0]);j=mp.log(60/(q(lam[r])*g2));finite=q(line[1])+q(line[2])*j;scale=q(line[2]);blind=q(line[1])
                component.append({'pole':str(pole),'finite_at_L0':mp.nstr(finite,50),'L':mp.nstr(scale,50),'blind_own_scale_finite':mp.nstr(blind,50)})
            parts.append({'r':r,'lambda':str(lam[r]),'components':component})
        total=[];bad=[]
        for ideal in range(3):
            pole=red(sum(s.sympify(v['components'][ideal]['pole']) for v in parts));finite=sum(q(v['components'][ideal]['finite_at_L0']) for v in parts);scale=sum(q(v['components'][ideal]['L']) for v in parts)
            blind=sum(q(v['components'][ideal]['blind_own_scale_finite']) for v in parts)
            total.append([str(pole),mp.nstr(finite,35),mp.nstr(scale,35)]);bad.append(mp.nstr(blind-finite,45))
        assert max(abs(q(v)) for v in bad)>mp.mpf('1e-6')
        cases[gs]={'axes':['overall_pole','finite_at_L0','L'],'coefficients':total,'components':parts,'blind_own_scale_addition_finite_changes':bad}
    bind=[{'r':r,'folder':d,'receipt':f,'sha256':sha256((CAL/d/f).read_bytes()).hexdigest(),'status':rs[r]['status']} for r,(d,f) in enumerate(FILES)]
    value={'schema':'VSSA1_COMMON_SCALE_ASSEMBLY','cases':cases,'coverage':coverage,'branch_receipts':bind,
      'whole_function':'Sum_r Lambda_r(g²,j_r) with j_r=L-log(g²)+log(60/lambda_r),r>0;R0 uses L,log(g²)',
      'common_scale':'L=log(Q²/60);total Lambda_VSS=g10²*coefficients','all_five_graph_matched_primitive_branches_only':True,
      'remaining_parent_minus_family_counterterm_included':False,'overall_subtraction_included':False,'full_C1_or_E5_qualified':False,
      'finite_physical_unification_test_performed':False,'scientific_acceptance':'NOT_PERFORMED'}
    save('primary','assembly',value,start)
if __name__=='__main__':main()
