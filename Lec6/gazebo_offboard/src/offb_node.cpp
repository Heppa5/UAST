/*
 *  Originally from: https://dev.px4.io/ros-mavros-offboard.html
 */

#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>
#include <mavros_msgs/CommandBool.h>
#include <mavros_msgs/SetMode.h>
#include <mavros_msgs/State.h>


mavros_msgs::State current_state;
void state_cb(const mavros_msgs::State::ConstPtr& msg){
    current_state = *msg;
}

geometry_msgs::PoseStamped pose;
void target_pos_cb(const geometry_msgs::PoseStamped::ConstPtr& msg){
       pose = *msg; 
}

geometry_msgs::PoseStamped targ_Px;
double errx, erry, old_errx, old_erry;
void targ_Px_cb(const geometry_msgs::PoseStamped::ConstPtr& msg){
       targ_Px = *msg; 
       errx = (targ_Px.pose.position.x - 400);
       erry = (targ_Px.pose.position.y - 400);
       pose.pose.position.x -= (errx/10000 + (errx - old_errx)/500);
       pose.pose.position.y -= (erry/10000 + (erry - old_erry)/500);
       old_errx = errx;
       old_erry = erry;
       ROS_INFO("%f\n", pose.pose.position.x); 
       ROS_INFO("%f\n", pose.pose.position.y); 
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "offb_node");
    ros::NodeHandle nh;

    ros::Subscriber state_sub = nh.subscribe<mavros_msgs::State>
            ("mavros/state", 10, state_cb);
            
    ros::Subscriber target_Pos_sub = nh.subscribe<geometry_msgs::PoseStamped>
            ("mavros/targetPosition", 100, target_pos_cb);
            
    ros::Subscriber targ_Px_coord_sub = nh.subscribe<geometry_msgs::PoseStamped>
            ("opencvtest/center", 10, targ_Px_cb);
            
    ros::Publisher local_pos_pub = nh.advertise<geometry_msgs::PoseStamped>
            ("mavros/setpoint_position/local", 10);
    ros::ServiceClient arming_client = nh.serviceClient<mavros_msgs::CommandBool>
            ("mavros/cmd/arming");
    ros::ServiceClient set_mode_client = nh.serviceClient<mavros_msgs::SetMode>
            ("mavros/set_mode");

    //the setpoint publishing rate MUST be faster than 2Hz
    ros::Rate rate(20.0);

    // wait for FCU connection
    while(ros::ok() && current_state.connected){
        ros::spinOnce();
        rate.sleep();
    }

    
    pose.pose.position.x = 0;
    pose.pose.position.y = 0;
    pose.pose.position.z = 2;

    //send a few setpoints before starting, or else you won't be able to switch to offboard mode
    for(int i = 10; ros::ok() && i > 0; --i){
        local_pos_pub.publish(pose);
        ros::spinOnce();
        rate.sleep();
    }

    mavros_msgs::SetMode offb_set_mode;
    offb_set_mode.request.custom_mode = "OFFBOARD";

    mavros_msgs::CommandBool arm_cmd;
    arm_cmd.request.value = true;

    ros::Time last_request = ros::Time::now();

    while(ros::ok()){
        if( current_state.mode != "OFFBOARD" &&
            (ros::Time::now() - last_request > ros::Duration(5.0))){
            if( set_mode_client.call(offb_set_mode) &&
                offb_set_mode.response.success){
                ROS_INFO("Offboard enabled");
            }
            last_request = ros::Time::now();
        } else {
            if( !current_state.armed &&
                (ros::Time::now() - last_request > ros::Duration(5.0))){
                if( arming_client.call(arm_cmd) &&
                    arm_cmd.response.success){
                    ROS_INFO("Vehicle armed");
                }
                last_request = ros::Time::now();
            }
        }

        local_pos_pub.publish(pose);

        ros::spinOnce();
        rate.sleep();
    }

    return 0;
}
