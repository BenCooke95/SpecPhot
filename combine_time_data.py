import pandas as pd
import numpy as np

array = pd.read_csv('specphot_post_ref_40.csv', sep=',')
specphot = pd.DataFrame(array)
specphot['PER'] = 10.**specphot['LOG_PER']
specphot['KS'] = specphot['SIGNAL_SPEC']
specphot['TDUR'] = specphot['TDUR']/24.
specphot['ID'] = range(1, len(specphot) + 1)
print(len(specphot))
NGTS_IDS = np.asarray(specphot.loc[(specphot['NGTS'] == 1)]['ID'])
print(len(NGTS_IDS))
HARPS_IDS = np.asarray(specphot.loc[(specphot['HARPS'] == 1)]['ID'])
print(len(HARPS_IDS))
CORALIE_IDS = np.asarray(specphot.loc[(specphot['CORALIE'] == 1)]['ID'])
print(len(CORALIE_IDS))


array = pd.read_csv('night_day_short_out_post_ref_40.csv', sep=',', usecols=['TIME_MED','TIME_MEAN'])
phot = pd.DataFrame(array)
phot = phot.rename(columns={'TIME_MED':'TIME_MED_NGTS','TIME_MEAN':'TIME_MEAN_NGTS'})
phot['ID'] = NGTS_IDS
print(len(phot))

specphot = pd.merge(specphot, phot, on=['ID'], how='left')
print(len(specphot))
print(len(specphot.loc[(specphot['TIME_MEAN_NGTS'] != np.nan)]))
print(specphot.count())

array = pd.read_csv('phase_no_phase_pgram_short_out_post_ref_40.csv', sep=',', usecols=['TIME_MED','TIME_MEAN'])
spec = pd.DataFrame(array)
spec = spec.rename(columns={'TIME_MED':'TIME_MED_HARPS','TIME_MEAN':'TIME_MEAN_HARPS'})
spec['ID'] = HARPS_IDS
print(len(spec))

specphot = pd.merge(specphot, spec, on=['ID'], how='left')
print(len(specphot))
print(len(specphot.loc[(specphot['TIME_MEAN_HARPS'] != np.nan)]))
print(specphot.count())

array = pd.read_csv('phase_no_phase_pgram_short_coralie_out_post_ref_40.csv', sep=',', usecols=['TIME_MED','TIME_MEAN'])
spec2 = pd.DataFrame(array)
spec2 = spec2.rename(columns={'TIME_MED':'TIME_MED_CORALIE','TIME_MEAN':'TIME_MEAN_CORALIE'})
spec2['ID'] = CORALIE_IDS
print(len(spec2))

specphot = pd.merge(specphot, spec2, on=['ID'], how='left')
print(len(specphot))
print(len(specphot.loc[(specphot['TIME_MEAN_CORALIE'] != np.nan)]))
print(specphot.count())

print('Merged')

specphot['TIME_RATIO_MED_HN'] = specphot['TIME_MED_NGTS']/specphot['TIME_MED_HARPS']
specphot['TIME_RATIO_MEAN_HN'] = specphot['TIME_MEAN_NGTS']/specphot['TIME_MEAN_HARPS']
specphot['TIME_RATIO_MED_CN'] = specphot['TIME_MED_NGTS']/specphot['TIME_MED_CORALIE']
specphot['TIME_RATIO_MEAN_CN'] = specphot['TIME_MEAN_NGTS']/specphot['TIME_MEAN_CORALIE']

specphot['TIME_RATIO_HN'] = specphot['TIME_RATIO_MEAN_HN']
specphot['TIME_RATIO_CN'] = specphot['TIME_RATIO_MEAN_CN']
specphot['WEIGHT_RATIO_HN'] = specphot['SNR_RATIO_HN']*specphot['TIME_RATIO_HN']/12.
specphot['WEIGHT_RATIO_CN'] = specphot['SNR_RATIO_CN']*specphot['TIME_RATIO_CN']/12.

print('Ratios calculated')

specphot.to_csv('specphot_alltime_post_ref_40.csv', sep=',', index=False)
print('done')
