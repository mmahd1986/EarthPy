#!/usr/bin/env python
# coding: utf-8

# ###### Disable scrolling ######

# In[ ]:


get_ipython().run_cell_magic('javascript', '', 'IPython.OutputArea.prototype._should_scroll = function(lines) {\n    return false;\n}')


# ###### Plot the domain ######

# In[3]:


# Clear variables
get_ipython().run_line_magic('reset', '-f')
# NOTE: "%reset" clears all variables. "-f" does not ask for confirmation everytime.

# Input data
geo_file =     "/scratch/p/peltier/mahdinia/WRF4.3_Verification_Runs/ERA5_RC44/geo_em.d01.nc" # Geofile name.
JON_domain_file = '/project/p/peltier/mahdinia/Post_Processing/jons_domian.nc'     # JON's domain file.
CORDEX_domain_file =     '/scratch/p/peltier/mahdinia/WRF4.3_Verification_Runs/ERA5_RC26/geo_em.d01.nc' # CORDEX domain's file.
dd = [-199.2,-0.8,-0.3,87.0]                                                       # Download domains extents.
ref_lon = -100.2; ref_lat = 48.0                                                   # WRF ref_lon and ref_lat.
range_f_ur = 2.55                                                                  # Plot range factor (unrot).
tick_f_ur = 1.0455                                                                 # Tick range factor (unrot).
range_f_rx = 1.3                                                                   # Plot range factor (rot x).
range_f_ry = 1.05                                                                  # Plot range factor (rot y).
cmap = 'viridis'                                                                   # Colormap. 
c_levels = 15                                                                      # Number of contour lvls.
land_edge_color = [0.55, 0.55, 0.55]                                               # states, etc border colors.   
BUD = '~/EarthPy/WPPOST/'                                                          # Backup folder address.

# Add EarthPy src to sys.path, if needed
import sys
if not('/home/p/peltier/mahdinia/EarthPy/src/' in sys.path):
    sys.path.append('/home/p/peltier/mahdinia/EarthPy/src/')

# Save notebook back-up as .py file in the Earthpy
import ipyparams
nb_name = ipyparams.notebook_name
om = get_ipython().getoutput('jupyter nbconvert {nb_name} --to python --output-dir={BUD}')
    
# Turn off annoying warnings
import warnings
warnings.filterwarnings('ignore')

# Make sure the environment is good 
import os
import cartopy
import matplotlib
import numpy as np
from latlonrotation import transformcoordinates
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature 
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from wrf import (getvar, interplevel, vertcross, 
                 CoordPair, ALL_TIMES, to_np,
                 get_cartopy, latlon_coords,
                 cartopy_xlim, cartopy_ylim,
                 Constants,extract_vars)

# Check that the files exist
if not os.path.exists(geo_file):
    raise ValueError("Error: Geo file does not exist. "
        "Check for typos or incorrect directory.")
if not os.path.exists(JON_domain_file):
    raise ValueError("Error: Jon's domain file does not exist. "
        "Check for typos or incorrect directory.")    
if not os.path.exists(CORDEX_domain_file):
    raise ValueError("Error: CORDEX's domain file does not exist. "
        "Check for typos or incorrect directory.") 
    
# Open geo_em files
geo = Dataset(geo_file)    

# Get mapfactors
MF = getvar(geo,"MAPFAC_M",timeidx=ALL_TIMES)

# Get cartopy projection
cart_proj = get_cartopy(MF)

# Get lats and lons
lats, lons = latlon_coords(MF)

# Land and states
land = NaturalEarthFeature(category="physical",scale="50m",name="land")
states = NaturalEarthFeature(category="cultural",scale="50m",name="admin_1_states_provinces_shp")
# NOTE: The data for this is at https://www.naturalearthdata.com/downloads/.

# ====================================================================================
# ================================== Rotated domain ==================================
# ====================================================================================

# Create figure
fig = plt.figure(figsize=(18,10))

