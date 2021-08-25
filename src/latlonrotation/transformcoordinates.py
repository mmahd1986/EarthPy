'''
Name: transformcoordinates
Description: This file contains the functions needed for transformation between
             standard and rotated lat-lon coordinates.   
Creation Date: 2021-08-24
Author: Mani Mahdinia
'''

# Imports
import numpy as np
from numpy import (sin,cos,tan,arctan2,arcsin,pi)


# =========================================================
# === Function to transform from standard to rotated    ===
# === lat-lon coordinates.                              ===
# ===                                                   ===
# === Inputs/outputs:                                   ===
# === (lat, lon) is in standard lat-lon coordinates.    ===
# === (latp, lonp) is in rotated lat-lon coordinates.   ===
# === phi is rotation z axis (1st rotation).            ===
# === nu is rotation around y=y' axis (2nd rotation).   ===
# === All inputs/outputs in degrees.                    ===
# ===                                                   ===
# === Value recommendation:                             ===
# === If also working with WRF and using the values     ===
# === recommended (WRF user's Guide, version 4.0, page  ===
# === 3-13), set phi = 180+ref_lon & nu = ref_lat.      ===
# =========================================================

def nonrotated2rotated(nu,phi,lat,lon):
    
    # Check if lat and lon have the same lengths
    if (len(lat)!=len(lon)):
        raise ValueError("Error: len(lat)!=len(lon). "
            "Check the lat and lon data lengths.")
    
    # Convert lat, lon, nu, and phi to radians
    lat = lat*pi/180
    lon = lon*pi/180
    nu = nu*pi/180
    phi = phi*pi/180
    
    # Adjust lon
    lon = lon+pi
    
    # Initialize latp and lonp
    latp = np.zeros(len(lat))
    lonp = np.zeros(len(lat))
    
    # Calculate latp and lonp
    for i in np.arange(len(lat)):  
        latp[i] = arcsin(-sin(nu)*cos(phi)*cos(lat[i])*cos(lon[i])-sin(nu)* \
            sin(phi)*cos(lat[i])*sin(lon[i])+cos(nu)*sin(lat[i]))*180/pi      
        lonp[i] = arctan2(-sin(phi)*cos(lat[i])*cos(lon[i])+cos(phi)* \
            cos(lat[i])*sin(lon[i]),cos(nu)*cos(phi)*cos(lat[i])*cos(lon[i])+ \
            cos(nu)*sin(phi)*cos(lat[i])*sin(lon[i])+sin(nu)*sin(lat[i]))*180/pi       
        
    return [latp,lonp] 


# =========================================================
# === Function to transform from rotated to standard    ===
# === lat-lon coordinates.                              ===
# ===                                                   ===
# === Inputs/outputs:                                   ===
# === (lat, lon) is in standard lat-lon coordinates.    ===
# === (latp, lonp) is in rotated lat-lon coordinates.   ===
# === nu is rotation around y' axis (1st rotation).     ===
# === phi is rotation z=z' axis (2nd rotation).         ===
# === All inputs/outputs in degrees.                    ===
# ===                                                   ===
# === Value recommendation:                             ===
# === If also working with WRF and using the values     ===
# === recommended (WRF user's Guide, version 4.0, page  ===
# === 3-13), set phi = -(180+ref_lon) & nu = -ref_lat.  ===
# =========================================================

def rotated2nonrotated(nu,phi,latp,lonp):
    
    # Check if latp and lonp have the same lengths
    if (len(latp)!=len(lonp)):
        raise ValueError("Error: len(latp)!=len(lonp). "
            "Check the latp and lonp data lengths.")
    
    # Convert latp, lonp, nu, and phi to radians
    latp = latp*pi/180
    lonp = lonp*pi/180
    nu = nu*pi/180
    phi = phi*pi/180        
    
    # Initialize lat and lon
    lat = np.zeros(len(latp))
    lon = np.zeros(len(latp))
    
    # Calculate lat and lon
    for i in np.arange(len(latp)):   
        lat[i] = arcsin(-sin(nu)*cos(latp[i])*cos(lonp[i])+cos(nu)*sin(latp[i]))*180/pi      
        lon[i] = (arctan2(sin(lonp[i]),tan(latp[i])*sin(nu)+cos(lonp[i])*cos(nu))-phi)*180/pi 
            
    # Adjust lon
    lon = lon-180             
        
    return [lat,lon] 



