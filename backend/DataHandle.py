#data request class handels the data from initiation to passing to the
#data processing modules
from netCDF4 import Dataset as ds
from backend import varfuncs as vf
from jdcal import jd2gcal
import numpy as np
from datetime import datetime
from scipy import stats
from geojson import Polygon, Feature, FeatureCollection
import json
import shapefile

class DataRequest:
    def __init__(self, datastr, lat_rng, longi_rng, startdatestr, enddatestr, seasonstr):   #define the various parameters,
                                                                #wether want rain fall data, 'rr',
        self.seasonstr=seasonstr                                                        #temp, 'tn', 'tq'
        self.datastr = datastr
        self.lat_rng = lat_rng
        self.longi_rng = longi_rng
        self.startdatestr = startdatestr
        self.enddatestr = enddatestr
        self.dataloc='/home/jd/climatedata/'                    # where you store your datafiles
    def getdatearrays(self):
        (self.jdstart, self.jdstarttup)=vf.conv2jd(self.time.units) #convert the dates into jullian day       
        self.jd_array=np.array(range(0, self.time.size-1,1)) + self.jdstart       
        self.doy=np.zeros(self.jd_array.size)                        # convert jd (julian day) into DOY (day of year)        
        for idx, x in enumerate(self.jd_array):            
            tuppy = jd2gcal(self.jdstarttup[0], x - self.jdstarttup[0])    ##getting the DOY and create an array with same index as jd_array
            b=datetime(tuppy[0], tuppy[1], tuppy[2]).timetuple
            self.doy[idx]=datetime(tuppy[0], tuppy[1], tuppy[2]).timetuple().tm_yday
            
    def seasonreduction(self):
        seasons=['summer', 'winter', 'spring', 'autumn']
        alllimits=[[152, 243], [335, 59], [60, 151], [244, 334]] # define the various DOY  limits [start, stop]
        if self.seasonstr==seasons[0]:
            limits=alllimits[0]
        elif self.seasonstr==seasons[1]:                            ## bunch of conditionals to determine the season
            limits=alllimits[1]
        elif self.seasonstr==seasons[2]:
            limits=alllimits[2]
        elif self.seasonstr==seasons[3]:
            limits=alllimits[3]
        self.seasonarrreduce(limits)  
    def seasonarrreduce(self, limits):        
        ##determine the how conditions going to be applied
        if limits[0]<limits[1]:
            mask = (self.doy >= limits[0])*(self.doy <=  limits[1])     ## numpy mask is just a logical array/ boolian 
        else:
            mask= (self.doy <= limits[0]) + (self.doy >=  limits[1])      ##apply the appropraite conditions
        self.seasonmask=mask
    def timereduction(self):                                                       ## this fucntion obtians the mask needed to only read in teh appropriate data
        self.getdatearrays()
        self.seasonreduction()
        (self.jddatestart, self.jddatestarttup)=vf.conv2jd(self.startdatestr)
        (self.jddateend, self.jddateendtup)=vf.conv2jd(self.enddatestr)
        subsetmask=(self.jd_array>=self.jddatestart)*(self.jd_array<=self.jddateend)    ##mask teh region of interest ie. the 9 years specify when first calling class
        self.timemask=self.seasonmask*subsetmask
        self.timemasklist=np.where(self.timemask==True)[0].tolist()
        
    def readdata(self):
        fullpath=self.dataloc+self.datastr+'_0.50deg_reg_v14.0.nc'
        # add relavent varibles to structure
        self.lat=ds(fullpath,'r').variables['latitude'][:]
        self.longi=ds(fullpath,'r').variables['longitude'][:]
        
        (self.lat_index, self.lat_reduced) = vf.condi_ind(self.lat, self.lat_rng)          #reduce the data to geographic regions of relavence
        (self.longi_index, self.longi_reduced) = vf.condi_ind(self.longi, self.longi_rng)
        
        self.time=ds(fullpath,'r').variables['time']
        self.full=ds(fullpath,'r')
        
        self.timereduction()
             
        self.vari=ds(fullpath,'r').variables[self.datastr][self.timemasklist,self.lat_index,self.longi_index] #reduce the main data matrix
        self.vari_data=self.vari.data[~self.vari.mask] #remove the mask just data array
    
        
        
        