# Set the axes to the projection we use
ax = plt.axes(projection=cart_proj)

# Add land and states to figure
ax.add_feature(land,linewidth=1,edgecolor=land_edge_color,facecolor="none") 
ax.add_feature(states,linewidth=1,edgecolor=land_edge_color,facecolor="none") 

# Create a globe
wrf_globe = crs.Globe(ellipse=None,
    semimajor_axis=Constants.WRF_EARTH_RADIUS,
    semiminor_axis=Constants.WRF_EARTH_RADIUS)
# NOTE: crs.Globe defines an ellipsoid and, optionally, how to relate it
# to the real world. 'ellipse=None' assumes a sphere. See here for more info:
# https://scitools.org.uk/cartopy/docs/latest/crs/index.html#cartopy.crs.Globe.

# Create a spherical topology coordinate system
wrf_xform_crs = crs.Geodetic(globe=wrf_globe)
# NOTE: crs.Geodetic defines a latitude/longitude coordinate system with
# spherical topology; geographical distance and coordinates are measured
# in degrees. See here for more info:
# https://scitools.org.uk/cartopy/docs/latest/crs/index.html.

# Find the x and y of the geo file points
xform_pts = cart_proj.transform_points(wrf_xform_crs,to_np(lons),to_np(lats))
x = xform_pts[...,0]
y = xform_pts[...,1]
# NOTE: transform_points(src_crs, x, y) transforms the given coordinates,
# in the given source coordinate system (src_crs), to this coordinate system.
# In more detail, lons and lats are given in the geographical
# coordinates; wrf_xform_crs is geographical coordinates; and cart_proj is the
# rotated lat-lon projection we used in wrf. This transforms the lons
# and lats in geographical coordiantes (wrf_xform_crs) to rotated lat-lon
# coordinates (cart_proj).

# Make contour plot
lvls = np.linspace(np.min(to_np(MF)),np.max(to_np(MF)),c_levels)
c = plt.contourf(x,y,to_np(MF),levels=lvls,colormap=cmap)

# Add colorbar
cbar = fig.colorbar(c,ax=ax,orientation="vertical",fraction=0.016,     pad=0.02,ticks=np.arange(1+1e-5,1.22,0.029))
cbar.ax.tick_params(labelsize=14)

# Figure limits
xmin = range_f_ur*np.min(x); xmax = range_f_ur*np.max(x)
ymin = range_f_ur*np.min(y); ymax = range_f_ur*np.max(y)
plt.xlim((xmin,xmax)); plt.ylim((ymin,ymax))

# Adjust figure further
ax.set_title('Rotated Coordiantes',fontsize=18,pad=10)
xmin_t = xmin*tick_f_ur; xmax_t = xmax*tick_f_ur;
ymin_t = ymin*tick_f_ur; ymax_t = ymax*tick_f_ur;
plt.xticks(np.arange(xmin_t+(xmax_t-xmin_t)/16-1e-10,     xmax_t-(xmax_t-xmin_t)/16+1e-10,step=(xmax_t-xmin_t)/8),fontsize=14)
plt.yticks(np.arange(ymin_t+(ymax_t-ymin_t)/16-1e-10,     ymax_t-(ymax_t-ymin_t)/16+1e-10,step=(ymax_t-ymin_t)/8),fontsize=14)

