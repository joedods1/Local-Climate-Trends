from backend import DataHandle as dh
import numpy as np
from netCDF4 import Dataset as ds
from backend.varfuncs import condi_ind
from datetime import datetime
import matplotlib.pyplot as plt
from scipy import stats
datastr='tn'
lat_rng=[35, 70]
longi_rng=[-15, 15]
seasonstr='winter'
startdatestr1='1962-01-01'
enddatestr1='1970-12-31'
startdatestr2='2007-01-01'
enddatestr2='2015-12-31'
tempy1=dh.DataRequest(datastr, lat_rng, longi_rng, startdatestr1,enddatestr1, seasonstr)
tempy1.readdata()
tempy2=dh.DataRequest(datastr, lat_rng, longi_rng,  startdatestr2,enddatestr2, seasonstr)
tempy2.readdata()





processed=dh.ProcessData(tempy1,tempy2)
processed.cumdist(100)
x=processed.edges
dx=processed.edges[1]-processed.edges[0]
a=np.cumsum(processed.histoarr1,axis=0)*dx
a2=np.cumsum(processed.histoarr2,axis=0)*dx
plt.plot(x[range(1,101)], a[:,150], x[range(1,101)], a2[:,150])
plt.show()
