#!/usr/bin/env python

import roslib
import aiml
import rospy
import os
import sys

from std_msgs.msg import String


class RobotAI():

    def __init__(self):
        self._robot = aiml.Kernel()
        self.pkg_dir = roslib.packages.get_pkg_dir('bender_ai')
        self.predicate = dict()
        self.initialize(self.pkg_dir+'/aiml')

    def initialize(self, aiml_dir):
        self._robot.learn(os.sep.join([aiml_dir, '*.aiml']))
        properties_file = open(os.sep.join([aiml_dir, 'bender.properties']), 'r')
        for line in properties_file:
            parts = line.split('=')
            key = parts[0]
            value = parts[1]
            self.predicate[key] = value
            self._robot.setBotPredicate(key, value)

    def getResponse(self, input):
        output = self._robot.respond(input)
        return output

    def getPredicate(self, key):
        return self.predicate[key]