# Add download domain boundaries
nu = ref_lat; phi = 180+ref_lon
lat_dl = np.linspace(dd[2],dd[3],100)
lon_dl = np.full((100, 1),dd[0])
[y_dl,x_dl] = transformcoordinates.nonrotated2rotated(nu,phi,lat_dl,lon_dl)
plt.plot(x_dl,y_dl,'b',linewidth=5)
lat_dr = np.linspace(dd[2],dd[3],100)
lon_dr = np.full((100, 1),dd[1])
[y_dr,x_dr] = transformcoordinates.nonrotated2rotated(nu,phi,lat_dr,lon_dr)
plt.plot(x_dr,y_dr,'b',linewidth=5)
lat_du = np.full((100, 1),dd[3])
lon_du = np.linspace(dd[0],dd[1],100)
[y_du,x_du] = transformcoordinates.nonrotated2rotated(nu,phi,lat_du,lon_du)
plt.plot(x_du,y_du,'b',linewidth=5)
lat_dd = np.full((100, 1),dd[2])
lon_dd = np.linspace(dd[0],dd[1],100)
[y_dd,x_dd] = transformcoordinates.nonrotated2rotated(nu,phi,lat_dd,lon_dd)
plt.plot(x_dd,y_dd,'b',linewidth=5)

# Add run domain boundaries
x_rl = np.min(x); x_rr = np.max(x);
y_rd = np.min(y); y_ru = np.max(y);
x_rl_a = np.full((100, 1),x_rl)
y_rl_a = np.linspace(y_rd,y_ru,100)
plt.plot(x_rl_a,y_rl_a,'b',linewidth=3)
x_rr_a = np.full((100, 1),x_rr)
y_rr_a = np.linspace(y_rd,y_ru,100)
plt.plot(x_rr_a,y_rr_a,'b',linewidth=3)
x_ru_a = np.linspace(x_rl,x_rr,100)
y_ru_a = np.full((100, 1),y_ru)
plt.plot(x_ru_a,y_ru_a,'b',linewidth=3)
x_rd_a = np.linspace(x_rl,x_rr,100)
y_rd_a = np.full((100, 1),y_rd)
plt.plot(x_rd_a,y_rd_a,'b',linewidth=3)

# Add forcing boundaries
x_rl = np.min(x)-2; x_rr = np.max(x)+2;
y_rd = np.min(y)-2; y_ru = np.max(y)+2;
x_rl_a = np.full((100, 1),x_rl)
y_rl_a = np.linspace(y_rd,y_ru,100)
plt.plot(x_rl_a,y_rl_a,'b--',linewidth=3)
x_rr_a = np.full((100, 1),x_rr)
y_rr_a = np.linspace(y_rd,y_ru,100)
plt.plot(x_rr_a,y_rr_a,'b--',linewidth=3)
x_ru_a = np.linspace(x_rl,x_rr,100)
y_ru_a = np.full((100, 1),y_ru)
plt.plot(x_ru_a,y_ru_a,'b--',linewidth=3)
x_rd_a = np.linspace(x_rl,x_rr,100)
y_rd_a = np.full((100, 1),y_rd)
plt.plot(x_rd_a,y_rd_a,'b--',linewidth=3)
x_rl = np.min(x)+2; x_rr = np.max(x)-2;
y_rd = np.min(y)+2; y_ru = np.max(y)-2;
x_rl_a = np.full((100, 1),x_rl)
y_rl_a = np.linspace(y_rd,y_ru,100)
plt.plot(x_rl_a,y_rl_a,'b--',linewidth=3)
x_rr_a = np.full((100, 1),x_rr)
y_rr_a = np.linspace(y_rd,y_ru,100)
plt.plot(x_rr_a,y_rr_a,'b--',linewidth=3)
x_ru_a = np.linspace(x_rl,x_rr,100)
y_ru_a = np.full((100, 1),y_ru)
plt.plot(x_ru_a,y_ru_a,'b--',linewidth=3)
x_rd_a = np.linspace(x_rl,x_rr,100)
y_rd_a = np.full((100, 1),y_rd)
plt.plot(x_rd_a,y_rd_a,'b--',linewidth=3)

