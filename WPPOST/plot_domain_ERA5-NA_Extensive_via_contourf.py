#!/usr/bin/env python
# coding: utf-8

# ###### Disable scrolling ######

# In[1]:


get_ipython().run_cell_magic('javascript', '', 'IPython.OutputArea.prototype._should_scroll = function(lines) {\n    return false;\n}')


# ###### Plot the domain ######

# In[26]:


# Clear variables
get_ipython().run_line_magic('reset', '-f')
# NOTE: "%reset" clears all variables. "-f" does not ask for confirmation everytime.

# Input data
geo_file =     "/scratch/p/peltier/mahdinia/WRF4.3_Verification_Runs/ERA5_RC44/geo_em.d01.nc" # Geofile name.
topo_file =     "/scratch/p/peltier/mahdinia/WRF4.3_Verification_Runs/ERA5_RC45/geo_em.d01.nc" # Overall topo file name.
ref_lon = -100.2; ref_lat = 48.0                                                   # Ref lat and lon.
c_levels = 100                                                                     # Number of color lvls.
land_edge_color = [0.55, 0.55, 0.55]                                               # States, etc border colors.   
savefiles = 1                                                                      # Save plots or not.
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
import matplotlib
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
if not os.path.exists(geo_file):
    raise ValueError("Error: Geo file does not exist. "
        "Check for typos or incorrect directory.")
if not os.path.exists(topo_file):
    raise ValueError("Error: Topo file does not exist. "
        "Check for typos or incorrect directory.")    
    
# Open geo_em and topo files
geo = Dataset(geo_file) 
topo = Dataset(topo_file) 

# Get topo heights
HGT_M_topo = getvar(topo,"HGT_M",timeidx=ALL_TIMES)

# Get domain MF values
MF = getvar(geo,"MAPFAC_M",timeidx=ALL_TIMES)

# Get domain lats and lons in np
lats, lons = latlon_coords(MF)
lats = to_np(lats)
lons = to_np(lons)

# Get topo lats and lons in np
lats_topo, lons_topo = latlon_coords(HGT_M_topo)
lons_topo = to_np(lons_topo)
lats_topo = to_np(lats_topo)

# Land, states and ocean
land = NaturalEarthFeature(category="physical",scale="50m",name="land")
states = NaturalEarthFeature(category="cultural",scale="50m",name="admin_1_states_provinces_shp")
ocean = NaturalEarthFeature(category="physical",scale="50m",name="ocean")
# NOTE: The data for this is at https://www.naturalearthdata.com/downloads/.

# Create figure
fig = plt.figure(figsize=(18,10))

# Set the axes to the projection we use
map_proj = crs.Orthographic(central_longitude=ref_lon,central_latitude=ref_lat)
map_proj._threshold /= 100.
ax = plt.axes(projection=map_proj)
# NOTE: "map_proj._threshold /= 100." is because the default value is bad and arcs become lines, 
#   so we need to set the threshold manually ("/=100." means divide by 100.0).

# Set axes to global
ax.set_global()
# NOTE: "ax.set_global()" makes the map global rather than have it zoom in to the extents of
#   any plotted data. If we do not set "ax.set_global()" an addition of a line to the globe, 
#   removes the globe. To keep drawing we need this.

# Add gridlines
gl = ax.gridlines(draw_labels=False,linewidth=2,color='k',alpha=0.5,linestyle='dotted')
gl.xlocator = matplotlib.ticker.FixedLocator(np.arange(-180,180,step=30))
gl.ylocator = matplotlib.ticker.FixedLocator(np.arange(-90,90,step=15))

# Add land, states and ocean to figure
ax.add_feature(land,linewidth=1,edgecolor=land_edge_color,facecolor="none") 
ax.add_feature(states,linewidth=1,edgecolor=land_edge_color,facecolor="none")  
ax.add_feature(ocean,linewidth=1,edgecolor="none",facecolor="blue") 

# Make appropriate colormap
cmp = matplotlib.cm.gist_earth; cmp.set_over('white'); 
colors = cmp(np.linspace(0.15,1.0,c_levels))
cmp = matplotlib.colors.LinearSegmentedColormap.from_list("mycmap", colors)
# NOTE: "matplotlib.colors.LinearSegmentedColormap" is for colormap objects based on lookup 
#   tables using linear segments. "from_list" is to create a LinearSegmentedColormap from a
#   list of colors.

# Convert HGT_M_topo to np array and convert to km
HGT_M_topo = to_np(HGT_M_topo)/1000

# Make the pcolormesh levels
levels = matplotlib.ticker.MaxNLocator(nbins=c_levels).tick_values(HGT_M_topo.min(),0.45*HGT_M_topo.max())
norm = matplotlib.colors.BoundaryNorm(levels,ncolors=cmp.N,clip=False)
# NOTE: "matplotlib.colors.BoundaryNorm" generates a colormap index based on discrete intervals.
#   Unlike Normalize or LogNorm, BoundaryNorm maps values to integers instead of to the interval 0-1.
#   In the above if clip is True, out of range values are mapped to 0 if they are below boundaries[0] 
#   or mapped to ncolors - 1 if they are above boundaries[-1]. If clip is False, out of range values are 
#   mapped to -1 if they are below boundaries[0] or mapped to ncolors if they are above boundaries[-1]. 

# Make the pcolormesh
c = plt.pcolormesh(lons_topo,lats_topo,HGT_M_topo,cmap=cmp,norm=norm,transform=crs.PlateCarree())

# Add colorbar
cbar = fig.colorbar(c,ax=ax,orientation="horizontal",fraction=0.03,pad=0.02,extend="both")
cbar.ax.tick_params(labelsize=14)
tick_locator = matplotlib.ticker.MaxNLocator(nbins=6)
cbar.locator = tick_locator
cbar.update_ticks()

# Add run domain boundaries
lons_rl = lons[:,0]
lats_rl = lats[:,0]
plt.plot(lons_rl,lats_rl,'k',linewidth=5,transform=crs.Geodetic())
lons_ru = lons[-1,:]
lats_ru = lats[-1,:]
plt.plot(lons_ru,lats_ru,'k',linewidth=5,transform=crs.Geodetic())
lons_rr = lons[:,-1]
lats_rr = lats[:,-1]
plt.plot(lons_rr,lats_rr,'k',linewidth=5,transform=crs.Geodetic())
lons_rd = lons[0,:]
lats_rd = lats[0,:]
plt.plot(lons_rd,lats_rd,'k',linewidth=5,transform=crs.Geodetic())

# Save figure
if savefiles:
    plt.savefig('domain_extended_contourf.jpeg',format='jpeg',dpi=300)        

# Add extra display line
print("")

# Display plot
plt.show()

