# SpecPhot

Simulation codes, data files and plotting scripts for the 3D parameter space data from the paper:

**SpecPhot: A Comparison of Spectroscopic and Photometric Exoplanet Follow-Up Methods - Benjamin. F. Cooke & Don Pollacco**

### Plotting
Data files are included for three different V-band magnitudes; 8, 11 and 14 (zipped csv files).
- specphot_8.zip
- specphot_11.zip
- specphot_14.zip

Plotting script is [3d_plotting_update.py](3d_plotting_update.py) (python script).

To better visualise the data presented in the accompanying paper download the data files and run the plotting script. The data is included to recreate and manipulate figures 3, 4, 6 & 7 from the SpecPhot paper for all three simulated magnitudes.

The script contains the option for 8 user inputs (mag is entered as an integer, all other options are entered as strings):
1. mag - Choose V-mand magnitude
   - 8
   - 11
   - 14
2. phot - Choose photometry instrument
   - NGTS ([Wheatley et al. 2018](https://ui.adsabs.harvard.edu/abs/2018MNRAS.475.4476W/abstract))
3. spec - Choose spectroscopy instrument
   - HARPS ([Mayor et al. 2003](https://ui.adsabs.harvard.edu/abs/2003Msngr.114...20M/abstract))
   - CORALIE ([Queloz et al. 2000](https://ui.adsabs.harvard.edu/abs/2000A%26A...354...99Q/abstract))
4. data - Choose what data to compare
   - SNR - plot the ratio of SNR value at each point for the chosen instruments
   - TIME - plot the ratio of follow-up time at each point for the chosen instruments
   - WEIGHT - plot the weighted combination of SNR and follow-up time at each point for the chosen instruments
5. display - Choose how much data to display
   - ALL - show the full range of parameter space accessible to both instruments
   - \>1 - show only data with a ratio >=1 (favours spectroscopy)
   - <1 - show only data with a ratio <=1 (favours photometry)
   - ~1 - show only data with a ratio between 5/6 and 6/5 (both methods comparable, useful for examining the transition region)
6. phot_plus - Plot parameter space available to photometry only
   - YES
   - NO
7. spec_plus - Plot parameter space available to spectroscopy only
   - YES
   - NO
8. neither_plus - Plot parameter space not available to either method
   - YES
   - NO

For more details please read the associated paper.

### Simulation codes
We also include the necessary files required to reproduce the simulation described in this paper. Requires the python modules MRExo (https://shbhuk.github.io/mrexo/) and ephem (https://pypi.org/project/ephem/).

These codes are (in order):

1. [specphot.py](specphot.py) - Reads in noise data for the chosen instruments (in folder noise/) and calculates SNR for each point in a 3D grid of stellar radius, planetary radius and period. User can define V-band magnitude of host and size of grid. Data are written to file.
2. [night_day.py](night_day.py) - Reads in data from specphot.py and calculates NGTS follow-up time for all grid points for which SNR(NGTS)>=3.0. Data are written to file.
3. [phase.py](phase.py) & [phase_coralie.py](phase_coralie.py) - Reads in data from specphot.py and calculates spectroscopic follow-up time for all grid points for which SNR(HARPS)>=3.0 or SNR(CORALIE)>=3.0 respectively. Data are written to file.
4. [combine_time_data.py](combine_time_data.py) - combines the outputs of night_day.py, phase.py & phase_coralie.py. Data are written to file.

The output of combine_time_data.py can then be passed to 3d_plotting_update.py to create the 3D plots.
To report any bugs or problems with the codes please contact me at b.cooke@warwick.ac.uk.
