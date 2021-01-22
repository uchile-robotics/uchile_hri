#!/usr/bin/env python
import os
import queue
from collections import deque
import time

import roslib
import rospy
import rospkg
import actionlib
#import speech_recognition as sr
from deepspeech import Model
import pyaudio
import numpy as np

from uchile_speech_deepspeech.msg import DoRecognitionAction, DoRecognitionResult

from buffermic import MicManager
from par_asr import AsrProcThread
import vad_sm

FORMAT = pyaudio.paInt16
RATE = 16000
BLOCKS_PER_SECOND = 50

VAD_AGG = 3

class SpeechRecognitionServer:
    def __init__(self):
        self.recognition_server = actionlib.SimpleActionServer('~recognizer_action', DoRecognitionAction, self.execute, False)

        # Load deepspeech model
        rospack = rospkg.RosPack()
        pkg_path = rospack.get_path('uchile_speech_deepspeech')
        model_path = os.path.join(pkg_path, "model/deepspeech-0.8.2-models.pbmm")
        scorer_path = os.path.join(pkg_path, "model/gpsr.scorer")
        self.recognizer = Model(model_path)
        self.recognizer.enableExternalScorer(scorer_path)

        self.mic_manager = MicManager(buff_duration = 10, bps = BLOCKS_PER_SECOND, rate = RATE, format = FORMAT)



        self.recognition_response = DoRecognitionResult()
        self.recognition_server.start()


    def terminate(self):
        """
        Stops the microphone buffer thread
        """
        self.mic_manager.close()

    def execute(self, goal):
        timeout = 15
        if goal.timeout:
            timeout = goal.timeout
            rospy.loginfo("I have received a goal with timeout = "+str(timeout))

        recording_start_time = 0
        if goal.start_time:
            recording_start_time = goal.start_time
            rospy.loginfo("Started recognition from {} seconds in the past".format(recording_start_time))

        # Set up state machine for VAD
        pre_buf = deque(maxlen=15)
        aud_buf = []
        sm_vad = vad_sm.VADsm(vad_agg=VAD_AGG, audio_rate = RATE)

        # Set up connection to mic manager
        audio_in = self.mic_manager.connect(start=recording_start_time)

        # Set up model
        asr_stream = self.recognizer.createStream()
        
        rospy.loginfo('Listening ...')
        t_start = time.time()
        start_speech = False
        success = True
        while sm_vad.current_state_id != vad_sm.ENDSTATE:
            # Check for early stop conditions
            if time.time() - t_start > timeout:
                self.recognition_server.set_aborted()
                rospy.loginfo('Timeout reached')
                success = False
                break
            elif self.recognition_server.is_preempt_requested():
                rospy.loginfo('Preempted')
                self.recognition_server.set_preempted()
                success = False
                break

            audio_block = audio_in.get()
            sm_vad.input_block(audio_block)

            if not start_speech:
                if sm_vad.current_state_id == vad_sm.SPEECHSTATE:
                    start_speech = True
                    # include past audio
                    for b in pre_buf:
                            aud_buf.append(b)
                            asr_stream.feedAudioContent(np.frombuffer(b, dtype=np.int16))

                    rospy.loginfo('Speech start')
                else:
                    pre_buf.append(audio_block)
            else:
                aud_buf.append(audio_block)
                asr_stream.feedAudioContent(np.frombuffer(audio_block, dtype=np.int16))
        rospy.loginfo('done')

        # End audio capture
        self.mic_manager.disconnect()

        if success:
            recognized_sentence = asr_stream.finishStream()
            #print recognized_sentence
            #rospy.loginfo("Result: ", recognized_sentence)
            self.recognition_response.final_result = recognized_sentence
            self.recognition_server.set_succeeded(self.recognition_response)


if __name__ == '__main__':
    rospy.init_node('recognizer')
    server = SpeechRecognitionServer()
    rospy.loginfo("Recognizer initialized")
    rospy.spin()
    
    # Close threads on exit
    server.terminate()
