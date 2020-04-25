import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import ephem
from scipy.optimize import curve_fit

array = pd.read_csv('specphot_post_ref_40.csv', sep=',')
df = pd.DataFrame(array)
df = df.loc[(df['NGTS'] == 1)].reset_index(drop=True)

df['TDUR'] = df['TDUR']/24.

start_time = datetime.datetime.now()
print ('Start time:', start_time)

PER=[]
TIME_MED=[]
N_PER_MED=[]
TIME_MEAN=[]
N_PER_MEAN=[]
LENGTH=[]
N_TRANS_MED=[]
N_TRANS_MEAN=[]
TDUR=[]

ilen=10.
klen=10.

j=0
while j<len(df):
        log_per = df['LOG_PER'][j]
        per = (10.**log_per)
        Tdur = df['TDUR'][j]

        TIME=[]
        N_PER=[]
        N_TRANS=[]
        i=0.
        while i<ilen:
                initial_time = np.random.rand()*per
                
                n_trans=0
                
                k=0.
                while k<klen:
                        time = per - initial_time + (k*per)
                        in_time = time - (Tdur/2.)
                        in_time_frac = in_time%1
                        eg_time = time+(Tdur/2.)
                        eg_time_frac = eg_time%1
                        n_per = time/per
                        
                        good_observing = np.random.randint(5) #80% chance of good observing

                        if ((in_time_frac < (1./3.)) | (eg_time_frac < (1./3.))) & (good_observing != 0): #8hr night
                                limit=0
                                n_trans=n_trans+1
                                if n_trans==2:
                                        k=klen
                                else:
                                        k=k+1.
                        else:
                                k=k+1.
                                time=np.nan
                                n_per=np.nan
                                limit=1
                if limit == 1:
                        print('limit reached')
                        time = 10.*per
                
                TIME.append(time)
                N_PER.append(n_per)
                N_TRANS.append(n_trans)
                i=i+1.

        PER.append(per)
        TIME_MED.append(np.nanmedian(TIME))
        N_PER_MED.append(np.nanmedian(TIME)/per)
        TIME_MEAN.append(np.nanmean(TIME))
        N_PER_MEAN.append(np.nanmean(TIME)/per)
        TDUR.append(Tdur)
        
        print('j:',j)
        j=j+1.

print('Runtime:', (datetime.datetime.now() - start_time))

df = pd.DataFrame({'PER' : PER, 'TIME_MED' : TIME_MED, 'N_PER_MED' : N_PER_MED, 'TIME_MEAN' : TIME_MEAN, 'N_PER_MEAN' : N_PER_MEAN, 'TDUR' : TDUR})#, 'LENGTH' : LENGTH, 'N_TRANS_MED' : N_TRANS_MED, 'N_TRANS_MEAN' : N_TRANS_MEAN, 'TDUR' : TDUR})

df.to_csv('night_day_short_out_post_ref_40.csv', index=False)
