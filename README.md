# SpecPhot

Data files and plotting script for the 3D parameter space data from the paper:
SpecPhot: A Comparison of Spectroscopic and Photometric Exoplanet Follow-Up Methods
Benjamin. F. Cooke & Don Pollacco

Data files are included for three differnt V-band magnitudes; 8, 11 and 14.
aaa_8.csv
aaa_11.csv
aaa_14.csv

Plotting script is xxx.py

To better visualise the data presented in the accompanying paper download the datafiles and run the plotting script.

The script contains the option for 8 user inputs:
mag - Choose V-mand magnitude
      8
      11
      14
phot - Choose photometry instrument
      NGTS ()
spec - Choose spectroscopy instrument
      HARPS ()
      CORALIE ()
data - Choose what data to compare
      SNR - plot the ratio of SNR value at each point for the chosen instruments
      TIME - plot the ratio of follow-up time at each point for the chosen instruments
      WEIGHT - plot the weighted combination of SNR and follow-up time at each point for the chosen instruments
display - Choose how much data to display
      ALL - show the full range of parameter space acessible to both instruments
      >1 - show only data with a ratio >=1 (favours spectroscopy)
      <1 - show only data with a ratio <=1 (favours photometry)
      ~1 - show only data with a ratio between 5/6 and 6/5 (both methods comparable, useful for examining the transition region)
phot_plus - Plot parameter space availale to photometry only
      YES
      NO
spec_plus - Plot parameter space availale to spectroscopy only
      YES
      NO
neither_plus - Plot parameter space not availale to either method
      YES
      NO

For more details please read the associated paper.
