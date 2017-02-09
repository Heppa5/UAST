import time
import datetime
import serial
import pynmea2
import matplotlib.pyplot as plt
from matplotlib import dates


def read(filename):
    f = open(filename)
    if not(f.closed):
        print("File opened.")
        line = f.readline()
    else:
        print("File was NOT opened.")

    while (line!= "\r\n"):
        #print(line)
        #line = line[:-1]
        #print(line)
        msg = pynmea2.parse(line)
        print(msg)
        #print(msg.timestamp)
        #print(msg.latitude)
        #print(msg.longitude)
        #raw_input("Press Enter to continue...")
        line = f.readline()

def parse_datafile(filename):
    f = open(filename)
    if not(f.closed):
        print("File opened.")
        line = f.readline()
    else:
        print("File was NOT opened.")


    msg_list = []    
    while (line!= "\r\n"):
        msg = pynmea2.parse(line)
        msg_list.append(msg)
        line = f.readline()
        
    return msg_list

def get_times(msg_list):
    # Create list with data
    timestamps = []
    # Iterate over message fields and save corresponding data to a new list
    for msg in msg_list:
        timestamps.append(msg.timestamp)
        
    return timestamps

def get_altitudes(msg_list):
    # Create list with data
    altitudes = []
    # Iterate over message fields and save corresponding data to a new list
    for msg in msg_list:
        altitudes.append(msg.altitude)
        
    return altitudes

def get_satNos(msg_list):
    # Create list with data
    satNos = []
    # Iterate over message fields and save corresponding data to a new list
    for msg in msg_list:
        satNos.append(msg.num_sats)
        
    return satNos


msg_list = parse_datafile("nmea_trimble_gnss_eduquad_flight.txt")

time = get_times(msg_list)
altitude = get_altitudes(msg_list)
satNo = get_satNos(msg_list)

# Change datetim.time structure to datetime
# Important for matplotlib
my_day = datetime.date(2017, 2, 15)
x_dt = [ datetime.datetime.combine(my_day, t) for t in time ]
# Plotting --------------------------------------    
# matplotlib date format object
# format of timestamps in the x axes
hfmt = dates.DateFormatter('%H:%M')

fig = plt.figure()
ax = fig.add_subplot(111)

# plot data
plt.plot(x_dt,altitude)
#plt.gcf().autofmt_xdate()

ax.xaxis.set_major_locator(dates.MinuteLocator())
ax.xaxis.set_major_formatter(hfmt)
ax.set_ylim(bottom = 0)

# document graph title and axes
ax.set_title('Altitude vs. Time', fontsize = 20)
ax.set_xlabel('Time [HH::MM]', fontsize = 15)
ax.set_ylabel('Altitude [m]', fontsize = 15)
# change y axes limits
ax.set_ylim([14,28])

# show window
plt.show()


# Plotting --------------------------------------    
# matplotlib date format object
# format of timestamps in the x axes
hfmt = dates.DateFormatter('%H:%M')

fig = plt.figure()
ax = fig.add_subplot(111)

# plot data
plt.plot(x_dt,satNo)
#plt.gcf().autofmt_xdate()

ax.xaxis.set_major_locator(dates.MinuteLocator())
ax.xaxis.set_major_formatter(hfmt)
ax.set_ylim(bottom = 0)

# document graph title and axes
ax.set_title('Satelites No vs. Time', fontsize = 20)
ax.set_xlabel('Time [HH::MM]', fontsize = 15)
ax.set_ylabel('Satelites No.', fontsize = 15)
# change y axes limits
ax.set_ylim([5,15])

# show window
plt.show()

# Two subplots, the axes array is 1-d
f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot(x_dt,altitude)
axarr[0].xaxis.set_major_locator(dates.MinuteLocator())
axarr[0].xaxis.set_major_formatter(hfmt)
axarr[0].set_ylim(bottom = 0)

# document graph title and axes
axarr[0].set_title('Altitude vs. Time', fontsize = 20)
axarr[0].set_xlabel('Time [HH::MM]', fontsize = 15)
axarr[0].set_ylabel('Altitude [m]', fontsize = 15)
# change y axes limits
axarr[0].set_ylim([14,28])

axarr[1].plot(x_dt,satNo)
ax.xaxis.set_major_locator(dates.MinuteLocator())
ax.xaxis.set_major_formatter(hfmt)
ax.set_ylim(bottom = 0)

# document graph title and axes
axarr[1].set_title('Satelites No vs. Time', fontsize = 20)
axarr[1].set_ylabel('Satelites No.', fontsize = 15)
# change y axes limits
axarr[1].set_ylim([5,15])
plt.show()