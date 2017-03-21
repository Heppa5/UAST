#include "ros/ros.h"
#include "std_msgs/String.h"
#include <geometry_msgs/PoseStamped.h>



int main(int argc, char **argv)
{
  
  ros::init(argc, argv, "target_pos_generator");


  ros::NodeHandle nh;

    // Create publisher of generated Target Points
  ros::Publisher target_pub = nh.advertise<geometry_msgs::PoseStamped>("mavros/targetPosition", 100);

  ros::Rate loop_rate(1);   //1Hz frequency of loop


  int x = 0;
  int dir = 1;
  while (ros::ok())
  {
    // Using geometry_msgs from Mavros package
    geometry_msgs::PoseStamped msg;

    // Generate target position in interval <-5,5>m
    if (dir == 1)
    {
        if (x < 5)
            x++;
        else
            dir = -1;
    }
    else
    {
        if (x > -5)
            x--;
        else
            dir = 1;
    }
    ROS_INFO("%d\n", x);    // Print value of x into terminal
    
    //Compose ROS message
    msg.pose.position.x = x;
    msg.pose.position.y = 0;
    msg.pose.position.z = 2;

    
    target_pub.publish(msg);

    ros::spinOnce();

    loop_rate.sleep();
  }


  return 0;
}
