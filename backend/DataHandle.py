#data request class handels the data from initiation to passing to the
#data processing modules
from netCDF4 import Dataset as ds
from backend import varfuncs as vf
from jdcal import jd2gcal
import numpy as np
from datetime import datetime

class DataRequest:
    def __init__(self, datastr, lat_rng, longi_rng, datestr, seasonstr):   #define the various parameters,
                                                                #wether want rain fall data, 'rr',
        self.seasonstr=seasonstr                                                        #temp, 'tn', 'tq'
        self.datastr = datastr
        self.lat_rng = lat_rng
        self.longi_rng = longi_rng
        self.datestr = datestr
        self.dataloc='/home/jd/climatedata/'                    # place holder
    def getdatearrays(self):
        (self.jdstart, self.jdstarttup)=vf.conv2jd(self.time.units) #convert the dates into jullian day       
        self.jd_array=np.array(range(0, self.time.size-1,1)) + self.jdstart    # gnerate jd array as     
        self.doy=np.zeros(self.jd_array.size)                        # convert jd into DOY        
        for idx, x in enumerate(self.jd_array):            
            tuppy = jd2gcal(self.jdstarttup[0], x - self.jdstarttup[0])    ##getting the DOY and create an array with same index as jd_array
            b=datetime(tuppy[0], tuppy[1], tuppy[2]).timetuple
            self.doy[idx]=datetime(tuppy[0], tuppy[1], tuppy[2]).timetuple().tm_yday
            
    def seasonreduction(self):
        seasons=['summer', 'winter', 'spring', 'autumn']
        alllimits=[[152, 243], [335, 59], [60, 151], [244, 334]] # define the various DOY  limits [start, stop]
        if self.seasonstr==seasons[0]:
            limits=alllimits[0]
        elif self.seasonstr==seasons[1]:
            limits=alllimits[1]
        elif self.seasonstr==seasons[2]:
            limits=alllimits[2]
        elif self.seasonstr==seasons[3]:
            limits=alllimits[3]
        self.seasonarrreduce(limits)  
    def seasonarrreduce(self, limits):        
        ##determine the how conditions going to be applied
        if limits[0]<limits[1]:
            mask = (self.doy >= limits[0])*(self.doy <=  limits[1])
        else:
            mask= (self.doy <= limits[0]) + (self.doy >=  limits[1])      ##apply the appropraite conditions
        self.doy=np.ma.array(self.doy, mask=mask)
        
    def readdata(self):
        fullpath=self.dataloc+self.datastr+'_0.50deg_reg_1950-1964_v14.0.nc'
        # add relavent varibles to structure
        self.lat=ds(fullpath,'r').variables['latitude'][:]
        self.longi=ds(fullpath,'r').variables['longitude'][:]
        
        (self.lat_index, lat_reduced) = vf.condi_ind(self.lat, self.lat_rng)          #reduce the data to geographic regions of relavence
        (self.longi_index, longi_reduced) = vf.condi_ind(self.longi, self.longi_rng)
        
        self.time=ds(fullpath,'r').variables['time']
        self.full=ds(fullpath,'r')
        
        self.getdatearrays()
        self.seasonreduction()
        
##        (self.jdstart, self.jdstarttup)=vf.conv2jd(self.time.units) #convert the dates into jullian day
##        
##        self.jd_array=np.array(range(0, self.time.size-1,1)) + self.jdstart        
##        self.doy=np.zeros(self.jd_array.size)                        # convert jd into DOY
##
##            
        self.vari=ds(fullpath,'r').variables[self.datastr][:,self.lat_index,self.longi_index] #reduce the main data matrix
        self.vari=self.vari.data[~self.vari.mask] #remove the mask just data array
    
        
        
        
class ProcessData(DataRequest):
    def __init__(self, DataRequest_1, DataRequest_2):
        self.DataRequest_1=DataRequest_1
        self.DataRequest_2=DataRequest_2
##    def sanitycheck(self):
##        ##this fucntion checks the ranges for the data, makes sure the data is of teh same type ie rainfull, temp etc aswell as other things might include later on
##        if self.DataRequest_1.datastr == self.DataRequest_1.datastr:
##            datatypes=('rr', 'tn', 'tq')
##            
##            if datatypes[0] == self.DataRequest_1.datastr
##
##            elif
##
##            
##            ## acceptable ranges
##            
##            ##check shit
##            
##                
##        else
##            print('Trying to compare the distributions of different data')
##            return False
    
        
    def cumdist(self,nedges):
        self.minmaxvals=[min(self.DataRequest_1.vari.min(), self.DataRequest_2.vari.min()), max(self.DataRequest_1.vari.max(), self.DataRequest_2.vari.max())]        
        hist1, edges = np.histogram(self.DataRequest_1.vari, range=(self.minmaxvals[0],  self.minmaxvals[1]), bins=nedges, density=True)
        self.cumsum1=np.cumsum(hist1)
        
        hist2, edges = np.histogram(self.DataRequest_2.vari, range=(self.minmaxvals[0],  self.minmaxvals[1]), bins=nedges, density=True)
        self.cumsum2=np.cumsum(hist2)
        
        self.edges=edges
        
##        if sanitycheck(self.DataRequest_1.datastr, minmaxvals):
##           self.edgearr=
            

            
##        devisions
        
        #things that need to be considered, what are the limits of the data, how many bins do we want,
        #do we want the cdf to be fitted with analytical function thereby reducing the amount of data stored 
        #
        




        
