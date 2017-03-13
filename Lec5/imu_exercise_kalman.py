#!/usr/bin/python
# -*- coding: utf-8 -*-

# IMU exercise
# Copyright (c) 2015-2017 Kjeld Jensen kjen@mmmi.sdu.dk kj@kjen.dk

# import libraries
from math import pi, sqrt, atan2
import matplotlib.pyplot as plt
from pylab import ion
from imu_box3d import imu_visualize
import time

# name of the file to read ##
fileName = 'imu_razor_data_pitch_45deg.txt'

## IMU type
#imuType = 'vectornav_vn100'
imuType = 'sparkfun_razor'

# other parameters
showPlot = True
show3DLiveView = False
show3DLiveViewInterval = 3

##### Insert initialize code below ###################

# approx. bias values determined by averaging over static measurements
bias_gyro_x = 0.0 # [rad/measurement]
bias_gyro_y = 0.0 # [rad/measurement]
bias_gyro_z = 0.0 # [rad/measurement]

# variances
# jesper has inserted values
#gyroVar = 0.1 # page 7 in ISG-3200 datasheet: 0.1 degree/s/g 
#pitchVar = 0.2 #could not find it in datasheet - random for now
# Put in something low for gyro and something high for acc. 
gyroVar = 0.5
pitchVar = 2

# Kalman filter start guess
# setting in something high to see kalman filter converge
#estAngle = -pi/4.0
#estVar =  pi

estAngle = 5
estVar = 15

# Kalman filter housekeeping variables
# it is our accumulated variance - initialized to zero by Jesper - try to do without this
#gyroVarAcc = 0.0

#Added last time sted variables - Jesper
estAngle_pre=estAngle
estVar_pre=estVar 

old_angle=0;

######################################################

## Variables for plotting ##
plotDataGyro = []
plotDataAcc = []
plotDataKalman = []

## Initialize your variables here ##
gyro_x_rel = 0.0
gyro_y_rel = 0.0
gyro_z_rel = 0.0

# open the imu data file
f = open (fileName, "r")

# initialize variables
count = 0

# initialize 3D liveview
if show3DLiveView == True:
	imuview = imu_visualize()
	imuview.set_axis (0, 0, 0)
	imuview.update()

# looping through file
for line in f:
	count += 1

	# split the line into CSV formatted data
	line = line.replace ('*',',') # make the checkum another csv value
	csv = line.split(',')

	# keep track of the timestamps 
	ts_recv = float(csv[0])
	if count == 1: 
		ts_now = ts_recv # only the first time
 	ts_prev = ts_now
	ts_now = ts_recv

	if imuType == 'sparkfun_razor': 
		# import data from a SparkFun Razor IMU (SDU firmware)
		# outputs ENU reference system
		acc_x = int(csv[2]) / 1000.0 * 4 * 9.82;
		acc_y = int(csv[3]) / 1000.0 * 4 * 9.82;
		acc_z = int(csv[4]) / 1000.0 * 4 * 9.82;
		gyro_x = int(csv[5]) * 1/14.375 * pi/180.0;
		gyro_y = int(csv[6]) * 1/14.375 * pi/180.0;
		gyro_z = int(csv[7]) * 1/14.375 * pi/180.0;

	elif imuType == 'vectornav_vn100': 
		# import data from a VectorNav VN-100 configured to output $VNQMR
		# outputs NED reference system (therefore converted to ENU)
		acc_y = float(csv[9])
		acc_x = float(csv[10])
		acc_z = -float(csv[11])
		gyro_y = float(csv[12])
		gyro_x = float(csv[13])
		gyro_z = -float(csv[14])

	# subtract defined static bias for each gyro		
	gyro_x -= bias_gyro_x
	gyro_y -= bias_gyro_y
	gyro_z -= bias_gyro_z

	##### Insert loop code below #########################

	# Variables available
	# ----------------------------------------------------
	# count		Current number of updates		
	# ts_prev	Time stamp at the previous update
	# ts_now	Time stamp at this update
	# acc_x		Acceleration measured along the x axis
	# acc_y		Acceleration measured along the y axis
	# acc_z		Acceleration measured along the z axis
	# gyro_x	Angular velocity measured about the x axis
	# gyro_y	Angular velocity measured about the y axis
	# gyro_z	Angular velocity measured about the z axis

	## Insert your code here ##

        #WE DO NOT NEED TO USE ALL HIS VARIABLES - IMPORTANT
        
	# calculate pitch (x-axis) and roll (y-axis) angles
	# equation 28 from exercise 4.1.1 - jesper
	pitch = atan2(acc_y,sqrt(acc_x*acc_x+acc_z*acc_z)) 
	# Formula from 4.1.2 - jesper 
	roll = atan2(-acc_x,acc_z)

	# integrate gyro velocities to releative angles
	
	# From Petr
	dt = ts_now - ts_prev


	gyro_x_rel += dt*gyro_x   
	gyro_y_rel += dt*gyro_y
	gyro_z_rel += dt*gyro_z

	#### Kalman prediction step (we have new data in each iteration)
	
	# Calculate new estimate - using gyro since it has less noise
	estAngle_intermediate=estAngle_pre+(gyro_y_rel-old_angle)
	estVar_intermediate=estVar_pre+gyroVar
        old_angle=gyro_y_rel


	##### Kalman correction step (we have new data in each iteration)
        kalman_gain = estVar_intermediate / (estVar_intermediate+pitchVar)
        # Save old estimated value
	estAngle_pre=estAngle
	estVar_pre=estVar 
	
	estAngle=estAngle_intermediate+kalman_gain*(pitch-estAngle_intermediate)
        estVar=estVar_intermediate*(1-kalman_gain)


	# define which value to plot as the Kalman filter estimate
	kalman_estimate = estAngle

	# define which value to plot as the absolute value (pitch/roll)
	pitch_roll_plot = pitch

	# define which value to plot as the relative gyro value
	gyro_rel_plot = gyro_y_rel

	######################################################

	# if 3D liveview is enabled
	if show3DLiveView == True and count % show3DLiveViewInterval == 0:

		# determine what variables to liveview
		roll_view = 0.0
		yaw_view = 0.0
		pitch_view = kalman_estimate
		#print kalman_estimate

		imuview.set_axis (-pitch_view, -yaw_view, roll_view)
		imuview.update()
		time.sleep( dt*10 )

	# if plotting is enabled
	if showPlot == True:
		plotDataGyro.append(gyro_rel_plot*180.0/pi)
		plotDataAcc.append(pitch_roll_plot*180.0/pi)
		plotDataKalman.append(kalman_estimate*180.0/pi)

# closing the file	
f.close()

# show the plot
if showPlot == True:
	ion()
	plt.figure(1)
	plt.title('Gyro integrated (relative) angle')
	plt.plot(plotDataGyro)
	plt.savefig('imu_exercise_gyro.png')

	plt.figure(2)
	plt.title('Accelerometer (blue) & Kalman estimation (red) angles')
	plt.plot(plotDataAcc,'blue')
	plt.plot(plotDataKalman,'red')
	plt.savefig('imu_exercise_acc_kalman.png')
	plt.draw()
	print 'Press enter to quit'
	raw_input()


