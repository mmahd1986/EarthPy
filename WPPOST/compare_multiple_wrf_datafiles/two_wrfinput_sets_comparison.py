#!/usr/bin/env python
# coding: utf-8

# ###### Disable scrolling ######

# In[1]:


get_ipython().run_cell_magic('javascript', '', 'IPython.OutputArea.prototype._should_scroll = function(lines) {\n    return false;\n}')


# ###### Save notebook back-up as .py file in the Earthpy ######

# In[3]:


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
file_1 = "/scratch/p/peltier/mahdinia/WRF4.3_Verification_Runs/ERA5_RC44/wrfinput_d01" 
    # First case's wrfinput file.
file_2 = "/scratch/p/peltier/mahdinia/WRF4.3_Verification_Runs/WRFToolsPropCheck_RC8/wrfinput_d01"
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
minV12_a = np.zeros((190,1)); maxV12_a = np.zeros((190,1))

# Go though variables
c = 0
for var in ['XLAT','XLONG','LU_INDEX','ZNU','ZNW','ZS','DZS',     'VAR_SSO','EROD','U','V','W','PH','PHB','T','THM','T_INIT',     'MU','MUB','P','AL','ALB','PB','FNM','FNP','RDNW','RDN',     'DNW','DN','T_BASE','CFN','CFN1','STEP_NUMBER',     'THIS_IS_AN_IDEAL_RUN','P_HYD','Q2','T2','TH2','PSFC',     'U10','V10','RDX','RDY','DTS','DTSEPS','RESM','ZETATOP',     'CF1','CF2','CF3','QVAPOR','QCLOUD','QRAIN','QICE',     'QSNOW','QGRAUP','QNICE','QNRAIN','FCX','GCX','TOPOSLPX',     'TOPOSLPY','SHDMAX','SHDMIN','SNOALB','LANDUSEF','SOILCTOP',     'SOILCBOT','PCT_PFT','TSLB','SMOIS','SH2O','SMCREL','SEAICE',     'IVGTYP','ISLTYP','VEGFRA','SNOW','SNOWH','CANWAT','FNDSNOWH',     'FNDSOILW','FNDALBSI','FNDSNOWSI','FNDICEDEPTH','LAKE_DEPTH',     'UOCE','VOCE','FRC_URB2D','LAI','VAR','CON','OA1','OA2','OA3',     'OA4','OL1','OL2','OL3','OL4','MAPFAC_M','MAPFAC_U','MAPFAC_V',     'MAPFAC_MX','MAPFAC_MY','MAPFAC_UX','MAPFAC_UY','MAPFAC_VX',     'MF_VX_INV','MAPFAC_VY','F','E','SINALPHA','COSALPHA',     'HGT','TSK','U_BASE','V_BASE','QV_BASE','Z_BASE','U_FRAME',     'V_FRAME','P_TOP','GOT_VAR_SSO','LAT_LL_T','LAT_UL_T',     'LAT_UR_T','LAT_LR_T','LAT_LL_U','LAT_UL_U','LAT_UR_U',     'LAT_LR_U','LAT_LL_V','LAT_UL_V','LAT_UR_V','LAT_LR_V',     'LAT_LL_D','LAT_UL_D','LAT_UR_D','LAT_LR_D','LON_LL_T',     'LON_UL_T','LON_UR_T','LON_LR_T','LON_LL_U','LON_UL_U',     'LON_UR_U','LON_LR_U','LON_LL_V','LON_UL_V','LON_UR_V',     'LON_LR_V','LON_LL_D','LON_UL_D','LON_UR_D','LON_LR_D',     'T00','P00','TLP','TISO','TLP_STRAT','P_STRAT','CLDFRA',     'XLAT_U','XLONG_U','XLAT_V','XLONG_V','CLAT','ALBBCK',     'TMN','XLAND','CPLMASK','SNOWC','SR','SAVE_TOPO_FROM_REAL',     'LAKEFLAG','LAKE_DEPTH_FLAG','C1H','C2H','C1F','C2F',     'C3H','C4H','C3F','C4F','PCB','PC','LANDMASK','LAKEMASK',     'SST']:
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

