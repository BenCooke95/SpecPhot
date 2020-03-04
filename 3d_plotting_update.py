from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib

####USER INPUTS####
mag = 11 #Choose V-mand magnitude: 8, 11 or 14
phot = 'NGTS' #Choose photometry instrument: NGTS only
spec = 'HARPS' #Choose spectroscopy instrument: HARPS or CORALIE
data = 'SNR' #Choose what data to compare: SNR, TIME or WEIGHT
display = 'ALL' #Choose how much data to display: ALL, >1, <1, ~1
phot_plus = 'NO' #Plot parameter space availale to photometry only: YES or NO
spec_plus = 'NO' #Plot parameter space availale to spectroscopy only: YES or NO
neither_plus = 'NO' #Plot parameter space not availale to either method: YES or NO
###################
	
col = data+'_RATIO_'+spec[0]+phot[0] #Define data column based on user inputs
print('col:', col)

plt.rcParams.update({'font.size': 15}) #Set plot text size


#Function to rescale logarithmic colour bar around 1
def shiftedColorMap(cmap, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'): #https://stackoverflow.com/questions/7404116/defining-the-midpoint-of-a-colormap-in-matplotlib
    cdict = {'red': [], 'green': [], 'blue': [], 'alpha': []}
    reg_index = np.linspace(start, stop, 257)
    shift_index = np.hstack([np.linspace(0.0, midpoint, 128, endpoint=False), np.linspace(midpoint, 1.0, 129, endpoint=True)])
    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)
        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))
    newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)
    return newcmap


#Read in chosen dataset
if mag == 11:
	array = pd.read_csv('specphot_alltime_post_ref_40.csv', sep=',')
specphot_all = pd.DataFrame(array)
print('All:', len(specphot_all))

#Calculate subset sizes based on chosen instruments
specphot = specphot_all.loc[(specphot_all[phot] == 1) & (specphot_all[spec] == 1)]
print(phot+'&'+spec+':', len(specphot), ',', 100.*len(specphot)/len(specphot_all),'%')
specphot_phot = specphot_all.loc[(specphot_all[phot] == 1) & (specphot_all[spec] == 0)]
print(phot+'only:', len(specphot_phot), ',', 100.*len(specphot_phot)/len(specphot_all),'%')
specphot_spec = specphot_all.loc[(specphot_all[spec] == 1) & (specphot_all[phot] == 0)]
print(spec+'only:', len(specphot_spec), ',', 100.*len(specphot_spec)/len(specphot_all),'%')
specphot_NONE = specphot_all.loc[(specphot_all[phot] == 0) & (specphot_all[spec] == 0)]
print('Neither:', len(specphot_NONE), ',', 100.*len(specphot_NONE)/len(specphot_all),'%')

#Calculate midpoint for scaled colourbar
mid = (0.-np.log10(min(specphot[col])))/(np.log10(max(specphot[col]))-np.log10(min(specphot[col])))
print('mid:', mid)

#Choose oignal colorbar and scale accordingly
orig_cmap = matplotlib.cm.seismic_r
shifted_cmap = shiftedColorMap(orig_cmap, midpoint=mid, name='shifted')

#Define data subset basen on how much data chosen to be displayed
if display == 'ALL':
	specphot_sub = specphot
elif display == '>1':
	specphot_sub = specphot.loc[(specphot[col] >= 1)]
elif display == '<1':
	specphot_sub = specphot.loc[(specphot[col] <= 1)]
elif display == '~1':
	specphot_sub = specphot.loc[(specphot[col] <= (6./5.)) & (specphot[col] >= (5./6.))]



#Begin plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#Plot the data
img=ax.scatter(specphot_sub['LOG_R_P'], specphot_sub['LOG_R_S'], specphot_sub['LOG_PER'], c=specphot_sub[col], norm=matplotlib.colors.LogNorm(), cmap=shifted_cmap, vmin=min(specphot[col]), vmax=max(specphot[col]))

#Plot additional parameter space regions if required
if phot_plus == 'YES':
	ax.scatter(specphot_phot['LOG_R_P'], specphot_phot['LOG_R_S'], specphot_phot['LOG_PER'], color='orange')
if spec_plus == 'YES':
	ax.scatter(specphot_spec['LOG_R_P'], specphot_spec['LOG_R_S'], specphot_spec['LOG_PER'], color='cyan')
if neither_plus == 'YES':
	ax.scatter(specphot_NONE['LOG_R_P'], specphot_NONE['LOG_R_S'], specphot_NONE['LOG_PER'], color='k')

#Set plot paramaters
ax.set_xlabel(r'$R_p$ ($R_{\rm Jup}$)')
ax.set_ylabel(r'$R_\star$ ($R_\odot$)')
ax.set_zlabel(r'Period (days)')
ax.set_xticks([np.log10(0.1),np.log10(0.2),np.log10(0.5),np.log10(1),np.log10(1.99)])
ax.set_xticklabels([0.1,0.2,0.5,1,2])
ax.set_yticks([np.log10(0.1),np.log10(0.2),np.log10(0.5),np.log10(1),np.log10(2),np.log10(5),np.log10(10)])
ax.set_yticklabels([0.1,0.2,0.5,1,2,5,10])
ax.set_zticks([np.log10(1),np.log10(10),np.log10(100),np.log10(1000)])
ax.set_zticklabels([1,10,100,1000])
ax.set_xlim(max(specphot_all['LOG_R_P']), min(specphot_all['LOG_R_P']))
ax.set_ylim(max(specphot_all['LOG_R_S']), min(specphot_all['LOG_R_S']))
ax.set_zlim(min(specphot_all['LOG_PER']), max(specphot_all['LOG_PER']))

#Set colourbar parameters
if data == 'SNR':
	fig.colorbar(img, format='%.3g', ticks=[0.0001,0.0002,0.0005,0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.5,1,2,5,10,20,50,100,200,500,1000,2000,5000,10000], label=r'$\rm SNR_{'+spec+'}/SNR_{'+phot+'}$')
elif data == 'TIME':
	fig.colorbar(img, format='%.3g', ticks=[0.0001,0.0002,0.0005,0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.5,1,2,5,10,20,50,100,200,500,1000,2000,5000,10000], label=r'$\rm Follow-up\ time_{'+spec+'}/Follow-up\ time_{'+phot+'}$')
elif data == 'WEIGHT':
	fig.colorbar(img, format='%.3g', ticks=[0.0001,0.0002,0.0005,0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.5,1,2,5,10,20,50,100,200,500,1000,2000,5000,10000], label=r'$\rm Weighted\ value$')

#Set 3d view
ax.view_init(elev=40., azim=315.)

#show plot
plt.tight_layout()
plt.show()
plt.close()
