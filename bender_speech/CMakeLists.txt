cmake_minimum_required(VERSION 2.8.3)
project(bender_speech)

# <!-- rosdep name="gstreamer_pocketsphinx"/ -->

find_package(catkin REQUIRED COMPONENTS
  bender_msgs
  bender_srvs
  diagnostic_msgs
  roscpp
  roslib
  rospy
  sound_play
  std_msgs
  std_srvs
  bender_utils
)

catkin_python_setup()

###################################
## catkin specific configuration ##
###################################
catkin_package(
  INCLUDE_DIRS include
  LIBRARIES bender_speech
  CATKIN_DEPENDS bender_msgs bender_srvs diagnostic_msgs roscpp roslib rospy sound_play std_msgs std_srvs
#  DEPENDS system_lib
)

###########
## Build ##
###########

include_directories(include
  ${catkin_INCLUDE_DIRS}
  ${bender_utils_INCLUDE_DIRS}
)

# - - - synthesizer - - -
add_executable(synthesizer src/synthesizer.cpp)
add_dependencies(synthesizer ${catkin_EXPORTED_TARGETS})
target_link_libraries(synthesizer ${catkin_LIBRARIES})

# I n t e r a c t 
#add_executable(interact_speech src/macros/InteractSpeech.cpp)
#add_dependencies(interact_speech ${catkin_EXPORTED_TARGETS})
#target_link_libraries(interact_speech ${catkin_LIBRARIES})

# S e n t e n c e s
#add_executable(sentences src/macros/Sentences.cpp)
#add_dependencies(sentences ${catkin_EXPORTED_TARGETS})
#target_link_libraries(sentences ${catkin_LIBRARIES})

# - - - ask_question - - -
#add_executable(ask_question src/macros/AskQuestion.cpp)
#add_dependencies(ask_question ${catkin_EXPORTED_TARGETS})
#target_link_libraries(ask_question ${catkin_LIBRARIES})

