#!/bin/bash

# =============================================================
# === Description: The script to clean download.sh          ===
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
procs=$(pgrep -d, -u mahdinia -x python)
if [ -n "${procs}" ]; then
    kill $(ps -f -p"$(pgrep -d, -u mahdinia -x python)" | awk 'NR>=2 {print $2}')
fi
# NOTE: The way procs is defined is how we get the output of a command
# into a variable in the shell script.


# Delete previous data, files, etc
rm -rf Data input_list.txt prepare_list.log sl_download.log pl_download.log download.log \
    pl_download_c.log sl_download_c.log download_continue.log


# Show folder contents
ls -alh


# Show user ps
ps -u mahdinia

