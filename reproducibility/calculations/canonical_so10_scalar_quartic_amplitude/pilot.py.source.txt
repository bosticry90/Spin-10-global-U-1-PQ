"""S4A1 full scalar reference mass functions and actual matched primitive."""
from data import *
role=sys.argv[1];assert role in ['primary','replay'];start=begin();mp.mp.dps=110 if role=='primary' else 140
frame,cov,polys,coeff,charges,fci,blocks,counts=input_data(role);root=root_value(role);pair,parts=pair_function(polys,coeff,root,role)
cases={};maxerr=mp.mpf(0);minmass=mp.inf
for gs in ['1/2','1']:
    g2=mp.mpf('.5') if gs=='1/2' else mp.mpf(1);A0=[];A1=[];RR=[];P0=[]
    for b in blocks:
        a,d,r,p,err,mm=spectrum(b,g2,fci['vector_mass_eigenvalues'],root,role);A0.append(a);A1.append(d);RR.append(r);P0.append(p)
        maxerr=max(maxerr,err);minmass=min(minmass,mm)
    aa,dd,pp=[form_values(v,cov,root) for v in [A0,A1,P0]];B=[];BS=[]
    for h in range(3):
        B.append(form_values([number(charges[h][i],root)*r for i,r in enumerate(RR)],cov,root))
        BS.append(form_values([number(charges[h][i],root)*p for i,p in enumerate(P0)],cov,root))
    totals=[];slopes=[];per=[];histories=[];soft=[];controls=[]
    diagA=form_values(A0,cov,root,True)
    for h in range(3):
        hh=parts(aa,B[h]);ss=parts(dd,B[h]);C=-mp.fsum(hh.values())/4;S=-mp.fsum(ss.values())/4
        totals.append(fmt(C));slopes.append(fmt(S));per.append({n:[fmt(-hh[n]/4),fmt(-ss[n]/4)] for n in polys})
        hl=-pair(aa,BS[h])/4;ll=-pair(pp,BS[h])/4;lh=-pair(pp,B[h])/4;soft.append({'HL':fmt(hl),'LL':fmt(ll),'LH':fmt(lh)})
        hist=[]
        for ds in ['1e-4','1e-8','1e-12']:
            delta=mp.mpf(ds);log=1+mp.log(60/delta)
            full=-pair([a+delta*log*p for a,p in zip(aa,pp)],[b+bs/delta for b,bs in zip(B[h],BS[h])])/4
            matched=full-hl/delta-ll*log;rem=delta*log*lh
            assert abs(matched-C-rem)<mp.mpf('1e-80')*(1+abs(C)+abs(rem))
            hist.append({'delta':ds,'full_minus_opened_soft_and_EFT':fmt(matched),'predicted_suppressed_remainder':fmt(rem),'scaled_error_from_hard':fmt(abs(matched-C)/(1+abs(C)))})
        if lh!=0:assert all(mp.mpf(hist[i+1]['scaled_error_from_hard'])<mp.mpf(hist[i]['scaled_error_from_hard'])/1000 for i in range(2))
        histories.append(hist)
        atL=-pair([a+mp.mpf(2)*d/7 for a,d in zip(aa,dd)],B[h])/4
        assert abs(atL-C-mp.mpf(2)*S/7)<mp.mpf('1e-80')*(1+abs(C)+abs(S))
        controls.append({'omit_tadpole_constant_change':fmt(-S),'extra_g2_prefactor_change':fmt((g2-1)*C),
          'omit_compact_offdiagonals_change':fmt(-pair(diagA,B[h])/4-C),'use_own_Q2_1_change':fmt(-mp.log(60)*S),
          'deleted_light_soft_sensitive':bool(hl or ll),'L_2_over7':fmt(atL)})
    assert not any(BS[2]),'light soft fields should be SU3 neutral, as proved by exact charge support'
    cases[gs]={'finite_L0':totals,'scale_linear':slopes,'coupling_contributions':per,'soft_coefficients':soft,
      'matching_histories':histories,'negative_controls':controls,
      'form_values':{'A0':list(map(complex_fmt,aa)),'A1':list(map(complex_fmt,dd)),'P0':list(map(complex_fmt,pp)),
        'B':[[complex_fmt(z) for z in row] for row in B],'Bsoft':[[complex_fmt(z) for z in row] for row in BS]}}
    print('STAGE',role,'all_scalar_modes_and_matched_amplitude_g2_'+gs,flush=True)
assert any(abs(mp.mpf(v['omit_tadpole_constant_change']))>mp.mpf('1e-40') for c in cases.values() for v in c['negative_controls'])
save(role,{'schema':'S4A1_COMPLETE_MATCHED_QUARTIC_PRIMITIVE','cases':cases,'mode_counts':counts,'real_fields':328,'classes':35,
 'working_digits':mp.mp.dps,'report_digits':65,'max_native_spectral_residual':mp.nstr(maxerr,35),'minimum_included_positive_mass':mp.nstr(minmass,65),
 'original_Cfull':'lambda[M+delta*P0,Cbar*H_eps(M+delta*P0)/(M+delta*P0)]/(4*eps)',
 'Csoft':'lambda[M+delta*P0,Cbar*P0*H_eps(delta)/delta]/(4*eps)',
 'Chard':'Cfull-Csoft before light limit; original Cfull retained for Cparent-Cfull',
 'remaining_overall_pole':[0,0,0],'uniform_numeric_all_g_bound':False,'full_C1_or_E5_qualified':False},start)
