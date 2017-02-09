import time
import datetime
#import serial
import pynmea2
import numbers
from exportkml import kmlclass


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
        if (line[0:6] == "$GPGGA"):
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


#msg_list = parse_datafile("nmea_ublox_neo_24h_static.txt")
msg_list = parse_datafile("nmea_trimble_gnss_eduquad_flight.txt")
# Create KML file
kml = kmlclass()
kml.begin("DroneTrack.kml","DroneTrack", "", 5.0)
kml.trksegbegin("Track1"," ", "blue", "absolute")

for msg in msg_list:
    lat = msg.latitude
    lon = msg.longitude
    alt = msg.altitude
    if (isinstance(lat, numbers.Real) and isinstance(lon, numbers.Real) and isinstance(alt, numbers.Real)):
        kml.trkpt(msg.latitude, msg.longitude, msg.altitude)
    
kml.trksegend()
kml.end()