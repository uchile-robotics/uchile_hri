cmake_minimum_required(VERSION 2.8.3)
project(bender_nlp)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  std_srvs
  uchile_msgs
  uchile_srvs
  uchile_util
)

catkin_python_setup()

