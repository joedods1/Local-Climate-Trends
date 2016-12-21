#data request class handels the data from initiation to passing to the
#data processing modules



class DataRequest:
    def __init__(self, datastr, lat_rng, longi_rng, datestr):   #define the various parameters,
                                                                #wether want rain fall data, 'rr',
                                                                #temp, 'tn', 'tq'
        self.datastr = datastr
        self.lat_rng = lat_rng
        self.longi_rng = longi_rng
        self.datestr = datestr
        self.dataloc='/home/jd/climatedata/'                    # place holder
        
    def readdata(self):
        from netCDF4 import Dataset as ds
        from backend import varfuncs as vf
        fullpath=self.dataloc+self.datastr+'_0.50deg_reg_1950-1964_v14.0.nc'
        # add relavent varibles to structure
        self.lat=ds(fullpath,'r').variables['latitude'][:]
        self.longi=ds(fullpath,'r').variables['longitude'][:]
        (self.lat_index, lat_reduced) = vf.condi_ind(self.lat, self.lat_rng)          #reduce the data to geographic regions of relavence
        (self.longi_index, longi_reduced) = vf.condi_ind(self.longi, self.longi_rng)
        self.time=ds(fullpath,'r').variables['time']
        self.full=ds(fullpath,'r')
        
        
#        (begdateuse,fmt)=format_datestr(self.time.units) # get teh date of teh first data entry    
 #       dt = datetime.strptime(begdateuse, fmt).timetuple() 
        self.jdstart=vf.conv2jd(self.time.units) #convert the dates into jullian day 
        
        self.vari=ds(fullpath,'r').variables[self.datastr][:,self.lat_index,self.longi_index] #reduce teh main data matrix
    
        


#       self.vari=ds(fullpath,'r').variables['rr'][~ds(fullpath,'r').variables[self.datestr].mask]
#       self.time=ds(fullpath,'r').variables['time'][~ds(fullpath,'r').variables['time'].mask]
