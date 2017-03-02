from backend import DataHandle as dh
import numpy as np
from netCDF4 import Dataset as ds
from backend.varfuncs import condi_ind
from datetime import datetime
import matplotlib.pyplot as plt
from scipy import stats
datastr='tn'
lat_rng=[35, 70]
longi_rng=[-15, 40]
seasonstr='winter'
startdatestr1='1962-01-01'
enddatestr1='1970-12-31'
startdatestr2='2007-01-01'
enddatestr2='2015-12-31'


tempy1=dh.DataRequest(datastr, lat_rng, longi_rng, startdatestr1,enddatestr1, seasonstr)
tempy1.readdata()
tempy2=dh.DataRequest(datastr, lat_rng, longi_rng,  startdatestr2,enddatestr2, seasonstr)
tempy2.readdata()



nedges=40
no_quants=10
processed=dh.ProcessData(tempy1,tempy2)
processed.cumdist(nedges)
x=processed.edges
dx=processed.edges[1]-processed.edges[0]
a=np.cumsum(processed.histoarr1,axis=0)*dx
a2=np.cumsum(processed.histoarr2,axis=0)*dx
processed.getquantilediffs(no_quants=no_quants)
processed.savequantilediffs()
processed.shapefile_grid()
##plt.plot(processed.edges, processed.cumsum1[:,0] ,processed.edges, processed.cumsum2[:,0])
##plt.show()
##plt.plot(processed.quant_range, processed.deltav[:,100])
##plt.show()

self=processed

