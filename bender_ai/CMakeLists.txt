cmake_minimum_required(VERSION 2.8.3)
project(bender_ai)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  std_srvs
  bender_msgs
  bender_srvs
  bender_utils
)

catkin_python_setup()

