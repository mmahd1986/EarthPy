#!/usr/bin/env python
# coding: utf-8

# ###### Disable scrolling ######

# In[1]:


get_ipython().run_cell_magic('javascript', '', 'IPython.OutputArea.prototype._should_scroll = function(lines) {\n    return false;\n}')


# ######  Save notebook back-up as .py file in the Earthpy ###### 

# In[2]:


# Input data
BUD = '~/EarthPy/WPPOST/compare_multiple_wrf_datafiles'
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
file_1 = "/scratch/p/peltier/mahdinia/WRF4.3_Verification_Runs/ERA5_RC44/wrfbdymod_d01" 
    # First case's wrfinput file.
file_2 = "/scratch/p/peltier/mahdinia/WRF4.3_Verification_Runs/WRFToolsPropCheck_RC8/wrfbdymod_d01"
    # Second case's wrfinput file.
        
# Turn off annoying warnings
import warnings
warnings.filterwarnings('ignore')

# Make sure the environment is good
import os
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

# Open wrfinput files
wrfin_1 = Dataset(file_1)
wrfin_2 = Dataset(file_2)

# ============== Calculate and print array diff values ==============

# Prompt on screen
print('\n>>>>>>>>>>>>>>>>>>>>>>>>>> Difference values <<<<<<<<<<<<<<<<<<<<<<<<<<<\n')

# Difference arrays
minV12_a = np.zeros((128,1)); maxV12_a = np.zeros((128,1))

# Go though variables
c = 0
for var in ['U_BXS','U_BXE','U_BYS','U_BYE','U_BTXS','U_BTXE',     'U_BTYS','U_BTYE','V_BXS','V_BXE','V_BYS','V_BYE','V_BTXS',     'V_BTXE','V_BTYS','V_BTYE','W_BXS','W_BXE','W_BYS','W_BYE',     'W_BTXS','W_BTXE','W_BTYS','W_BTYE','PH_BXS','PH_BXE',     'PH_BYS','PH_BYE','PH_BTXS','PH_BTXE','PH_BTYS','PH_BTYE',     'T_BXS','T_BXE','T_BYS','T_BYE','T_BTXS','T_BTXE','T_BTYS',     'T_BTYE','MU_BXS','MU_BXE','MU_BYS','MU_BYE','MU_BTXS','MU_BTXE',     'MU_BTYS','MU_BTYE','QVAPOR_BXS','QVAPOR_BXE','QVAPOR_BYS',     'QVAPOR_BYE', 'QCLOUD_BXS', 'QCLOUD_BXE', 'QCLOUD_BYS',     'QCLOUD_BYE','QRAIN_BXS','QRAIN_BXE','QRAIN_BYS','QRAIN_BYE',     'QICE_BXS','QICE_BXE','QICE_BYS','QICE_BYE','QSNOW_BXS',     'QSNOW_BXE','QSNOW_BYS','QSNOW_BYE','QGRAUP_BXS','QGRAUP_BXE',     'QGRAUP_BYS','QGRAUP_BYE','QVAPOR_BTXS','QVAPOR_BTXE',     'QVAPOR_BTYS','QVAPOR_BTYE','QCLOUD_BTXS','QCLOUD_BTXE',     'QCLOUD_BTYS','QCLOUD_BTYE','QRAIN_BTXS','QRAIN_BTXE',     'QRAIN_BTYS','QRAIN_BTYE','QICE_BTXS','QICE_BTXE','QICE_BTYS',     'QICE_BTYE','QSNOW_BTXS','QSNOW_BTXE','QSNOW_BTYS','QSNOW_BTYE',     'QGRAUP_BTXS','QGRAUP_BTXE','QGRAUP_BTYS','QGRAUP_BTYE',     'QNICE_BXS','QNICE_BXE','QNICE_BYS','QNICE_BYE','QNRAIN_BXS',     'QNRAIN_BXE','QNRAIN_BYS','QNRAIN_BYE','QNICE_BTXS','QNICE_BTXE',     'QNICE_BTYS','QNICE_BTYE','QNRAIN_BTXS','QNRAIN_BTXE','QNRAIN_BTYS',     'QNRAIN_BTYE','HT_SHAD_BXS','HT_SHAD_BXE','HT_SHAD_BYS','HT_SHAD_BYE',     'HT_SHAD_BTXS','HT_SHAD_BTXE','HT_SHAD_BTYS','HT_SHAD_BTYE',     'PC_BXS','PC_BXE','PC_BYS','PC_BYE','PC_BTXS',     'PC_BTXE','PC_BTYS','PC_BTYE']:
    minV12 = 1E40; maxV12 = -1E40
    masked = False    
    V1 = to_np(getvar(wrfin_1,var,timeidx=ALL_TIMES))        
    V2 = to_np(getvar(wrfin_2,var,timeidx=ALL_TIMES))       
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
    minV12 = np.min([minV12,np.min(dV12)])
    maxV12 = np.max([maxV12,np.max(dV12)]) 
    minV12_a[c] = minV12
    maxV12_a[c] = maxV12          
    print('Variable = ',var) 
    if (masked==True):
        print('This var was initially masked and was therefore umasked.')   
    print('min dV12  =',"{:0.2e}".format(minV12), end=', ')
    print('max dV12  =',"{:0.2e}".format(maxV12))
    c = c+1

# Global min and max
print('\nGlobal minV12 =',"{:0.2e}".format(np.min(minV12_a))) 
print('Global maxV12 =',"{:0.2e}".format(np.max(maxV12_a)),'\n')

