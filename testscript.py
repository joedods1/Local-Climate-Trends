from backend import DataHandle as dh
import numpy as np
from netCDF4 import Dataset as ds
from backend.varfuncs import condi_ind
from datetime import datetime

datastr='rr'
lat_rng=[35, 70]
longi_rng=[-15, 15]
seasonstr='summer'
datestr1='1950-01-01'
datestr2='2000-01-01'
tempy1=dh.DataRequest(datastr, lat_rng, longi_rng, datestr1, seasonstr)
tempy1.readdata()
tempy2=dh.DataRequest(datastr, lat_rng, longi_rng, datestr2, seasonstr)
tempy2.readdata()
a=dh.ProcessData(tempy1,tempy2)

