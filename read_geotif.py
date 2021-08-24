#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 12:34:36 2021

@author: doan
"""

import xarray as xr
import numpy as np
import pandas as pd
import sys
import  mpl_toolkits.basemap  



# read tif file
# use xarray lib to read geotif file:
# 
tiffile = 'DEM_geotiff/alwdgg.tif'
df = xr.open_rasterio(tiffile) 

# df is xarray datatype


# Get 2-dim data that you want to regrid it
# for example here we get the first band

d = df.values[0][::-1]

# Get lat, and lon information from tiff file
lat_tif, lon_tif = df.y.values[::-1], df.x.values
# Note that lat_tif and lon_tif is 1-dim array

# Read WRF like file
dw = xr.open_dataset('wrf-like-file.nc')

# It can be whaterver, we get lat and lon information from this file
xlat, xlon = dw.XLAT.values, dw.XLONG.values
# Note that xlat, xlon are 2-dim arrays

# Now we regrid tiff to xlat, xlon frame
# Amazing!? Only by one command line
# Read more 
#https://matplotlib.org/basemap/api/basemap_api.html
#for Basemap 

d_new = mpl_toolkits.basemap.interp(d, lon_tif, lat_tif, xlon, xlat, checkbounds=False, masked=False, order=1)

# d_new is numpy array, we might want to save it as netcdf
do = xr.DataArray(d_new, 
                  name='data_new', 
                  dims=('y','x'), 
                  coords= {'lon':(('y', 'x'), xlon ), 
                           'lat':(('y', 'x'), xlat )  
                           } )
    
do.to_netcdf('data_after_regrid.nc')
    
    
    
    
    
# check how it look
# or ncview data_after_regrid.nc

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

fig = plt.figure(figsize=(5,5))

m = Basemap(projection='merc',llcrnrlat=-20,urcrnrlat=20,\
            llcrnrlon=80,urcrnrlon=125,lat_ts=20,resolution='c')
x, y = m(xlon, xlat)

m.drawcoastlines(linewidth=1.)
cs = m.contourf(x,y,d_new, levels = np.arange(-2000,2000,200), extend='both')
plt.colorbar(orientation='vertical')







    
    
    
    
    







