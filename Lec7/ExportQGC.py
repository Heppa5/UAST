"""  
exportQGC(wpt_list_list)
	Initialize the class using a list of lists with waypoint coordinates
		wpt_list_list = [x,y,z]	where x,y,z are lists
		
writeToFile(wpt_file_name)
	Write QGC waypoint list to a file.
"""

class exportQGC():
	
	# Fake QGC constants
	QGC_FRAME_ABSOLUTE = 0
	QGC_FRAME_RELATIVE = 3
	
	# QGC constants
	MAV_CMD_NAV_WAYPOINT = 16
	MAV_CMD_NAV_TAKEOFF = 22
	
	def __init__(self, wpt_list_list, current_wpt = 0, coord_frame = QGC_FRAME_ABSOLUTE, radius = 3.5, loiter_time = 0, desired_yaw = 0, hori_vmax = 1.0, vert_vmax = 1.0, autocontinue = 1):
		self.wpt_list_list = wpt_list_list
		self.current_wpt = current_wpt
		self.coord_frame = coord_frame
		self.radius = radius
		self.loiter_time = loiter_time
		self.desired_yaw = desired_yaw
		self.hori_vmax = hori_vmax
		self.vert_vmax = vert_vmax
		self.autocontinue = autocontinue

	def writeToFile(self, wpt_file_name):
		# export to QGC waypoint list
		f = open (wpt_file_name, 'w')
		f.write ('QGC WPL 120\n')
		f.write ('%d\t%d\t%d\t%d\t%.2f\t%.0f\t%.2f\t%.2f\t%.8f\t%.8f\t%.3f\t%d\n' % (0, self.current_wpt, self.coord_frame, self.MAV_CMD_NAV_TAKEOFF, self.radius, self.loiter_time*1000, self.desired_yaw, self.vert_vmax, self.wpt_list_list[0][0], self.wpt_list_list[0][1], self.wpt_list_list[0][2], self.autocontinue))

		for i in xrange(len(self.wpt_list_list)):
			f.write ('%d\t%d\t%d\t%d\t%.2f\t%.0f\t%.2f\t%.2f\t%.8f\t%.8f\t%.3f\t%d\n' % (i+1, self.current_wpt, self.coord_frame, self.MAV_CMD_NAV_WAYPOINT, self.radius, self.loiter_time*1000, self.hori_vmax, self.desired_yaw, self.wpt_list_list[i][0], self.wpt_list_list[i][1], self.wpt_list_list[i][2], self.autocontinue))
		f.close

