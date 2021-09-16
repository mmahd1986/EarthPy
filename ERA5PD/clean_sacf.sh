#!/bin/bash

# =============================================================
# === Description: Clean split_and_compress_files.sh        ===
# ===              generated outputs and kill all related   ===
# ===              processes.                               ===
# === Version: 1.                                           ===      
# === Author: Mani Mahdinia                                 ===
# === Emails: mani.mahdinia@utoronto.ca,                    ===
# ===         mani.mahdinia@gmail.com                       ===    
# =============================================================


# Clear
clear


# Kill all previous execs
procs=$(pgrep -d, -u mahdinia -x grib_filter)
if [ -n "${procs}" ]; then
    kill $(ps -f -p"$(pgrep -d, -u mahdinia -x grib_filter)" | awk 'NR>=2 {print $2}')
fi
procs=$(pgrep -d, -u mahdinia -x grib_set)
if [ -n "${procs}" ]; then
    kill $(ps -f -p"$(pgrep -d, -u mahdinia -x grib_set)" | awk 'NR>=2 {print $2}')
fi
# NOTE: The way procs is defined is how we get the output of a command
# into a variable in the shell script.


# Delete previous data, files, etc
rm -rf Test_Comp/Split_Data_Files rules_file_pl.txt \
    rules_file_sl.txt pl_split.log sl_split.log \
    pl_monthly_data_file_list.txt sl_monthly_data_file_list.txt \
    pl_split_data_file_list.txt sl_split_data_file_list.txt \
    pl_compress.log sl_compress.log split_and_compress_files.log
    

# Show folder contents
ls -alh


# Show user ps
ps -u mahdinia