# Plot CORDEX domain
geo_CORDEX = Dataset(CORDEX_domain_file)    
MF_CORDEX = getvar(geo_CORDEX,"MAPFAC_M",timeidx=ALL_TIMES)
lats_CORDEX, lons_CORDEX = latlon_coords(MF_CORDEX)
xform_pts_CORDEX = cart_proj.transform_points(wrf_xform_crs,to_np(lons_CORDEX),to_np(lats_CORDEX))
x_CORDEX = xform_pts_CORDEX[...,0]
y_CORDEX = xform_pts_CORDEX[...,1]
[M,N] = x_CORDEX.shape
x_cl = x_CORDEX[:,0]; y_cl = y_CORDEX[:,0];
plt.plot(x_cl,y_cl,'k',linewidth=1)
x_cr = x_CORDEX[:,N-1]; y_cr = y_CORDEX[:,N-1];
plt.plot(x_cr,y_cr,'k',linewidth=1)
x_cd = x_CORDEX[0,:]; y_cd = y_CORDEX[0,:];
plt.plot(x_cd,y_cd,'k',linewidth=1)
x_cu = x_CORDEX[M-1,:]; y_cu = y_CORDEX[M-1,:];
plt.plot(x_cu,y_cu,'k',linewidth=1)

# Plot Jon's domain
geo_JON = Dataset(JON_domain_file)    
MF_JON = getvar(geo_JON,"MAPFAC_M",timeidx=ALL_TIMES)
lats_JON, lons_JON = latlon_coords(MF_JON)
xform_pts_JON = cart_proj.transform_points(wrf_xform_crs,to_np(lons_JON),to_np(lats_JON))
x_JON = xform_pts_JON[...,0]
y_JON = xform_pts_JON[...,1]
[M,N] = x_JON.shape
x_jl = x_JON[:,0]; y_jl = y_JON[:,0];
plt.plot(x_jl,y_jl,'k-.',linewidth=3)
x_jr = x_JON[:,N-1]; y_jr = y_JON[:,N-1];
plt.plot(x_jr,y_jr,'k-.',linewidth=3)
x_jd = x_JON[0,:]; y_jd = y_JON[0,:];
plt.plot(x_jd,y_jd,'k-.',linewidth=3)
x_ju = x_JON[M-1,:]; y_ju = y_JON[M-1,:];
plt.plot(x_ju,y_ju,'k-.',linewidth=3)

# Add extra display line
print("")

# Display plot
plt.show()

# ====================================================================================
# ================================ Un-Rotated domain =================================
# ====================================================================================

# Create figure
fig = plt.figure(figsize=(18,10))

# Set the axes to the projection we use
ax = plt.axes(projection=crs.PlateCarree(central_longitude=ref_lon))

# Add land and states to figure
ax.add_feature(land,linewidth=1,edgecolor=land_edge_color,facecolor="none") 
ax.add_feature(states,linewidth=1,edgecolor=land_edge_color,facecolor="none") 

# Adjust lons
lons = to_np(lons)
lons[lons>0] = lons[lons>0]-360
lons = lons-ref_lon

# Make contour plot
c = plt.contourf(lons,lats,to_np(MF),levels=lvls,colormap=cmap)

# Add colorbar
cbar = fig.colorbar(c,ax=ax,orientation="vertical",fraction=0.016,     pad=0.02,ticks=np.arange(1+1e-5,1.22,0.029))
cbar.ax.tick_params(labelsize=14)

# Add figure title
ax.set_title('Geographical Coordiantes',fontsize=18,pad=10)

# Add download domain
plt.plot(lon_dl-ref_lon,lat_dl,'b',linewidth=5)
plt.plot(lon_dr-ref_lon,lat_dr,'b',linewidth=5)
plt.plot(lon_dd-ref_lon,lat_dd,'b',linewidth=5)
plt.plot(lon_du-ref_lon,lat_du,'b',linewidth=5)

