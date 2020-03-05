# SpecPhot

Data files and plotting script for the 3D parameter space data from the paper:

**SpecPhot: A Comparison of Spectroscopic and Photometric Exoplanet Follow-Up Methods - Benjamin. F. Cooke & Don Pollacco**

Data files are included for three different V-band magnitudes; 8, 11 and 14 (zipped .csv files).
- specphot_8.zip
- specphot_11.zip
- specphot_14.zip

Plotting script is [3d_plotting_update.py](3d_plotting_update.py)

To better visualise the data presented in the accompanying paper download the data files and run the plotting script.

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
