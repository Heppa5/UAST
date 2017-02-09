import time
import datetime
#import serial
import pynmea2
import numbers
import matplotlib.pyplot as plt
from matplotlib import dates
import numpy as np

def parse_datafile(filename):
    f = open(filename)
    if not(f.closed):
        print("File opened.")
        line = f.readline()
    else:
        print("File was NOT opened.")


    msg_list = []  
    i = 0
    while (line!= "\r\n"):
        if (line[0:6] == "$GPGGA"):
            msg = pynmea2.parse(line)
            msg_list.append(msg)
        
        line = f.readline()
        i=i+1
        if (i%1000 == 0):
            print i
    return msg_list


msg_list = parse_datafile("nmea_ublox_neo_24h_static.txt")

HDOP = []
time = []

for msg in msg_list:
    lat = msg.latitude
    lon = msg.longitude
    alt = msg.altitude
    if (isinstance(lat, numbers.Real) and isinstance(lon, numbers.Real) and isinstance(alt, numbers.Real)):
        HDOP.append(msg.horizontal_dil)
        time.append(msg.timestamp)
        
# Change datetim.time structure to datetime
# Important for matplotlib
my_day = datetime.date(2017, 2, 15)
x_dt = [ datetime.datetime.combine(my_day, t) for t in time ]

# matplotlib date format object
# format of timestamps in the x axes
hfmt = dates.DateFormatter('%H:%M')

fig, ax = plt.subplots(1,1, figsize=(10,4))

#fig = plt.figure()
#ax = fig.add_subplot(111)

# plot data
plt.plot(np.arange(len(HDOP)),HDOP)
ax.xaxis.set_major_locator(dates.MinuteLocator())
ax.xaxis.set_major_formatter(hfmt)
ax.set_xticklabels(x_dt)
ax.set_ylim(bottom = 0)

# document graph title and axes
ax.set_title('HDOP vs. Time', fontsize = 20)
ax.set_xlabel('Time [HH::MM]', fontsize = 15)
ax.set_ylabel('HDOP', fontsize = 15)
# change y axes limits
#ax.set_ylim([14,28])

# show window
plt.show()