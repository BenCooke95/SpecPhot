import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from mpl_toolkits.mplot3d import Axes3D
import sys
from mrexo import predict_from_measurement
from datetime import datetime

start_time = datetime.now()
print('Start time:', start_time)

####USER INPUTS####
Vmag = 11. #Choose V-band magnitude of host (float)
ilen=jlen=klen=39. #Set size of grid. i,j,k correspond to stellar radius, planetary radius and period (float)
###################


#define constants
r_sun = 6.957e8
r_jup = 7.1492e7
r_earth = 6.3781e6
rho_sun = 1.408e3
rho_jup = 1.326e3
rho_earth = 5.515e3
m_sun = 1.98847e30
m_jup = 1.89813e27
m_earth = 5.9722e24
G = 6.67408e-11

Imag=Vmag-0.39 #I-band magnitude of host

ngts = pd.read_csv('noise/ngts_noise_data.csv', sep=',', names=['x','y']) #read NGTS noise data (binned to 1hour)
ngts = pd.DataFrame(ngts)
ngts_x = np.arange(min(ngts['x']), max(ngts['x']), 0.001) #create array of possible NGTS mag values

harps = pd.read_csv('noise/harps_noise_data.csv', sep=',', names=['x','y']) #read CORALIE noise data (minimum signal that gives 3sigma detection)
harps = pd.DataFrame(harps)
coralie = pd.read_csv('noise/coralie_noise_data.csv', sep=',', names=['x','y']) #read CORALIE noise data (minimum signal that gives 3sigma detection)
coralie = pd.DataFrame(coralie)
harps_x = np.arange(min(harps['x']),max(harps['x']),0.001) #create array of possible HARPS mag values
coralie_x = np.arange(min(coralie['x']),max(coralie['x']),0.001) #create array of possible CORALIE mag values

ngts_func = interp1d(ngts['x'], (3.*ngts['y']), kind='cubic', fill_value='extrapolate') # Line shows minimum depth for SNR=3
coralie_func = interp1d(coralie['x'], coralie['y'], kind='linear', fill_value=[1.441150], bounds_error=False) # Line shows minimum k for SNR=3
harps_func = interp1d(harps['x'], harps['y'], kind='linear', fill_value=[0.413589], bounds_error=False) # Line shows minimum k for SNR=3

#initialise arrays
LOG_R_S=[]
LOG_R_P=[]
LOG_PER=[]

LOG_M_S=[]
LOG_M_P=[]

A=[]
R_H=[]

TDUR=[]

NOISE_NGTS=[]
NOISE_TESS=[]
NOISE_CORALIE=[]
NOISE_HARPS=[]

SIGNAL_PHOT=[]
SIGNAL_SPEC=[]

NGTS=[]
TESS=[]
CORALIE=[]
HARPS=[]

SNR_RATIO_CN=[]
SNR_RATIO_CT=[]
SNR_RATIO_HN=[]
SNR_RATIO_HT=[]