class ProcessData(DataRequest):
    def __init__(self, DataRequest_1, DataRequest_2):
        self.DataRequest_1=DataRequest_1
        self.DataRequest_2=DataRequest_2
        
    def cumdist(self,nedges):
        self.minmaxvals=[min(self.DataRequest_1.vari_data.min(), self.DataRequest_2.vari_data.min()), max(self.DataRequest_1.vari_data.max(), self.DataRequest_2.vari_data.max())]        
        vari_size=self.DataRequest_1.vari.shape

        ## select for regions in which both data sets  have a sufficient number of data entries (here >400) 
        self.looptup=np.where(((~self.DataRequest_1.vari.mask).sum(axis=0)>400)*((~self.DataRequest_1.vari.mask).sum(axis=0)>400)==True)
        self.nedges=nedges       
        
        
        self.histoarr1=np.zeros((nedges+1, len(self.looptup[0])))
        self.histoarr2=np.zeros((nedges+1, len(self.looptup[0])))

        self.cumsum1=np.zeros((nedges+1, len(self.looptup[0])))
        self.cumsum2=np.zeros((nedges+1, len(self.looptup[0])))
        ## get the edge array I am being lazy here generating it from histofram function is unnessary
        hist2, edges = np.histogram(self.DataRequest_2.vari.data[:,self.looptup[0][0],self.looptup[1][0]], range=(float(self.minmaxvals[0]),  float(self.minmaxvals[1])), bins=nedges, normed=True)
        dx=edges[1]-edges[0]
        self.edges=edges
        for indx in range(len(self.looptup[0])):
            
            data1=self.DataRequest_1.vari.data[~self.DataRequest_1.vari.mask[:,self.looptup[0][indx],self.looptup[1][indx]],self.looptup[0][indx],self.looptup[1][indx]]
            data2=self.DataRequest_2.vari.data[~self.DataRequest_2.vari.mask[:,self.looptup[0][indx],self.looptup[1][indx]],self.looptup[0][indx],self.looptup[1][indx]]

            indx_arr1=np.where(((edges>= data1.min())*(edges<= data1.max())))[0] ## idenitify what part of edge array is actually needed
            indx_arr2=np.where(((edges>= data2.min())*(edges<= data2.max())))[0]          
                
            edgesuse1 = self.edges[indx_arr1]
            edgesuse2 = self.edges[indx_arr2]
            
            hist1=stats.gaussian_kde(data1)                                     ## obtain kernel density estimates to get smooth pdfs
            hist2=stats.gaussian_kde(data2)
            
            self.histoarr1[indx_arr1,indx]=hist1.pdf(edgesuse1)                 ## dump pdfs into large array
            self.histoarr2[indx_arr2,indx]=hist2.pdf(edgesuse2)
            
        self.cumsum1=np.cumsum(self.histoarr1, axis=0)*dx   ## get the cummalative distribution
        self.cumsum2=np.cumsum(self.histoarr2, axis=0)*dx
    def getquantilediffs(self,**ops):
        if 'no_quants' in ops:
            no_quants=ops['no_quants']
        else:
            no_quants=100
        self.no_quants=no_quants
        dx=self.edges[1]-self.edges[0]
        
        
        self.deltav=np.zeros((no_quants, np.shape(self.cumsum1)[1]))
        self.quant_range=np.arange(0, 1, 1/no_quants)
        for indx, quant in enumerate(self.quant_range):
            temp_arr1=abs(self.cumsum1 - quant)## generate array to be used to identify index of value closest to quant
            temp_arr2=abs(self.cumsum2 - quant)
            indx_t1=np.argmin(temp_arr1,axis=0)
            indx_t2=np.argmin(temp_arr2,axis=0)
            self.deltav[indx,:]=(indx_t2-indx_t1)*dx       ## this array contains the variable changes at a given quantile dx is there to convert index difference to temperature differences

    def constructfilename(self):
        filename=self.DataRequest_1.datastr+'-'+self.DataRequest_1.seasonstr+'-'+self.DataRequest_1.startdatestr +'-' +self.DataRequest_2.startdatestr +'-'+'nedges'+str(self.nedges) + '-' + 'no_quants' +'-' +str(self.no_quants)
        return filename
    
    def savequantilediffs(self, **ops):
        if 'fileloc' in ops:
            fileloc=ops['fileloc']
        else:
            fileloc='/home/jd/webapps/geodjango2/world/data/'
        ## filename for save file
        filename=self.constructfilename()
        self.filename=filename
        self.fileloc=fileloc
        data=ds(fileloc+filename+'.nc', 'w',format='NETCDF4_CLASSIC') 
        lat=data.createDimension('lat', np.shape(self.deltav)[1])
        lon=data.createDimension('lon', np.shape(self.deltav)[1])
        quantr=data.createDimension('quantr',np.shape(self.deltav)[0])
        lat=data.createVariable('latitude', np.float32, ('lat',))
        lon=data.createVariable('longitude', np.float32, ('lon',))
        quant_range=data.createVariable('quant range',np.float32, ('quantr',))
        deltav=data.createVariable('deltav', np.float32, ('quantr','lat'))
        
        lat_vals=self.looptup[0]*abs(self.DataRequest_1.lat[1]-self.DataRequest_1.lat[0]) +min(self.DataRequest_1.lat_reduced)
        lon_vals=self.looptup[1]*abs(self.DataRequest_1.longi[1]-self.DataRequest_1.longi[0]) +min(self.DataRequest_1.longi_reduced)
        self.lat_vals=lat_vals
        self.lon_vals=lon_vals
 #       self.geojson_grid()
        data.variables['latitude'].data=lat_vals
        data.variables['longitude'].data=lon_vals
        data.variables['quant range'].data=self.quant_range
        data.variables['deltav'].data=self.deltav
        data.close()
    def geojson_grid(self):
        allfeat=[];
        latdev=self.DataRequest_1.lat[1]-self.DataRequest_1.lat[0]
        longdev=self.DataRequest_1.longi[1]-self.DataRequest_1.longi[0]
        for indx, x  in enumerate(self.lon_vals):
            y=self.lat_vals[indx]
            tempfeat=Feature(id= indx, geometry=Polygon(([(x-longdev/2, y-latdev/2), (x-longdev/2, y+latdev/2), (x+longdev/2, y+latdev/2), (x+longdev/2, y-latdev/2)],)))
            allfeat.append(tempfeat)

        collection=FeatureCollection(allfeat)
        self.collection=collection
        with open(self.fileloc + self.filename+'.json', 'w') as outfile:
            json.dump(collection, outfile)
    def shapefile_grid(self):
        allfeat=[];
        latdev=self.DataRequest_1.lat[1]-self.DataRequest_1.lat[0]
        longdev=self.DataRequest_1.longi[1]-self.DataRequest_1.longi[0]
        w= shapefile.Writer(shapefile.POLYGON)
        w.field("grid_id", 'N')
        w.field('name','C')
        w.field("LAT",'N')
        w.field("LON",'N')
        for indx, x  in enumerate(self.lon_vals):
            y=self.lat_vals[indx]
            w.poly(parts=[[[x-longdev/2, y-latdev/2], [x-longdev/2, y+latdev/2], [x+longdev/2, y+latdev/2], [x+longdev/2, y-latdev/2]]])
        for indx, x  in enumerate(self.lon_vals):
            w.record(grid_id=indx, LAT=self.lat_vals[indx],LON=x,name=str(indx))
        w.save(self.fileloc + self.filename)
            
                
            
            
    
