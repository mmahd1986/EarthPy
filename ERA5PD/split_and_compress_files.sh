#!/bin/bash

# =============================================================
# === Description: The script for breaking files into       ===
# ===              files containing only 1 timestamp each,  ===
# ===              and also compressing the files.          ===
# === Version: 1.                                           ===      
# === Author: Mani Mahdinia                                 ===
# === Emails: mani.mahdinia@utoronto.ca,                    ===
# ===         mani.mahdinia@gmail.com                       ===    
# =============================================================


# Input parameters
ncpus=24              # Number of processes.
compress=1            # 1 to compress the files, 0 not to.
comp_type='grid_jpeg' # Compression type: grid_jpeg or grid_png.
replaceregcomp=0      # 1 replaces uncompressed files with  
                      #   compressed ones, 0 keeps both.


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


# Clear screen
clear


# Check if Data directory exists and is not empty
if [ ! -d "Data" ]; then
    echo "Data directory does not exist. Run and finish download.sh first."
    exit 1
fi
if [ ! "$(ls -A Data)" ]; then
    echo "Data directory is empty. Run and finish download.sh first."
    exit 1
fi


# Make split and compressed data folders (only if they do not exist = -p)
mkdir -p Data/Split_Data_Files
if [ $compress == 1 ]; then
    mkdir -p Data/Split_Data_Files/Compressed/
fi    


# Make the rules files
echo "write \"./Data/Split_Data_Files/ERA5-[date][time]-pl.grib\";" > rules_file_pl.txt
echo "write \"./Data/Split_Data_Files/ERA5-[date][time]-sl.grib\";" > rules_file_sl.txt


# Generate files containing name of monthly files
echo -e "\n=========== Perparing monthly file name list ==========" 
find ./Data/ -maxdepth 1 -type f -name ERA5-*-pl.grib \
    | sort > pl_monthly_data_file_list.txt 
find ./Data/ -maxdepth 1 -type f -name ERA5-*-sl.grib \
    | sort > sl_monthly_data_file_list.txt     
echo "Done."
# NOTE: "-e" above enables some backslash options including "\n".

# Split PL files 
echo -e "\n======== Splitting pressure level files =======" 
parallel -j ${ncpus} ~/eccodes/bin/grib_filter rules_file_pl.txt :::: pl_monthly_data_file_list.txt \
    &> pl_split.log
echo "Done."

# Split SL files 
echo -e "\n======== Splitting surface level files =======" 
parallel -j ${ncpus} ~/eccodes/bin/grib_filter rules_file_sl.txt :::: sl_monthly_data_file_list.txt \
    &> sl_split.log
echo "Done."


# If needed, compress the files
if [ $compress == 1 ]; then

    # Generate files containing name of split files
    echo -e "\n=========== Perparing split file name list ==========" 
    find ./Data/Split_Data_Files/ -maxdepth 1 -type f -name ERA5-*-pl.grib \
        | sort > pl_split_data_file_list.txt 
    find ./Data/Split_Data_Files/ -maxdepth 1 -type f -name ERA5-*-sl.grib \
        | sort > sl_split_data_file_list.txt     
    echo "Done."

    # Compress PL files 
    echo -e "\n======== Compressing pressure level files =======" 
    parallel -j ${ncpus} ~/eccodes/bin/grib_set -s edition=2,packingType=${comp_type} \
        {= '$arg' =} ./Data/Split_Data_Files/Compressed/{/}_1 :::: \
        pl_split_data_file_list.txt &> pl_compress.log
    echo "Done."

    # Compress SL files 
    echo -e "\n======== Compressing surface level files =======" 
    parallel -j ${ncpus} ~/eccodes/bin/grib_set -s \
        localDefinitionNumber=1,edition=2,packingType=${comp_type} {= '$arg' =} \
        ./Data/Split_Data_Files/Compressed/{/}_1 :::: sl_split_data_file_list.txt \
        &> sl_compress.log
    echo "Done."
    
    # Rename files to remove "_1"
    for filename in ./Data/Split_Data_Files/Compressed/*_1; do 
        mv "$filename" "${filename/_1/}" 2>/dev/null
    done
    
    # Make the rules files to fix SL data soil levels  
    echo "# Fix bottom level of the lowest soil layer" > rules_file_flvl_sl.txt
    echo "if ((parameterNumber==42) || (parameterNumber==236))" >> rules_file_flvl_sl.txt
    echo "{" >> rules_file_flvl_sl.txt
    echo "set bottomLevel=255;" >> rules_file_flvl_sl.txt
    echo "}" >> rules_file_flvl_sl.txt
    echo "" >> rules_file_flvl_sl.txt
    echo "# Convert level units to cm (not m) for all the soil layers' levels" >> rules_file_flvl_sl.txt
    echo "if ((39<=parameterNumber && parameterNumber<=42) || (parameterNumber==139) || (parameterNumber==170) || (parameterNumber==183) || (parameterNumber==236))" >> rules_file_flvl_sl.txt
    echo "{" >> rules_file_flvl_sl.txt 
    echo "set scaleFactorOfFirstFixedSurface=2;" >> rules_file_flvl_sl.txt
    echo "set scaleFactorOfSecondFixedSurface=2;" >> rules_file_flvl_sl.txt      
    echo "}" >> rules_file_flvl_sl.txt
    echo "">> rules_file_flvl_sl.txt
    echo "# Write grib file" >> rules_file_flvl_sl.txt
    echo "write \"./Data/Split_Data_Files/Compressed/ERA5-[date][time]-sl.grib_1\";" >> rules_file_flvl_sl.txt      
            
    # Fix SL soil data
    echo -e "\n======== Fixing the SL soil data =======" 
    parallel -j ${ncpus} ~/eccodes/bin/grib_filter rules_file_flvl_sl.txt \
        "./Data/Split_Data_Files/Compressed/"{/} :::: sl_split_data_file_list.txt \
        &> sl_flvl.log
    echo "Done." 
    
    # Remove all -sl.grib files
    rm -rf *-sl.grib
    
    # Rename files to remove "_1"
    for filename in ./Data/Split_Data_Files/Compressed/*_1; do 
        mv "$filename" "${filename/_1/}" 2>/dev/null
    done
    
    # Replace uncompressed files with compressed ones, if needed
    if [ $replaceregcomp == 1 ]; then    
      rm -rf ./Data/Split_Data_Files/ERA5-*-pl.grib
      rm -rf ./Data/Split_Data_Files/ERA5-*-sl.grib
      mv ./Data/Split_Data_Files/Compressed/* ./Data/Split_Data_Files/
      rm -rf ./Data/Split_Data_Files/Compressed/    
    fi    

fi