#begin sim.
i=0.
while i<ilen+1.:
        log_r_s = -1. + (i/ilen)*2. #log stellar radius (r_sun)
        log_m_s = 0.11854831*log_r_s**3. + -0.54426878*log_r_s**2. + 0.64555162*log_r_s + -0.00662566 #define stellar mass using cubic relation
        
        j=0.
        while j<jlen+1.:
                log_r_p = -1. + (j/jlen)*1.3 #log planet radius (r_jup)
                log_m_p = np.log10(predict_from_measurement(measurement=((10.**log_r_p)*(r_jup/r_earth)), measurement_sigma=0.0, result_dir=None, dataset='kepler', is_posterior=False, use_lookup=True)[0] * (m_earth/m_jup))
                
                signal_phot = (((10.**log_r_p)*r_jup)/((10.**log_r_s)*r_sun))**2. #calculate photometric signal size
                
                if (signal_phot/(ngts_func(Imag)/3.)) >= 3.:
                    ngts=1
                else:
                    ngts=0
                
                if (((10.**log_r_p)*r_jup) <= 0.5 * ((10.**log_r_s)*r_sun)) & (((10.**log_m_p)*m_jup) <= ((10.**log_m_s)*m_sun)): #check if planet radius <= half star radius & if check if planet mass < star mass
                            k=0.
                            while k<klen+1.:
                                    log_per = 0. + (k/klen)*3. #log period (days)
                                
                                    a = (((10.**log_per)*24.*60.*60.)**2. * G * ((10.**log_m_s)*m_sun + (10.**log_m_p)*m_jup) / (4.*np.pi**2.))**(1./3.) #calculate orbital sep.
                                    r_h = a * ( ((10.**log_m_p)*m_jup)/(3.*(10.**log_m_s)*m_sun) )**(1./3.) #calculate Hill radius
                                    
                                    if (a > ((10.**log_r_s)*r_sun + r_h)) & (a > ((10.**log_r_s)*r_sun + (10.**log_r_p)*r_jup)): #check if planet (and planet Hill radius) are outside star
                                
                                        Tdur = ( ((10.**log_per)*24.*60.*60./np.pi) * np.arcsin( ((10.**log_r_s)*r_sun + (10.**log_r_p)*r_jup) / a) ) / 3600. #calculate transt duration (less simplified)
                                
                                        signal_spec = (2.*np.pi*a*(10.**log_m_p)*m_jup) / (((10.**log_m_p)*m_jup + (10.**log_m_s)*m_sun) * ((10.**log_per)*24.*60.*60.)) #calculate spectrometric signal size
                                        
                                        #determine if each instrument can detect signal at SNR>=3.0
                                        
                                        if (signal_spec/(coralie_func(Vmag)/3.)) >= 3.:
                                            coralie=1
                                        else:
                                            coralie=0
                                        
                                        if (signal_spec/(harps_func(Vmag)/3.)) >= 3.:
                                            harps=1
                                        else:
                                            harps=0
                                        
                                        #calculate SNR ratio for each pair of instruments
                                        snr_ratio_cn = (signal_spec/(coralie_func(Vmag)/3.)) / (signal_phot/(ngts_func(Imag)/3.))
                                        snr_ratio_hn = (signal_spec/(harps_func(Vmag)/3.)) / (signal_phot/(ngts_func(Imag)/3.))
                                        
                                        #append arrays with output values
                                        LOG_R_S.append(log_r_s)
                                        LOG_R_P.append(log_r_p)
                                        LOG_PER.append(log_per)
                                        LOG_M_P.append(log_m_p)
                                        LOG_M_S.append(log_m_s)
                                        A.append(a)
                                        R_H.append(r_h)
                                        TDUR.append(Tdur)
                                        NOISE_NGTS.append(ngts_func(Imag)/3.)
                                        NOISE_CORALIE.append(coralie_func(Vmag)/3.)
                                        NOISE_HARPS.append(harps_func(Vmag)/3.)
                                        SIGNAL_PHOT.append(signal_phot)
                                        SIGNAL_SPEC.append(signal_spec)
                                        NGTS.append(ngts)
                                        HARPS.append(harps)
                                        CORALIE.append(coralie)
                                        SNR_RATIO_CN.append(snr_ratio_cn)
                                        SNR_RATIO_HN.append(snr_ratio_hn)
                                        
                                    k=k+1.0
                j=j+1.0
        print(i)
        i=i+1.0

print('array done')

df = pd.DataFrame({'LOG_R_S' : LOG_R_S, 'LOG_R_P' : LOG_R_P, 'LOG_PER' : LOG_PER, 'LOG_M_S' : LOG_M_S, 'LOG_M_P' : LOG_M_P, 'A' : A, 'R_H' : R_H, 'TDUR' : TDUR, 'NOISE_NGTS' : NOISE_NGTS, 'NOISE_CORALIE' : NOISE_CORALIE, 'NOISE_HARPS' : NOISE_HARPS, 'SIGNAL_PHOT' : SIGNAL_PHOT, 'SIGNAL_SPEC' : SIGNAL_SPEC, 'NGTS' : NGTS, 'CORALIE' : CORALIE, 'HARPS' : HARPS, 'SNR_RATIO_CN' : SNR_RATIO_CN, 'SNR_RATIO_HN' : SNR_RATIO_HN}) #save outputs to dataframe

df.to_csv('specphot_post_ref_40.csv', index=False) #save dataframe to output file

print('Runtime:', (datetime.now() - start_time))
