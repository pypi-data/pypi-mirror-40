# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 13:08:28 2019

@author: MichaelEK
"""
import numpy as np
import pandas as pd
import xarray as xr
from hydrointerp.interp2d import interp_to_grid, interp_to_points
from hydrointerp.io.raster import save_geotiff
from hydrointerp.util import grp_ts_agg

#########################################
### Parameters

nc1 = 'nasa_gpm_2018-01-17.nc'
tif1 = 'nasa_gpm_2018-01-17.tif'

time_name = 'time'
x_name = 'lon'
y_name = 'lat'
data_name = 'precipitationCal'
from_crs = 4326
to_crs = 2193
grid_res = 1000
bbox=None
order=1
extrapolation='constant'
cval=np.nan
digits = 2
min_lat = -48
max_lat = -41
min_lon = 170
max_lon = 178
min_val=0
method='linear'

########################################
### Read data

ds = xr.open_dataset(nc1)
ds.close()

### Aggregate data
da4 = ds[data_name].resample(time='D', closed='right', label='left').sum('time')

### Save as tif
df5 = da4.to_dataframe().reset_index()

save_geotiff(df5, 4326, 'precipitationCal', 'lon', 'lat', export_path=tif1)

########################################
### Run interpolations














