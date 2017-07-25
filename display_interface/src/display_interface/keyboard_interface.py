#!/usr/bin/env python


import rospy
import rospkg
import sys
import os

from uchile_srvs.srv import stringReturn, stringReturnResponse


class KeyboardInterface():
    """
    Base class for gender_recognition
    """
    _type = "keyboard_interface"

    def __init__(self):
        self._description = "Keyboard Interface"

        self.namespace_prefix=(rospy.get_namespace()+'/'+KeyboardInterface._type+'/').replace('//','/')
        self.wait_service = rospy.Service(self.namespace_prefix+'wait_write', stringReturn, self._waitwrite)


    def _waitwrite(self, req):
        res = stringReturnResponse()
        res.data = raw_input("Write your sentence: ")
        return res



def main():

    rospy.init_node('KeyboardInterface')

    KeyboardInterface()
    rospy.spin()

if __name__ == '__main__':
    main()
