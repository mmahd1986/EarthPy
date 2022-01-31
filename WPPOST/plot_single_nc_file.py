#!/usr/bin/env python
# coding: utf-8

# ###### Disable scrolling ######

# In[28]:


get_ipython().run_cell_magic('javascript', '', 'IPython.OutputArea.prototype._should_scroll = function(lines) {\n    return false;\n}')


# ###### Make the plot ######

# In[ ]:


# Clear variables
get_ipython().run_line_magic('reset', '-f')
# NOTE: "%reset" clears all variables. "-f" does not ask for confirmation everytime.

# Input data
file = "/scratch/p/peltier/mahdinia/WRF4.3_Verification_Runs/ERA5_RC44"+     "/wrfplev3d_d01_1979-01-01_00:00:00.nc"                                        # File containing data.
field = "T2"                                                                       # Field to plot.
time_idx_specified = 1                                                             # If time idx is specified.
time_idx = 398                                                                     # Time index value. 
cmap = 'viridis'                                                                   # Colormap. 
c_levels = 15                                                                      # Number of contour lvls.
land_edge_color = [0.55, 0.55, 0.55]                                               # States, etc border colors.   
savefile = 1                                                                       # Save plot or not.
savename = field+'_contour_plot'                                                   # Save file name.                                                             
BUD = '~/EarthPy/WPPOST/'                                                          # Backup folder address.

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
import numpy as np
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
if not os.path.exists(file):
    raise ValueError("Error: File does not exist. "
        "Check for typos or incorrect directory.")
    
# Open data file
data = Dataset(file)    

# Get field values
FD = getvar(data,field,timeidx=ALL_TIMES)

# Get cartopy projection
cart_proj = get_cartopy(FD)

# Get lats and lons
lats, lons = latlon_coords(FD)

# Land and states
land = NaturalEarthFeature(category="physical",scale="50m",name="land")
states = NaturalEarthFeature(category="cultural",scale="50m",name="admin_1_states_provinces_shp")
# NOTE: The data for this is at https://www.naturalearthdata.com/downloads/.

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

# Find the x and y of the file points
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

# Convert field data to numpy and extract specific time, if needed
FD = to_np(FD)
if time_idx_specified:
    FD = FD[time_idx,...]

# Make contour plot
lvls = np.linspace(np.min(FD),np.max(FD),c_levels)
c = plt.contourf(x,y,FD,levels=lvls,colormap=cmap)

# Add colorbar
cbar = fig.colorbar(c,ax=ax,orientation="vertical",fraction=0.016,pad=0.02)
cbar.ax.tick_params(labelsize=14)

# Data ranges
xmin = np.min(x); xmax = np.max(x)
ymin = np.min(y); ymax = np.max(y)

# Figure limits
plt.xlim((xmin,xmax)); plt.ylim((ymin,ymax))

# Figure ticks
plt.xticks(np.arange(xmin+(xmax-xmin)/16-1e-10,     xmax-(xmax-xmin)/16+1e-10,step=(xmax-xmin)/8),fontsize=14)
plt.yticks(np.arange(ymin+(ymax-ymin)/16-1e-10,     ymax-(ymax-ymin)/16+1e-10,step=(ymax-ymin)/8),fontsize=14)

# Save figure
if savefile:
    if time_idx_specified:
        plt.savefig(savename+'_tid='+str(time_idx)+'.eps', format='eps')
    else:
        plt.savefig(savename+'.eps',format='eps')
        
# Add extra display line
print("")

# Display plot
plt.show()        