# Add run domain boundaries
phi = -(180+ref_lon); nu = -ref_lat
x_rl = np.min(x); x_rr = np.max(x);
y_rd = np.min(y); y_ru = np.max(y);
x_rl_a = np.full((100, 1),x_rl)
y_rl_a = np.linspace(y_rd,y_ru,100)
[lat_rl,lon_rl] = transformcoordinates.rotated2nonrotated(nu,phi,y_rl_a,x_rl_a)
plt.plot(lon_rl-ref_lon,lat_rl,'b',linewidth=3)
x_rr_a = np.full((100, 1),x_rr)
y_rr_a = np.linspace(y_rd,y_ru,100)
[lat_rr,lon_rr] = transformcoordinates.rotated2nonrotated(nu,phi,y_rr_a,x_rr_a)
plt.plot(lon_rr-ref_lon,lat_rr,'b',linewidth=3)
x_ru_a = np.linspace(x_rl,x_rr,100)
y_ru_a = np.full((100, 1),y_ru)
[lat_ru,lon_ru] = transformcoordinates.rotated2nonrotated(nu,phi,y_ru_a,x_ru_a)
plt.plot(lon_ru-ref_lon,lat_ru,'b',linewidth=3)
x_rd_a = np.linspace(x_rl,x_rr,100)
y_rd_a = np.full((100, 1),y_rd)
[lat_rd,lon_rd] = transformcoordinates.rotated2nonrotated(nu,phi,y_rd_a,x_rd_a)
plt.plot(lon_rd-ref_lon,lat_rd,'b',linewidth=3)

# Add forcing boundaries
x_rl = np.min(x)-2; x_rr = np.max(x)+2;
y_rd = np.min(y)-2; y_ru = np.max(y)+2;
x_rl_a = np.full((100, 1),x_rl)
y_rl_a = np.linspace(y_rd,y_ru,100)
[lat_rl,lon_rl] = transformcoordinates.rotated2nonrotated(nu,phi,y_rl_a,x_rl_a)
plt.plot(lon_rl-ref_lon,lat_rl,'b--',linewidth=3)
x_rr_a = np.full((100, 1),x_rr)
y_rr_a = np.linspace(y_rd,y_ru,100)
[lat_rr,lon_rr] = transformcoordinates.rotated2nonrotated(nu,phi,y_rr_a,x_rr_a)
plt.plot(lon_rr-ref_lon,lat_rr,'b--',linewidth=3)
x_ru_a = np.linspace(x_rl,x_rr,100)
y_ru_a = np.full((100, 1),y_ru)
[lat_ru,lon_ru] = transformcoordinates.rotated2nonrotated(nu,phi,y_ru_a,x_ru_a)
plt.plot(lon_ru-ref_lon,lat_ru,'b--',linewidth=3)
x_rd_a = np.linspace(x_rl,x_rr,100)
y_rd_a = np.full((100, 1),y_rd)
[lat_rd,lon_rd] = transformcoordinates.rotated2nonrotated(nu,phi,y_rd_a,x_rd_a)
plt.plot(lon_rd-ref_lon,lat_rd,'b--',linewidth=3)
x_rl = np.min(x)+2; x_rr = np.max(x)-2;
y_rd = np.min(y)+2; y_ru = np.max(y)-2;
x_rl_a = np.full((100, 1),x_rl)
y_rl_a = np.linspace(y_rd,y_ru,100)
[lat_rl,lon_rl] = transformcoordinates.rotated2nonrotated(nu,phi,y_rl_a,x_rl_a)
plt.plot(lon_rl-ref_lon,lat_rl,'b--',linewidth=3)
x_rr_a = np.full((100, 1),x_rr)
y_rr_a = np.linspace(y_rd,y_ru,100)
[lat_rr,lon_rr] = transformcoordinates.rotated2nonrotated(nu,phi,y_rr_a,x_rr_a)
plt.plot(lon_rr-ref_lon,lat_rr,'b--',linewidth=3)
x_ru_a = np.linspace(x_rl,x_rr,100)
y_ru_a = np.full((100, 1),y_ru)
[lat_ru,lon_ru] = transformcoordinates.rotated2nonrotated(nu,phi,y_ru_a,x_ru_a)
plt.plot(lon_ru-ref_lon,lat_ru,'b--',linewidth=3)
x_rd_a = np.linspace(x_rl,x_rr,100)
y_rd_a = np.full((100, 1),y_rd)
[lat_rd,lon_rd] = transformcoordinates.rotated2nonrotated(nu,phi,y_rd_a,x_rd_a)
plt.plot(lon_rd-ref_lon,lat_rd,'b--',linewidth=3)

