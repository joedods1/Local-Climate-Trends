from datetime import datetime

#converts a string containing the date for the first entry of netcdf4 ebos data (and anything else under certain constraints)
# want to reduce the messy ebos datestr to one able to be handled by datetime functions, should work for most common date formats as long as : is not used to seperate yyyy:mm:dd also no other numbers unrealed to date in string
# function outputs the reduced string
# also fails at american (aka retarded) dates mm/dd/yyyy
def format_datestr(datestr):
    
    numbers="0123456789"
    strlen=len(datestr)
    i=0
    count=0
    prevno=0
    prevdelim=0
    pdelimstr=''
    yeardef=0                      
    p=-1                          
    struse=''
    pdelim=''
    while p < strlen:            #first go through datstr to identify if a number or not
        print(p)    
        p+=1
        if datestr[p]==numbers[0] or datestr[p]==numbers[1] or datestr[p]==numbers[2]\
        or datestr[p]==numbers[3] or datestr[p]==numbers[4] or datestr[p]==numbers[5]\
        or datestr[p]==numbers[6] or datestr[p]==numbers[7] or datestr[p]==numbers[8] or datestr[p]==numbers[9]:
        
            struse+=datestr[p]        #if number add to reduced string 
            prevno=1 
            count+=1                  # count to see if groups of numbers are years or not
            print('count='+str(count))
            print('struse=' + struse)
        else:
            if prevno==1:
                delim=datestr[p]   # in non-number branch but since last entry was number this must be a delimiter
                print('pdelim='+pdelim)
                print('delim='+delim)
                if delim==":":     # a : delimiter is almost exclusive to times of day hh:mm  therfore want to skip ahead and overwrite struse
                    struse=''
                    p+=2
                    
                else:     
                    struse+=delim
                    i+=1
                    
                if count==4:
                    yst=p-count
                    yeardef=1      # identify if its a year
                           
                
                if  pdelim==delim:
                    if yeardef==1:
                        print('op1='+struse)
                        struse=struse + datestr[p+1:p+3] 
                        fmt='%Y'+delim+'%m'+ delim + '%d'   #if a year has been identified aswell as a repeated delim tehn format must be as shown
                        break
                    else:
                        print('op2='+struse)
                        struse=struse + datestr[p+1:p+5]
                        fmt='%d'+delim+'%m'+delim+'%Y'   #if a year hasnt been then
                        break                            #Reset count
                pdelim=delim
                count=0
                
            prevno=0                                     
            print('in else p=' + str(p))   

                
    return (struse, fmt)
