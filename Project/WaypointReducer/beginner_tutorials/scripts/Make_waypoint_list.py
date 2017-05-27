#!/usr/bin/env python
from AQLogReader import *
from math import sqrt

from utm import * 
import rospy
import numpy as np

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
        # NED data
        if (UseGpsCoordinates==False):
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
                    while (self.linear_path_max_error(new_data_list,False) < max_error and end_of_list==False):
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

        # GPS data 
        else:
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
                    while (self.linear_path_max_error(new_data_list,True) < max_error and end_of_list==False):
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
            
    def ChooseBestWaypoints(self):
		#get fewer waypoints
	waypointNiko = 0
	
	thresshold = 0.0000020
	counterNiko = 0
	numberOfWaypointsNiko = 25 
	
	while (waypointNiko < numberOfWaypointsNiko):
		waypointNiko = 0
		del newWaypointsNikoLat[:]
		del newWaypointsNikoLong[:]
		del newWaypointsNikoAlt [:]
		for i in range(1,len(selected_waypoints_NED)-1):
			if i == 0: 
				waypointNiko = waypointNiko + 1
				newWaypointsNikoLat.append(newVarNiLat)
				newWaypointsNikoLong.append(newVarNiLong)
				newWaypointsNikoAlt.append(selected_waypoints_NED[i][2])
	
			newVarNiLat = selected_waypoints_NED[i][0]
			varNewNiLat = selected_waypoints_NED[i+1][0]
			
			varNikoLat = newVarNiLat - varNewNiLat
	
			newVarNiLong = selected_waypoints_NED[i][1]
			varNewNiLong = selected_waypoints_NED[i+1][1]
			
			varNikoLong = newVarNiLong - varNewNiLong
			#dist = sqrt((x1-x0)**2 + (y1-y0)**2 + (z1-z0))
			if (abs(varNikoLat) < thresshold) & (abs(varNikoLong) < thresshold):
				waypointNiko = waypointNiko + 1
				newWaypointsNikoLat.append(newVarNiLat)
				newWaypointsNikoLong.append(newVarNiLong)
				newWaypointsNikoAlt.append(selected_waypoints_NED[i][2])
				
			counterNiko = counterNiko + 1 
			
		thresshold = thresshold + 0.0000005
		print "hej: "
		print thresshold
		print waypointNiko



    def ChooseBestWaypointsNi(self):
		#get fewer waypoints
	waypointNiko = 0
	
	thresshold = 5.0
	counterNiko = 0
	numberOfWaypointsNiko = 24 
	print "ChooseBestNI: "
	while (waypointNiko < numberOfWaypointsNiko):
		waypointNiko = 0
		del newWaypointsNikoLat[:]
		del newWaypointsNikoLong[:]
		del newWaypointsNikoAlt [:]
		for i in range(1,len(selected_waypoints_NED)-2):
			if i == 0: 
				waypointNiko = waypointNiko + 1
				newWaypointsNikoLat.append(newVarNiLat)
				newWaypointsNikoLong.append(newVarNiLong)
				newWaypointsNikoAlt.append(selected_waypoints_NED[i][2])
			distNi = 0			
			#print "find points: "
			x0 = selected_waypoints_NED[i][0]
			x1 = selected_waypoints_NED[i+1][0]
			x2 = selected_waypoints_NED[i+2][0]			

			y0 = selected_waypoints_NED[i][1]
			y1 = selected_waypoints_NED[i+1][1]
			y2 = selected_waypoints_NED[i+2][1]

			z0 = selected_waypoints_NED[i][2]  # current point
			z1 = selected_waypoints_NED[i+1][2]  # next point
			z2 = selected_waypoints_NED[i+2][2]
		
			distNiFirst = sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0) + (z1-z0)*(z1-z0))
			distNiSecond = sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) + (z2-z1)*(z2-z1))
			
			if (distNiFirst > thresshold and distNiSecond > thresshold and waypointNiko < numberOfWaypointsNiko ):
				waypointNiko = waypointNiko + 1
				newWaypointsNikoLat.append(x1)
				newWaypointsNikoLong.append(y1)
				newWaypointsNikoAlt.append(z1)
				
			counterNiko = counterNiko + 1 
			
		thresshold = thresshold - 0.0001
		
		print "hej: "
		print thresshold		
		print distNi
		print waypointNiko
	waypointNiko = waypointNiko + 1
	lastx = len(selected_waypoints_NED)-1
	print lastx
	#print len(selected_waypoints_NED
	newWaypointsNikoLat.append(selected_waypoints_NED[lastx][0])
	newWaypointsNikoLong.append(selected_waypoints_NED[lastx][1])
	newWaypointsNikoAlt.append(selected_waypoints_NED[lastx][2])
	print "Finish : "
	print waypointNiko

    def ChooseBestWaypointsNiko(self):
		#get fewer waypoints
	waypointNiko = 0
	
	thresshold = 10.0
	counterNiko = 0
	numberOfWaypointsNiko = 24 
	print "ChooseBestNI: "
	while (waypointNiko < numberOfWaypointsNiko):
		waypointNiko = 0
		del newWaypointsNikoLat[:]
		del newWaypointsNikoLong[:]
		del newWaypointsNikoAlt [:]
		for i in range(1,len(selected_waypoints_NED)-1):
			if i == 0: 
				waypointNiko = waypointNiko + 1
				newWaypointsNikoLat.append(newVarNiLat)
				newWaypointsNikoLong.append(newVarNiLong)
				newWaypointsNikoAlt.append(selected_waypoints_NED[i][2])
			distNi = 0			
			#print "find points: "
			x0 = selected_waypoints_NED[i][0]
			x1 = selected_waypoints_NED[i+1][0]
			
			y0 = selected_waypoints_NED[i][1]
			y1 = selected_waypoints_NED[i+1][1]

			z0 = selected_waypoints_NED[i][2]  # current point
			z1 = selected_waypoints_NED[i+1][2]  # next point
			
			distNi = sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0) + (z1-z0)*(z1-z0))
			
			if (distNi > thresshold ):
				waypointNiko = waypointNiko + 1
				newWaypointsNikoLat.append(x0)
				newWaypointsNikoLong.append(y0)
				newWaypointsNikoAlt.append(z0)
				
			counterNiko = counterNiko + 1 
			
		thresshold = thresshold - 0.0001
		
		print "hej: "
		print thresshold		
		print distNi
		print waypointNiko

	waypointNiko = waypointNiko + 1
	lastx = len(selected_waypoints_NED)-1
	print lastx
	#print len(selected_waypoints_NED
	newWaypointsNikoLat.append(selected_waypoints_NED[lastx][0])
	newWaypointsNikoLong.append(selected_waypoints_NED[lastx][1])
	newWaypointsNikoAlt.append(selected_waypoints_NED[lastx][2])
	print "Finish : "
	
    def ChooseBestWaypointsNiNi(self):
		#get fewer waypoints
	waypointNiko = 0
	
	thresshold = 5 #1.7
	counterNiko = 0
	LowestValue = 0
	distarray = []
	latDistarray = []
	longDistarray = []
	altDistarray = []
	latArray = []
	longArray = []
	altArray = []
	numberOfWaypointsNiko = 23 
	print "ChooseBestNI: "

	for j in range(1,len(selected_waypoints_NED)-1):
		x0 = selected_waypoints_NED[j][0]
		x1 = selected_waypoints_NED[j+1][0]

		y0 = selected_waypoints_NED[j][1]
		y1 = selected_waypoints_NED[j+1][1]

		z0 = selected_waypoints_NED[j][2]  # current point
		z1 = selected_waypoints_NED[j+1][2]  # next point

		dist = sqrt((x1-x0)*(x1-x0) + (y1-y0)*(y1-y0) + (z1-z0)*(z1-z0))
		#print dist
		distarray.append(dist)
		latDistarray.append(abs(x0-x1))
		longDistarray.append(abs(y0-y1))
		altDistarray.append(abs(z0-z1))
		latArray.append(x0)
		longArray.append(y0)
		altArray.append(z0)



	while (waypointNiko < numberOfWaypointsNiko ):#or waypointNiko <numberOfWaypointsNiko-5):
		waypointNiko = 0
		del newWaypointsNikoLat[:]
		del newWaypointsNikoLong[:]
		del newWaypointsNikoAlt [:]
		for i in range(1,len(selected_waypoints_NED)-3):
			
			if i == 0: 
				waypointNiko = waypointNiko + 1
				newWaypointsNikoLat.append(newVarNiLat)
				newWaypointsNikoLong.append(newVarNiLong)
				newWaypointsNikoAlt.append(selected_waypoints_NED[i][2])
			x = latArray[i]  # den siger index out of range for tal over 1
			
			y = longArray[i]
			z = altArray[i]
			x1 = latArray[i+1]  # den siger index out of range for tal over 1
			
			y1 = longArray[i+1]
			z1 = altArray[i+1]
			distNi = distarray[i]
			distNext = distarray[i+1]
			distNextNext = [i+2]

			# find de 25 stoerste afstande. 
			#if(distNi > distNext ):
			if (distNi > thresshold): # find the 25 biggest distances
				#latArray.pop(6)			
				waypointNiko = waypointNiko + 1
				newWaypointsNikoLat.append(x)
				newWaypointsNikoLong.append(y)
				newWaypointsNikoAlt.append(z)
				newWaypointsNikoLat.append(x1)
				newWaypointsNikoLong.append(y1)
				newWaypointsNikoAlt.append(z1)
				print distNi
				print waypointNiko
					#print distNi
			
			
		thresshold = thresshold - 0.0001  # lower limit distance
		
		print "hej: "
		print thresshold		
		#print distNi
		print waypointNiko
	waypointNiko = waypointNiko + 1
	lastx = len(selected_waypoints_NED)-1
	print lastx
	#print len(selected_waypoints_NED
	newWaypointsNikoLat.append(selected_waypoints_NED[lastx][0])
	newWaypointsNikoLong.append(selected_waypoints_NED[lastx][1])
	newWaypointsNikoAlt.append(selected_waypoints_NED[lastx][2])
	print "Finish : "
	print waypointNiko
    
