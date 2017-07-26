cmake_minimum_required(VERSION 2.8.3)
project(display_interface)

find_package(catkin REQUIRED COMPONENTS
  roslib
  rospy
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS rospy std_msgs

)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)
