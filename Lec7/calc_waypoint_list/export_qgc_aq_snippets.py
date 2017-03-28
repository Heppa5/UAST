

# qgc parameters
qgc_dunno = 0
qgc_frame_takeoff = 0 # 0 = abs 3 = relative
qgc_frame_wpt = 0 # 0 = abs 3 = relative
qgc_poi_heading = desired_yaw_angle
qgc_vert_vmax = 1.0
qgc_radius = 3.5
qgc_loiter = wpt_loiter_time
qgc_hori_vmax = leg_velocity
qgc_yaw = desired_yaw_angle
qgc_dunno2 = 1



# qgc constants
MAV_CMD_NAV_WAYPOINT = 16
MAV_CMD_NAV_TAKEOFF = 22




# export to QGC waypoint list
f = open ('waypoints.txt', 'w')
f.write ('QGC WPL 120\n')
f.write ('%d\t%d\t%d\t%d\t%.2f\t%.0f\t%.2f\t%.2f\t%.8f\t%.8f\t%.3f\t%d\n' % (0, qgc_dunno, qgc_frame_takeoff, MAV_CMD_NAV_TAKEOFF, qgc_radius, qgc_loiter*1000, qgc_poi_heading, qgc_vert_vmax, rtell[0][0], rtell[0][1], alt, qgc_dunno2))

for i in xrange(len(rtell)):
	f.write ('%d\t%d\t%d\t%d\t%.2f\t%.0f\t%.2f\t%.2f\t%.8f\t%.8f\t%.3f\t%d\n' % (i+1, qgc_dunno, qgc_frame_wpt, MAV_CMD_NAV_WAYPOINT, qgc_radius, qgc_loiter*1000, qgc_hori_vmax, qgc_yaw, rtell[i][0], rtell[i][1], alt, qgc_dunno2))
f.close

