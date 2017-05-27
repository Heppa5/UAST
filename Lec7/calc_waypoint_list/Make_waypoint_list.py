from AQLogReader import *
from math import sqrt

from utm import * 

from export_kml import *


class calc_waypoints():
    def __init__(self,fileName):
        self.reader=aqLogReader(fileName)
        self.reader.setChannels(["GPS_LAT","GPS_LON","GPS_HEIGHT","UKF_POSN","UKF_POSE","UKF_POSD"])
        self.data=self.reader.getData()

    def calc_dist_between_point_line_NED(self,start, end, point):
        #https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
        start_x=start[4] #east is x
        start_y=start[3] # north is y
        end_x=end[4] #east is x
        end_y=end[3] # north is y
        point_x=point[4] #east is x
        point_y=point[3] # north is y
        divisor=sqrt((end_y-start_y)*(end_y-start_y)+(end_x-start_x)*(end_x-start_x))
        numerator= (end_y-start_y)*point_x - (end_x-start_x)*point_y + end_x*start_y - end_y*start_x
        error = abs(numerator)/divisor
        
        return error
    
    def calc_dist_between_point_line_gps(self, start, end, point):
        #https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
        convertToUtm=utmconv()
        start_utm=convertToUtm.geodetic_to_utm(start[0],start[1])
        start_x=start_utm[3] #east is x
        start_y=start_utm[4] # north is y
        end_utm=convertToUtm.geodetic_to_utm(end[0],end[1])
        end_x=end_utm[3] #east is x
        end_y=end_utm[4] # north is y
        point_utm=convertToUtm.geodetic_to_utm(point[0],point[1])
        point_x=point_utm[3] #east is x
        point_y=point_utm[4] # north is y
        divisor=sqrt((end_y-start_y)*(end_y-start_y)+(end_x-start_x)*(end_x-start_x))
        numerator= (end_y-start_y)*point_x - (end_x-start_x)*point_y + end_x*start_y - end_y*start_x
        error = abs(numerator)/divisor
    
        return error

    def linear_path_max_error(self, subDataList , UseGpsCoordinates):
        error = 0
        first_data_element=subDataList[0]
        last_data_element=subDataList[len(subDataList)-1]
        for x in range(1, len(subDataList)-2):
            cur_error=0
            if UseGpsCoordinates == False:
                cur_error=self.calc_dist_between_point_line_NED(first_data_element,last_data_element,subDataList[x])
            else:
                cur_error=self.calc_dist_between_point_line_gps(first_data_element,last_data_element,subDataList[x])
            if cur_error>error:
                error=cur_error
        print "Our error was: " + str(error) + " and the size of the list was: " + str(len(subDataList))
        return error
    
    def return_full_dataset(self):
        return self.data
    
    def find_waypoints(self, UseGpsCoordinates, max_error, start_offset):
        # NED data: UseGpsCoordinates==False
        # GPS data: UseGpsCoordinates==True
       
        index=0;
        end_of_list=False
        selected_waypoints=[]
        selected_waypoints.append(self.data[start_offset])
        #for i in data:
        while index < len(self.data)-1:
            if index > start_offset:  #Start offset since data is invalid at first
                numb_data_points=2
                new_data_list = self.data[index:index+numb_data_points]
                #new_data_list = data[50:index+10]
                print "Starting new iteration and index is: " + str(index)
                while (self.linear_path_max_error(new_data_list,UseGpsCoordinates) < max_error and end_of_list==False):
                    print "Retrying and index is: " + str(index) + " and numb_data_points is: " + str(numb_data_points+1)
                    if (index+numb_data_points < len(self.data)-1):
                        numb_data_points=numb_data_points+1
                        new_data_list = self.data[index:index+numb_data_points]
                    else:
                        end_of_list=True
                print "################### Done"
                selected_waypoints.append(self.data[index+numb_data_points-1]) # Minus 1 since, we have moved one step to far if we want to stay under max_error
                index=index+numb_data_points-1 # update index to be correct starting value
            else:
                index=index+1
        return selected_waypoints 
            


    
# 2568
wow=calc_waypoints("021-AQL.LOG")
selected_waypoints_NED=wow.find_waypoints(False,0.5,50)
selected_waypoints_GPS=wow.find_waypoints(True,0.5,50)
full_data=wow.return_full_dataset()


# Create KML file for NED FILTERED datapoints
kml = kmlclass()
kml.begin("DroneTrack_NED.kml","DroneTrack", "", 5.0)
kml.trksegbegin("Track1"," ", "red", "absolute")

#for msg in msg_list:
#    kml.trkpt(msg.latitude, msg.longitude, msg.altitude)
for i in selected_waypoints_NED:
    kml.trkpt(i[0],i[1],i[2])
    
kml.trksegend()
kml.end()


# Create KML file for GPS FILTERED datapoints
kml.begin("DroneTrack_GPS.kml","DroneTrack", "", 5.0)
kml.trksegbegin("Track1"," ", "red", "absolute")

#for msg in msg_list:
#    kml.trkpt(msg.latitude, msg.longitude, msg.altitude)
for i in selected_waypoints_GPS:
    kml.trkpt(i[0],i[1],i[2])
    
kml.trksegend()
kml.end()

# Create KML file for FULL drone track
kml.begin("DroneTrack_full.kml","DroneTrack", "", 5.0)
kml.trksegbegin("Track1"," ", "red", "absolute")

#for msg in msg_list:
#    kml.trkpt(msg.latitude, msg.longitude, msg.altitude)
for i in full_data:
    kml.trkpt(i[0],i[1],i[2])
    
kml.trksegend()
kml.end()


