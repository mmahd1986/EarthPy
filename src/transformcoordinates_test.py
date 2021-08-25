'''
Name: transformcoordinates_test
Description: This file contains tests for transformcoordinates.py.  
Creation Date: 2021-08-24
Author: Mani Mahdinia
'''

# Imports
from latlonrotation.transformcoordinates import nonrotated2rotated
from latlonrotation.transformcoordinates import rotated2nonrotated
import numpy as np

# Print about word 'TRANS'
print('\nIMPORTANT NOTE: Below TRANS means transformed coordinates.')

# ======================== CORDEX NA domain ========================
# CORDEX Doc: CPD (lat = 47.28, lon = 263.0 = -97)
# WRF equivalent: ref_lat = 47.28, ref_lon = -97

print('\n==============================================================================')
print('================================== CORDEX NA =================================')
print('==============================================================================')

print('\n|nu| = 47.28, |phi| = 83')

print('\n*************************** DOMAIN CENTER (CPD) **************************')

nu = 47.28; phi = 83;
lat = np.array([47.28]); lon = np.array([-97])
[latp,lonp] = nonrotated2rotated(nu,phi,lat,lon)
print('\nFrom CORDEX: lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]))
print('TRANS:       latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]),'\n')

nu = -47.28; phi = -83;
latp = np.array([0.0]); lonp = np.array([0.0])
[lat,lon] = rotated2nonrotated(nu,phi,latp,lonp)
print('ORIG:        latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('TRANS:       lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]))
print('NOTE: These 2 rows are exact reverse of the CPD first 2 rows.\n')

print('********************** Domain Top-Left Corner (TLC) **********************') 

nu = 47.28; phi = 83;
lat = np.array([59.28]); lon = np.array([189.26])
[latp,lonp] = nonrotated2rotated(nu,phi,lat,lon)
print('\nFrom CORDEX: lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]))
print('TRAN:        latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]),'\n')

nu = -47.28; phi = -83;
latp = np.array([28.36]); lonp = np.array([326.12-360])
[lat,lon] = rotated2nonrotated(nu,phi,latp,lonp)
print('From CORDEX: latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('TRANS:       lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]+360),'\n')

print('NOTE: In the above TLC values there are <= 0.38 degrees (small) errors.\n' 
'This can be due to errors in CORDEX calculations or the fact that CORDEX\n'
'may not use exactly the same values as those we use for pole location, etc.\n')  

nu = -47.28; phi = -83;
latp = np.array([28.56]); lonp = np.array([-33.94])
[lat,lon] = rotated2nonrotated(nu,phi,latp,lonp)
print('From above:  latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('TRANS:       lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]+360))
print('NOTE: These 2 rows are exact reverse of the TLC first 2 rows.\n')

print('********************** Domain Top-Right Corner (TRC) *********************') 

nu = 47.28; phi = 83;
lat = np.array([59.28]); lon = np.array([336.74])
[latp,lonp] = nonrotated2rotated(nu,phi,lat,lon)
print('\nFrom CORDEX: lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]))
print('TRAN:        latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('NOTE: These 2 rows are consistent \w the TLC first 2 rows.\n')

nu = -47.28; phi = -83;
latp = np.array([28.56]); lonp = np.array([33.94])
[lat,lon] = rotated2nonrotated(nu,phi,latp,lonp)
print('From above:  latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('TRANS:       lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]+360))
print('NOTE: These 2 rows are exact reverse of the TRC first 2 rows.\n')

print('********************** Domain Bottom-Left Corner (BLC) *********************') 

nu = 47.28; phi = 83;
lat = np.array([12.56]); lon = np.array([232.84])
[latp,lonp] = nonrotated2rotated(nu,phi,lat,lon)
print('\nFrom CORDEX: lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]))
print('TRAN:        latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('NOTE: These 2 rows are consistent \w the TLC/TRC first 2 rows.\n')

nu = -47.28; phi = -83;
latp = np.array([-28.20]); lonp = np.array([-33.81])
[lat,lon] = rotated2nonrotated(nu,phi,latp,lonp)
print('From above:  latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('TRANS:       lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]+360))
print('NOTE: These 2 rows are exact reverse of the BLC first 2 rows.\n')

print('********************** Domain Bottom-Right Corner (BRC) *********************') 

nu = 47.28; phi = 83;
lat = np.array([12.55]); lon = np.array([293.16])
[latp,lonp] = nonrotated2rotated(nu,phi,lat,lon)
print('\nFrom CORDEX: lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]))
print('TRAN:        latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('NOTE: These 2 rows are consistent \w the TLC/TRC/BLC first 2 rows.\n')

nu = -47.28; phi = -83;
latp = np.array([-28.21]); lonp = np.array([33.81])
[lat,lon] = rotated2nonrotated(nu,phi,latp,lonp)
print('From above:  latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('TRANS:       lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]+360))
print('NOTE: These 2 rows are exact reverse of the BRC first 2 rows.\n')

