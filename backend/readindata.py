
import numpy as np
import netCDF4 as nc

###directorys home
dataloc='/home/jd/climatedata/'

fullpath=dataloc+'rr_0.50deg_reg_v14.0.nc'
rain=nc.Dataset(fullpath,'r').variables['rr'][:, :, :]
lat=nc.Dataset(fullpath,'r').variables['latitude'][:]
long=nc.Dataset(fullpath,'r').variables['longitude'][:]
time=nc.Dataset(fullpath,'r').variables['time'][:]
##onlyvalid=mndat[~mndat.mask] 
##onlyvalid