# 2568
wow=calc_waypoints("021-AQL.LOG")
selected_waypoints_NED=wow.find_waypoints(False,0.5,50)
selected_waypoints_GPS=wow.find_waypoints(True,0.5,50)
full_data=wow.return_full_dataset()


newWaypointsNikoLat = []
newWaypointsNikoLong = []
newWaypointsNikoAlt = []
 
wow.ChooseBestWaypointsNiNi()   


# Create KML file
kml = kmlclass()
kml.begin("/home/robo/catkin_ws/src/beginner_tutorials/scripts/DroneTrack_NED.kml","DroneTrack", "", 5.0)
kml.trksegbegin("Track1"," ", "red", "absolute")

#for msg in msg_list:
#    kml.trkpt(msg.latitude, msg.longitude, msg.altitude)
for i in selected_waypoints_NED:
    kml.trkpt(i[0],i[1],i[2])
    
kml.trksegend()
kml.end()


# Create KML file
kml.begin("/home/robo/catkin_ws/src/beginner_tutorials/scripts/DroneTrack_GPS.kml","DroneTrack", "", 5.0)
kml.trksegbegin("Track1"," ", "red", "absolute")

#for msg in msg_list:
#    kml.trkpt(msg.latitude, msg.longitude, msg.altitude)
for i in selected_waypoints_GPS:
    kml.trkpt(i[0],i[1],i[2])
    #print "hej: "
    
kml.trksegend()
kml.end()

# Create KML file
kml.begin("/home/robo/catkin_ws/src/beginner_tutorials/scripts/DroneTrack_full.kml","DroneTrack", "", 5.0)
kml.trksegbegin("Track1"," ", "red", "absolute")

#for msg in msg_list:
#    kml.trkpt(msg.latitude, msg.longitude, msg.altitude)
for i in full_data:
    kml.trkpt(i[0],i[1],i[2])
    
kml.trksegend()
kml.end()

# Create KML file
kml.begin("/home/robo/catkin_ws/src/beginner_tutorials/scripts/DroneTrack_NEDDDiNiko.kml","DroneNiTrack", "", 5.0)
kml.trksegbegin("Track1"," ", "red", "absolute")

#for msg in msg_list:
    #kml.trkpt(msg.latitude, msg.longitude, msg.altitude)
for i in range(0,len(newWaypointsNikoLat)):

    kml.trkpt(newWaypointsNikoLat[i],newWaypointsNikoLong[i],newWaypointsNikoAlt[i])
    
kml.trksegend()
kml.end()


