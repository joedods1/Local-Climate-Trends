from netCDF4 import Dataset as ds
import numpy as np
import folium
from folium.plugins import HeatMap
import os
centre=[42,0]
quantile=0.1
seasonstr='winter' # placeholders will get this info from user inputs of db
startdatestr1='1962-01-01'
startdatestr2='2007-01-01'
no_quants=1000
datastr='tn'
nedges=4000
fileloc='/home/jd/climatedata/processed/'
filename=datastr+'-'+seasonstr+'-'+startdatestr1 +'-' +startdatestr2 +'-'+'nedges'+str(nedges) + '-' + 'no_quants' +'-' +str(no_quants)+'.nc'
deltav=ds(fileloc+filename,'r').variables['deltav'].data
quant_range=ds(fileloc+filename,'r').variables['quant range'].data

lon=ds(fileloc+filename,'r').variables['longitude'].data
lat=ds(fileloc+filename,'r').variables['latitude'].data
quant_indx=np.where(quant_range==quantile)
deltav=np.reshape(deltav, (len(quant_range), len(lon)))
dataslice=deltav[quant_indx[0][0],:]
    
data=np.zeros((len(lon),3), dtype='float32')
data[:,0]=lat
data[:,1]=lon
data[:,2]=dataslice
data.tolist()
m = folium.Map([centre[0], centre[1]], tiles='stamentoner', zoom_start=6)
HeatMap(data).add_to(m)
m.save(os.path.join('/home/jd/webapps/geodjango','templates', 'Heatmap.html'))