# Plot CORDEX domain
[M,N] = lons_CORDEX.shape
lon_cl = lons_CORDEX[:,0]; lat_cl = lats_CORDEX[:,0];
lon_cl[lon_cl>0] = lon_cl[lon_cl>0]-360
plt.plot(lon_cl-ref_lon,lat_cl,'k',linewidth=1)
lon_cr = lons_CORDEX[:,N-1]; lat_cr = lats_CORDEX[:,N-1];
lon_cr[lon_cr>0] = lon_cr[lon_cr>0]-360
plt.plot(lon_cr-ref_lon,lat_cr,'k',linewidth=1)
lon_cd = lons_CORDEX[0,:]; lat_cd = lats_CORDEX[0,:];
lon_cd[lon_cd>0] = lon_cd[lon_cd>0]-360
plt.plot(lon_cd-ref_lon,lat_cd,'k',linewidth=1)
lon_cu = lons_CORDEX[M-1,:]; lat_cu = lats_CORDEX[M-1,:];
lon_cu[lon_cu>0] = lon_cu[lon_cu>0]-360
plt.plot(lon_cu-ref_lon,lat_cu,'k',linewidth=1)

# Plot Jon's domain
[M,N] = lons_JON.shape
lon_jl = lons_JON[:,0]; lat_jl = lats_JON[:,0];
lon_jl[lon_jl>0] = lon_jl[lon_jl>0]-360
plt.plot(lon_jl-ref_lon,lat_jl,'k-.',linewidth=3)
lon_jr = lons_JON[:,N-1]; lat_jr = lats_JON[:,N-1];
lon_jr[lon_jr>0] = lon_jr[lon_jr>0]-360
plt.plot(lon_jr-ref_lon,lat_jr,'k-.',linewidth=3)
lon_jd = lons_JON[0,:]; lat_jd = lats_JON[0,:];
lon_jd[lon_jd>0] = lon_jd[lon_jd>0]-360
plt.plot(lon_jd-ref_lon,lat_jd,'k-.',linewidth=3)
lon_ju = lons_JON[M-1,:]; lat_ju = lats_JON[M-1,:];
lon_ju[lon_ju>0] = lon_ju[lon_ju>0]-360
plt.plot(lon_ju-ref_lon,lat_ju,'k-.',linewidth=3)

# Figure limits
xmin_l = range_f_rx*np.min(lons); xmax_l = range_f_rx*np.max(lons)
ymin_l = (dd[3]+dd[2])/2-range_f_ry*(dd[3]-dd[2])/2 
ymax_l = (dd[3]+dd[2])/2+range_f_ry*(dd[3]-dd[2])/2
plt.xlim((xmin_l,xmax_l)); plt.ylim((ymin_l,ymax_l))

# Figure labels
xmin_t = dd[0]-ref_lon; xmax_t = dd[1]-ref_lon;
xticks = np.arange(xmin_t-1e-10,xmax_t+1e-10,step=(xmax_t-xmin_t)/5)
ax.set_xticks(xticks)
ax.set_xticklabels(f"{t:.2f}" for t in (xticks+ref_lon))
ymin_t = dd[2]; ymax_t = dd[3];
yticks = np.arange(ymin_t-1e-10,ymax_t+1e-10,step=(ymax_t-ymin_t)/5)
ax.set_yticks(yticks)
ax.set_yticklabels(f"{t:.2f}" for t in (yticks))
ax.tick_params(axis='both',which='major',labelsize=16)

# Display plot
plt.show()

