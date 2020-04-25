import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import datetime
import scipy.signal as signal

array = pd.read_csv('specphot_post_ref_40.csv', sep=',')
df = pd.DataFrame(array)
df = df.loc[(df['HARPS'] == 1)].reset_index(drop=True)

####USER INPUTS####
Vmag = 11. #Choose V-band magnitude of host (float)
###################

from scipy.interpolate import interp1d
harps = pd.read_csv('harps_noise_data.csv', sep=',', names=['x','y']) #read HARPS noise data (minimum signal that gives 3sigma detection)
harps = pd.DataFrame(harps)
harps_func = interp1d(harps['x'], harps['y'], kind='linear', fill_value=[0.413589], bounds_error=False) # Line shows minimum k for SNR=3
HARPS_err = (harps_func(Vmag)/3.)
print ('HARPS_err=', HARPS_err)

start_time = datetime.datetime.now()
print('Start time:', start_time)

sub_start_time = datetime.datetime.now()

PER=[]
TIME_MED=[]
N_PER_MED=[]
TIME_MEAN=[]
N_PER_MEAN=[]
KS=[]
PRED_PER=[]
LENGTH=[]

jlen=10.

f = np.logspace(-3., 0., 1000)
f = 2.*np.pi*f

k=0.
while k<len(df):

        log_period = df['LOG_PER'][k]
        period = 10.**log_period
        period_jump = np.ceil(period/30.)
        K = df['SIGNAL_SPEC'][k]
            
        TIME=[]

        j=0.
        while j<jlen:

                PHASE=[]
                AMPLITUDE=[]

                int_time = np.random.random()*period
                time = int_time - 1.
                day_time = time
                pgram_period = 0.
                pgram_K = 0.
                pgram_b = 1.

                while (abs(pgram_period-period)/period > 0.05) | ((abs(pgram_K-K)/K) > 0.05) | (abs(pgram_b) > 0.05):
                        day_time = day_time + period_jump
                        
                        good_observing = np.random.randint(5)
                        
                            
                        if good_observing != 0:
                                time = day_time - (4./24.) + np.random.random()*(8./24.)
                                phase = time
                                amplitude = K*np.sin(phase*2.*np.pi/period) + np.random.normal(0,HARPS_err)
                                PHASE.append(phase)
                                AMPLITUDE.append(amplitude)
                        else:
                                PHASE=PHASE
                                AMPLITUDE=AMPLITUDE
                        
                        if ((time - int_time)>=0.5*period) & (len(PHASE)>=6):
                                    pgram = signal.lombscargle(PHASE, AMPLITUDE, f, normalize=True)
                                    pgram_period = 2.*np.pi/f[np.argmax(pgram)]
                                    
                                    if (abs(pgram_period - period)/period < 0.05):
                                        def func_test(x,a,b):
                                                return a * np.sin((2.*np.pi*x)+b)
                                        try:
                                            popt_test = curve_fit(func_test, ( PHASE/pgram_period - divmod(PHASE/pgram_period, 1)[0] ), AMPLITUDE, sigma=np.ones(len(PHASE))*HARPS_err, bounds=([-np.inf,-0.5], [np.inf, 0.5]))[0]
                                            pgram_K = popt_test[0]
                                            pgram_b = popt_test[1]
                                        except:
                                            pgram_K = 0
                                            pgram_b = 1.
                        else:
                            pgram_period = 0.
                            pgram_K = 0.
                            pgram_b = 1.
                        
                        if (day_time/period > 10.):
                            print('limit reached')
                            pgram_period = period
                            pgram_K = K
                            pgram_b = 0.
                            time = np.nan
                            time = 10.*period
                        
                TIME.append(time - int_time)
                
                j=j+1.

        PER.append(period)
        TIME_MED.append(np.nanmedian(TIME))
        N_PER_MED.append(np.nanmedian(TIME)/period)
        TIME_MEAN.append(np.nanmean(TIME))
        N_PER_MEAN.append(np.nanmean(TIME)/period)
        KS.append(K)

        print('k:', k)
        k=k+1


df = pd.DataFrame({'PER' : PER, 'TIME_MED' : TIME_MED, 'N_PER_MED' : N_PER_MED, 'TIME_MEAN' : TIME_MEAN, 'N_PER_MEAN' : N_PER_MEAN, 'KS' : KS})#, 'LENGTH' : LENGTH})

df.to_csv('phase_no_phase_pgram_short_out_post_ref_40.csv', index=False)

print('Runtime:', (datetime.datetime.now() - start_time))
