#!/bin/bash

# =============================================================
# === Description: ERA5 parallel data download script.      ===
# === Version: 1.                                           ===      
# === Author: Mani Mahdinia                                 ===
# === Emails: mani.mahdinia@utoronto.ca,                    ===
# ===         mani.mahdinia@gmail.com                       ===    
# =============================================================


# Input parameters
ncpus=24                   # Number of processes.
NorthB=87.0                # North domain latitude.   
WestB=-199.2               # West domain longitude. 
SouthB=-0.3                # South domain latitude.
EastB=-0.8                 # East domain longitude. 
hourly_freq="03"           # Data download hourly frequency. 
start_year="1979"          # Data download start year.
end_year="2021"            # Data download end year.
end_month="08"             # Data download end month.
end_day="31"               # Data download end day.
# NOTE: For dates/hourly_freq, use the same number of digits as in the above. 


# Loading modules
module load NiaEnv/2019b
module load intel/2019u4
module load intelmpi/2019u4
module load hdf5/1.8.21
module load netcdf/4.6.3
module load intelpython3/2019u4
module load ncl/6.6.2
module load udunits/2.2.26
module load ncview/2.1.7
module load jasper/.experimental-2.0.14
module load openjpeg/2.3.1
module load gnu-parallel/20191122


# Activate virtual env
source /project/p/peltier/mahdinia/pyEnvs_mani/pyDefEnv_mani/bin/activate


# Clear screen
clear


# Make data folder (only if it does not exist = -p)
mkdir -p Data


# Prepare gnu parallel input list 
echo -e "\n=========== Perparing month data file ==========" 
python ERA5_CDS_Data_Prepare_List_Script.py ${start_year} ${end_year} \
    ${end_month} ${end_day} &> prepare_list.log
echo "Done."
# NOTE: "-e" above enables some backslash options including "\n".

# Download PL data 
echo -e "\n======== Downloading pressure level data =======" 
parallel -j ${ncpus} python ERA5_CDS_PL_Data_Download_Script.py ${NorthB} \
    ${WestB} ${SouthB} ${EastB} ${hourly_freq} :::: input_list.txt \
    &> pl_download.log
echo "Done."

# Download SL data 
echo -e "\n======== Downloading surface level data ========" 
parallel -j ${ncpus} python ERA5_CDS_SL_Data_Download_Script.py ${NorthB} \
    ${WestB} ${SouthB} ${EastB} ${hourly_freq} :::: input_list.txt \
    &> sl_download.log
echo "Done."







