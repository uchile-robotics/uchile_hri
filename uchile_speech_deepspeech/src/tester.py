#! /usr/bin/env python


import rospy

# Brings in the SimpleActionClient
import actionlib

# Brings in the messages used by the fibonacci action, including the
# goal message and the result message.
import uchile_speech_deepspeech.msg

def tester_client():
    # Creates the SimpleActionClient, passing the type of the action
    # (FibonacciAction) to the constructor.
    client = actionlib.SimpleActionClient('/bender/speech_deepspeech/recognizer/recognizer_action', uchile_speech_deepspeech.msg.DoRecognitionAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    goal = uchile_speech_deepspeech.msg.DoRecognitionGoal(timeout=10, start_time=1)

    # Sends the goal to the action server.
    client.send_goal(goal)

    # Waits for the server to finish performing the action.
    client.wait_for_result()

    # Prints out the result of executing the action
    return client.get_result()

if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('tester_client_py')
        result = tester_client()
        print result
    except rospy.ROSInterruptException:
        print "program interrupted before completion"