print('==============================================================================')
print('=========================== CORDEX NA (modified nu) ==========================')
print('==============================================================================')

print('\n|nu| = 47.5, |phi| = 83')

print('\n*************************** DOMAIN CENTER (CPD) **************************')

nu = 47.5; phi = 83;
lat = np.array([47.28]); lon = np.array([-97])
[latp,lonp] = nonrotated2rotated(nu,phi,lat,lon)
print('\nFrom CORDEX: lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]))
print('TRANS:       latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]),'\n')

nu = -47.5; phi = -83;
latp = np.array([0.0]); lonp = np.array([0.0])
[lat,lon] = rotated2nonrotated(nu,phi,latp,lonp)
print('ORIG:        latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('TRANS:       lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]))

print('\nNOTE: After changing nu, domain is not centered around local (0,0) anymore.\n')

nu = -47.5; phi = -83;
latp = np.array([-0.22]); lonp = np.array([0.0])
[lat,lon] = rotated2nonrotated(nu,phi,latp,lonp)
print('From above:  latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('TRANS:       lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]))
print('NOTE: These 2 rows are exact reverse of the CPD first 2 rows.\n')

print('********************** Domain Top-Left Corner (TLC) **********************') 

nu = 47.5; phi = 83;
lat = np.array([59.28]); lon = np.array([189.26])
[latp,lonp] = nonrotated2rotated(nu,phi,lat,lon)
print('\nFrom CORDEX: lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]))
print('TRAN:        latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]),'\n')

nu = -47.5; phi = -83;
latp = np.array([28.36]); lonp = np.array([326.12-360])
[lat,lon] = rotated2nonrotated(nu,phi,latp,lonp)
print('From CORDEX: latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('TRANS:       lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]+360),'\n')

print('NOTE: In the above TLC values there are <= 0.03 degrees errors.\n' 
'This is much better than before.\n')  

nu = -47.5; phi = -83;
latp = np.array([28.38]); lonp = np.array([-33.88])
[lat,lon] = rotated2nonrotated(nu,phi,latp,lonp)
print('From above:  latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('TRANS:       lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]+360))
print('NOTE: These 2 rows are exact reverse of the TLC first 2 rows.\n')

print('********************** Domain Top-Right Corner (TRC) *********************') 

nu = 47.5; phi = 83;
lat = np.array([59.28]); lon = np.array([336.74])
[latp,lonp] = nonrotated2rotated(nu,phi,lat,lon)
print('\nFrom CORDEX: lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]))
print('TRAN:        latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('NOTE: These 2 rows are consistent \w the TLC first 2 rows.\n')

nu = -47.5; phi = -83;
latp = np.array([28.38]); lonp = np.array([33.88])
[lat,lon] = rotated2nonrotated(nu,phi,latp,lonp)
print('From above:  latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('TRANS:       lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]+360))
print('NOTE: These 2 rows are exact reverse of the TRC first 2 rows.\n')

print('********************** Domain Bottom-Left Corner (BLC) *********************') 

nu = 47.5; phi = 83;
lat = np.array([12.56]); lon = np.array([232.84])
[latp,lonp] = nonrotated2rotated(nu,phi,lat,lon)
print('\nFrom CORDEX: lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]))
print('TRAN:        latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('NOTE: These 2 rows are consistent \w the TLC/TRC first 2 rows.\n')

nu = -47.5; phi = -83;
latp = np.array([-28.38]); lonp = np.array([-33.87])
[lat,lon] = rotated2nonrotated(nu,phi,latp,lonp)
print('From above:  latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('TRANS:       lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]+360))
print('NOTE: These 2 rows are exact reverse of the BLC first 2 rows.\n')

print('********************** Domain Bottom-Right Corner (BRC) *********************') 

nu = 47.5; phi = 83;
lat = np.array([12.55]); lon = np.array([293.16])
[latp,lonp] = nonrotated2rotated(nu,phi,lat,lon)
print('\nFrom CORDEX: lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]))
print('TRAN:        latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('NOTE: These 2 rows are consistent \w the TLC/TRC/BLC first 2 rows.\n')

nu = -47.5; phi = -83;
latp = np.array([-28.39]); lonp = np.array([33.88])
[lat,lon] = rotated2nonrotated(nu,phi,latp,lonp)
print('From above:  latp =','{:6.2f}'.format(latp[0]),', lonp =','{:6.2f}'.format(lonp[0]))
print('TRANS:       lat  =','{:6.2f}'.format(lat[0]),', lon  =','{:6.2f}'.format(lon[0]+360))
print('NOTE: These 2 rows are exact reverse of the BRC first 2 rows.\n')


