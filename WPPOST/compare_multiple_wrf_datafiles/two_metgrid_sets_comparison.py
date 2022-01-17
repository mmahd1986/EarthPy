#!/usr/bin/env python
# coding: utf-8

# ###### Disable scrolling ######

# In[1]:


get_ipython().run_cell_magic('javascript', '', 'IPython.OutputArea.prototype._should_scroll = function(lines) {\n    return false;\n}')


# ###### Save notebook back-up as .py file in the Earthpy ######

# In[1]:


# Input data
BUD = '~/EarthPy/WPPOST/compare_multiple_wrf_datafiles/'                                                          
    # Backup folder address.

# Save notebook back-up as .py file in the Earthpy
import ipyparams
nb_name = ipyparams.notebook_name
om = get_ipython().getoutput('jupyter nbconvert {nb_name} --to python --output-dir={BUD}')


# ###### Calculate differences ######

# In[2]:


# Clear variables
get_ipython().run_line_magic('reset', '-f')
# NOTE: "%reset" clears all variables. "-f" does not ask for confirmation everytime.

# Input data
case_1 = "/scratch/p/peltier/mahdinia/WRF4.3_Verification_Runs/ERA5_RC44/met_em/" 
    # First case's metgrid folder.
case_2 = "/scratch/p/peltier/mahdinia/WRF4.3_Verification_Runs/WRFTools_RC9/met_em_check_test/"
    # Second case's metgrid folder.
    
# Turn off annoying warnings
import warnings
warnings.filterwarnings('ignore')

# Make sure the environment is good
import os
import gc
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from wrf import (getvar, interplevel, vertcross, 
                 CoordPair, ALL_TIMES, to_np,
                 get_cartopy, latlon_coords,
                 cartopy_xlim, cartopy_ylim,
                 Constants,extract_vars)
   
# Check that the files exist
if not os.path.exists(case_1):
    raise ValueError("Error: Case 1 folder does not exist. "
        "Check for typos or incorrect directory.")
if not os.path.exists(case_2):
    raise ValueError("Error: Case 2 folder does not exist. "
        "Check for typos or incorrect directory.")       

# Get listsof files
files_1 = get_ipython().getoutput("ls {case_1+'met_em.*'}")
files_1 = files_1[1:] 
files_2 = get_ipython().getoutput("ls {case_2+'met_em.*'}")
files_2 = files_2[1:] 
    
# Check the number of files
if len(files_1)!=len(files_2):
    raise ValueError("len(files_1)!=len(files_2). "
        "Number of files not equal.")
    
# Number of files
NF = len(files_1)

# Difference arrays
minV12_a = np.zeros((NF,105)); maxV12_a = np.zeros((NF,105))

# Display extra line
print("")

# Go over all records
for t in np.arange(NF):
    
    # Display message
    print("Processing time step "+str(t+1)+" / "+str(NF))
    
    # Open metgrid files
    metgrid_1 = Dataset(files_1[t])
    metgrid_2 = Dataset(files_2[t])

    # Go though variables
    c = 0
    for var in ['PRES','SOIL_LAYERS','SM','ST','SM100289','SM028100',         'SM007028','SM000007','ST100289','ST028100','ST007028','ST000007',         'SNOWH','SNOW','SST','SEAICE','SKINTEMP','PMSL','PSFC',         'LANDSEA','DEWPT','RH','VV','UU','TT', 'GHT', 'OL4SS',         'OL3SS','OL2SS','OL1SS','OA4SS','OA3SS','OA2SS', 'OA1SS',         'VARSS','CONSS','OL4LS','OL3LS','OL2LS','OL1LS','OA4LS',         'OA3LS','OA2LS','OA1LS','VARLS','CONLS','SANDFRAC','CLAYFRAC',         'EROD','CANFRA','IMPERV','FRC_URB2D','URB_PARAM',         'LAKE_DEPTH', 'VAR_SSO', 'OL4', 'OL3', 'OL2', 'OL1',         'OA4','OA3','OA2','OA1','VAR', 'CON', 'SNOALB', 'LAI12M',         'GREENFRAC','ALBEDO12M','SCB_DOM','SOILCBOT','SCT_DOM',         'SOILCTOP','SOILTEMP','HGT_M','LU_INDEX','LANDUSEF',         'COSALPHA_V','SINALPHA_V','COSALPHA_U','SINALPHA_U',         'XLONG_C','XLAT_C','LANDMASK','COSALPHA','SINALPHA',         'F','E','MAPFAC_UY','MAPFAC_VY','MAPFAC_MY','MAPFAC_UX',         'MAPFAC_VX','MAPFAC_MX','MAPFAC_U','MAPFAC_V','MAPFAC_M',         'CLONG','CLAT','XLONG_U','XLAT_U','XLONG_V', 'XLAT_V',         'XLONG_M','XLAT_M']:
        minV12 = 1E40; maxV12 = -1E40
        masked = False    
        V1 = to_np(getvar(metgrid_1,var,timeidx=ALL_TIMES))        
        V2 = to_np(getvar(metgrid_2,var,timeidx=ALL_TIMES))       
        if (((isinstance(V1,np.ma.MaskedArray)) and (not(isinstance(V2,np.ma.MaskedArray))))             or
            ((isinstance(V2,np.ma.MaskedArray)) and (not(isinstance(V1,np.ma.MaskedArray))))):
            raise ValueError("Mask inconsistency."
                'V1 is masked but V2 isn''t, or V2 is masked but V1 isn''t.')
        if ((isinstance(V1,np.ma.MaskedArray)) and (isinstance(V2,np.ma.MaskedArray))):       
            masked = True        
            V1 = np.where(V1.mask == 0, V1, 9999)
            V2 = np.where(V2.mask == 0, V2, 9999)
        if ((isinstance(V1,np.ma.MaskedArray)) or (isinstance(V2,np.ma.MaskedArray))):
            raise ValueError("Error occured during unmasking."
                'Could not unmask ',var,'!')
        dV12 = V1-V2
        minV12 = np.min([minV12,np.min(dV12)])
        maxV12 = np.max([maxV12,np.max(dV12)]) 
        minV12_a[t,c] = minV12
        maxV12_a[t,c] = maxV12           
        if (masked==True):
            print('This var was initially masked and was therefore umasked.')   
        c = c+1
        gc.collect()
        
# Calculate max and min vs time
minV12_at = np.min(minV12_a,axis=1)
maxV12_at = np.max(maxV12_a,axis=1)       


# ###### Plot/show differences ######

# In[3]:


# Plot min and max vs time
fig = plt.figure(figsize=(12, 8))
ax = plt.gca()
plt.plot(minV12_at,'k-',linewidth=2)
plt.plot(maxV12_at,'k--',linewidth=2)
ax.tick_params(axis='x',labelsize=18)
ax.tick_params(axis='y',labelsize=18)
ax.set_xlabel('Time index',fontsize=25)
[x.set_linewidth(3) for x in ax.spines.values()]

# Show global min and max
print('\nGlobal minV12 =',"{:0.2e}".format(np.min(minV12_a))) 
print('Global maxV12 =',"{:0.2e}".format(np.max(maxV12_a)),'\n')

