
import matplotlib.pyplot as plt


from datetime import datetime

def read_get_time(filename):
    f=open(filename)
    lines=f.readlines()
    result=[]
    for x in lines:
        result.append(x.split('\t')[4])
    f.close
    
    return result

def read_get_voltage(filename):
    f=open(filename)
    lines=f.readlines()
    result=[]
    for x in lines:
        result.append(x.split('\t')[11])
    f.close
    
    return result



time=read_get_time("log-2016-01-14.txt")
voltage=read_get_voltage("log-2016-01-14.txt")

#time2=[datetime.strptime(x, '%hr%min%sec') for x in time]
time2=[datetime.strptime(x, '%H%M%S.%f') for x in time]
plt.plot(time2,voltage)
#plt.plot(voltage,time2)
plt.show()





#time = get_times(msg_list)
#altitude = get_altitudes(msg_list)
#satNo = get_satNos(msg_list)

## Change datetim.time structure to datetime
## Important for matplotlib
#my_day = datetime.date(2017, 2, 15)
#x_dt = [ datetime.datetime.combine(my_day, t) for t in time ]
## Plotting --------------------------------------    
## matplotlib date format object
## format of timestamps in the x axes
#hfmt = dates.DateFormatter('%H:%M')

#fig = plt.figure()
#ax = fig.add_subplot(111)

## plot data
#plt.plot(x_dt,altitude)
##plt.gcf().autofmt_xdate()

#ax.xaxis.set_major_locator(dates.MinuteLocator())
#ax.xaxis.set_major_formatter(hfmt)
#ax.set_ylim(bottom = 0)

## document graph title and axes
#ax.set_title('Altitude vs. Time', fontsize = 20)
#ax.set_xlabel('Time [HH::MM]', fontsize = 15)
#ax.set_ylabel('Altitude [m]', fontsize = 15)
## change y axes limits
#ax.set_ylim([14,28])

## show window
#plt.show()