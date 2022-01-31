#!/usr/bin/env python
# coding: utf-8

# ###### Disable scrolling ######

# In[1]:


get_ipython().run_cell_magic('javascript', '', 'IPython.OutputArea.prototype._should_scroll = function(lines) {\n    return false;\n}')


# ###### Calculate differences ######

# In[ ]:


# Clear variables
get_ipython().run_line_magic('reset', '-f')
# NOTE: "%reset" clears all variables. "-f" does not ask for confirmation everytime.

# Input data
file_1 = "/scratch/p/peltier/mahdinia/WRF4.3_Verification_Runs/ERA5_RC44/wrfplev3d_d01_1979-01-01_00:00:00.nc" 
    # First case's wrfinput file.
file_2 = "/scratch/p/peltier/mahdinia/WRF4.3_Verification_Runs/WRFTools_RC9/wrfout/wrfplev3d_d01_1979-02-01_00:00:00.nc"
    # Second case's wrfinput file.
BUD = '~/EarthPy/WPPOST/compare_multiple_wrf_datafiles'                                       
    # Backup folder address.
    
# Save notebook back-up as .py file in the Earthpy
import ipyparams
nb_name = ipyparams.notebook_name
om = get_ipython().getoutput('jupyter nbconvert {nb_name} --to python --output-dir={BUD} ')
    
# Turn off annoying warnings
import warnings
warnings.filterwarnings('ignore')

# Make sure the environment is good
import os
import gc
import numpy as np
from netCDF4 import Dataset
from wrf import (getvar, interplevel, vertcross, 
                 CoordPair, ALL_TIMES, to_np,
                 get_cartopy, latlon_coords,
                 cartopy_xlim, cartopy_ylim,
                 Constants,extract_vars)
   
# Check that the files exist
if not os.path.exists(file_1):
    raise ValueError("Error: Case 1 file does not exist. "
        "Check for typos or incorrect directory.")
if not os.path.exists(file_2):
    raise ValueError("Error: Case 2 file does not exist. "
        "Check for typos or incorrect directory.")       

# Open wrfplev files
wrfin_1 = Dataset(file_1)
wrfin_2 = Dataset(file_2)

# Getting number of time steps
V2 = to_np(getvar(wrfin_2,'T2',timeidx=ALL_TIMES)) 
NT = V2.shape[0] 
del V2

# ============== Calculate and print array diff values ==============

# Prompt on screen
print('\n>>>>>>>>>>>>>>>>>>>>>>>>>> Difference values <<<<<<<<<<<<<<<<<<<<<<<<<<<\n')

# Difference arrays
minV12_a = np.zeros((NT,27)); maxV12_a = np.zeros((NT,27))

# Go though variables
c = 0
for var in ['XLAT','XLONG','Q2','T2','PSFC','U10','V10','ITIMESTEP',     'XTIME','PBLH','P_PL','U_PL','V_PL','T_PL','RH_PL','GHT_PL',     'S_PL','TD_PL','Q_PL','C1H','C2H','C1F','C2F','C3H','C4H',     'C3F','C4F']:
    masked = False    
    V1 = to_np(getvar(wrfin_1,var,timeidx=ALL_TIMES))        
    V2 = to_np(getvar(wrfin_2,var,timeidx=ALL_TIMES)) 
    # Modify index ranges to accomodate file time range differences
    LR = 248
    if V1.ndim==1:
        V1 = V1[LR:]
    elif V1.ndim==2:
        V1 = V1[LR:,:]
    elif V1.ndim==3:
        V1 = V1[LR:,:,:]
    elif V1.ndim==4:    
        V1 = V1[LR:,:,:,:]       
    gc.collect()   
    if (((isinstance(V1,np.ma.MaskedArray)) and (not(isinstance(V2,np.ma.MaskedArray))))         or
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
    del V1, V2
    gc.collect()     
    nd = dV12.ndim
    temp = dV12
    for dim in np.arange(nd,0,step=-1):
        temp = temp.min(axis=dim)
    minV12_a[:,c] = temp        
    temp = dV12
    for dim in np.arange(nd,0,step=-1):
        temp = temp.max(axis=dim)    
    maxV12_a[:,c] = temp          
    print('Variable = ',var) 
    if (masked==True):
        print('This var was initially masked and was therefore umasked.')   
    print('min dV12  =',"{:0.2e}".format(np.min(minV12_a[:,c])), end=', ')
    print('max dV12  =',"{:0.2e}".format(np.max(maxV12_a[:,c])))
    c = c+1
    del dV12, temp
    gc.collect()

# Global min and max
print('\nGlobal minV12 =',"{:0.2e}".format(np.min(minV12_a))) 
print('Global maxV12 =',"{:0.2e}".format(np.max(maxV12_a)),'\n')

