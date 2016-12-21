from backend.DataRequest import DataRequest

import numpy as np
from netCDF4 import Dataset as ds
from backend.varfuncs import condi_ind


datastr='rr'
lat_rng=[35, 70]
longi_rng=[-15, 15]
datestr=''

tempy=DataRequest(datastr, lat_rng, longi_rng, datestr)
tempy.readdata()
