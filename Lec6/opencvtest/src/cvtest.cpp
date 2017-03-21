#include <ros/ros.h>
//#include <std_msgs/UInt64.h>
#include <geometry_msgs/PoseStamped.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <stdio.h>

static const std::string OPENCV_WINDOW = "Image window";

using namespace cv;

class ImageConverter
{
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;
  image_transport::Publisher image_pub_;
  ros::Publisher xy_pub;
  
public:
  ImageConverter()
    : it_(nh_)
  {
    // Subscrive to input video feed and publish output video feed
    //image_sub_ = it_.subscribe("/camera/left/image_color", 1,
      //&ImageConverter::imageCb, this);
    image_sub_ = it_.subscribe("/rrbot/camera1/image_raw", 1,
      &ImageConverter::imageCb, this);
    image_pub_ = it_.advertise("/image_converter/output_video", 1);

    cv::namedWindow(OPENCV_WINDOW);
  }

  ~ImageConverter()
  {
    cv::destroyWindow(OPENCV_WINDOW);
  }

  void imageCb(const sensor_msgs::ImageConstPtr& msg)
  {
    cv_bridge::CvImagePtr cv_ptr;
    try
    {
      cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
    }
    catch (cv_bridge::Exception& e)
    {
      ROS_ERROR("cv_bridge exception: %s", e.what());
      return;
    }

    // Draw an example circle on the video stream
    //if (cv_ptr->image.rows > 60 && cv_ptr->image.cols > 60)
      //cv::circle(cv_ptr->image, cv::Point(50, 50), 10, CV_RGB(255,0,0));

		// Extract hue information
    Mat hsv_temp, hsv[3];
    //cvtColor(cv_ptr->image, hsv_temp, CV_BGR2HSV); // convert image to HSV color space
    cvtColor(cv_ptr->image, hsv_temp, CV_RGB2HSV); // convert image to HSV color space
    split(hsv_temp, hsv);    // split image into hue, saturation and value images
    Mat sat = hsv[1].clone();   // select hue channel
    
    // Perform hue thresholding
    int sat_min = 1,
        sat_red = 255;
    Mat bin;
    inRange(sat, sat_min, sat_red, bin);
    
    /// Find contours
    std::vector<std::vector<Point> > contours;
    std::vector<Vec4i> hierarchy;
    findContours(sat, contours, hierarchy,
            CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));
            
    /// Get the moments
		std::vector<Moments> mu(contours.size());
    for (int i = 0; i < contours.size(); i++) {
            mu[i] = moments(contours[i], false);
    }
    
    /// Find the most circular contour in the binary image
    double maxRatio = 0, curRatio;
    Point2f maxCenter, curCenter;
    for (int i = 0; i < contours.size(); i++) {
      float radius;
      minEnclosingCircle(contours[i], curCenter, radius);
      curRatio = mu[i].m00 / radius;  // mu[i].m00 is the contour area
      if ( curRatio > maxRatio ) {
        maxRatio = curRatio;
        maxCenter = curCenter;
      }
    }
    
    // Draw ball position onto original stream
    Scalar color(0, 255, 0);
    circle( cv_ptr->image,
    				maxCenter,
            3,
            color,
            5,
            8 );
    

    // Update GUI Window
    cv::imshow(OPENCV_WINDOW, sat/*cv_ptr->image*/);
    cv::waitKey(3);
    
    // Output modified video stream
    image_pub_.publish(cv_ptr->toImageMsg());
    
    xy_pub = nh_.advertise<geometry_msgs::PoseStamped>("opencvtest/center", 1000);
    //uint64_t center_out = (uint64_t) maxCenter.x << 32 | (uint32_t)maxCenter.y;
    
    geometry_msgs::PoseStamped msg_center;
    msg_center.pose.position.x = maxCenter.x;
    msg_center.pose.position.y = maxCenter.y;
    msg_center.pose.position.z = 0;
    xy_pub.publish(msg_center);
  }
};

int main(int argc, char** argv)
{
  ros::init(argc, argv, "image_converter");
  ImageConverter ic;
  ros::spin();
  return 0;
}
