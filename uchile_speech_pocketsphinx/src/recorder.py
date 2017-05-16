#!/usr/bin/env python
import rospy
import alsaaudio
import wave
from std_msgs.msg import Empty, String

class Recorder:
    def __init__(self):
        self.record_sub = rospy.Subscriber("record", String, self.recordCallback)
        self.stop_sub= rospy.Subscriber("stop",Empty,self.stopCallback)
        self.stoped = False
    def recordCallback(self,msg):
        rospy.loginfo("Recording...")
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
        inp.setchannels(1)
        inp.setrate(16000)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp.setperiodsize(1024)
        self.stoped = False
        w = wave.open(msg.data, 'w')
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        while not self.stoped:
            l, data = inp.read()
            w.writeframes(data)
        w.close()
        rospy.loginfo("Finished")
    def stopCallback(self,data):
        self.stoped = True
if __name__ == '__main__':
    rospy.init_node('recorder', anonymous=True)
    r=Recorder()
    rospy.spin()