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
        self.recognition_server.start()

        # Load deepspeech model
        rospack = rospkg.RosPack()
        pkg_path = rospack.get_path('uchile_speech_deepspeech')
        model_path = os.path.join(pkg_path, "model/deepspeech-0.8.2-models.pbmm")
        scorer_path = os.path.join(pkg_path, "model/gpsr.scorer")
        self.recognizer = Model(model_path)
        self.recognizer.enableExternalScorer(scorer_path)

        self.mic_manager = MicManager(buff_duration = 10, bps = BLOCKS_PER_SECOND, rate = RATE, format = FORMAT)



        self.recognition_response = DoRecognitionResult()


    def terminate(self):
        self.mic_manager.close()

    def execute(self, goal):
        timeout = 15
        if goal.timeout:
            timeout = goal.timeout
            rospy.loginfo("I have received a goal with timeout = "+str(timeout))

        # Set up state machine for VAD
        pre_buf = deque(maxlen=15)
        aud_buf = []
        sm_vad = vad_sm.VADsm(vad_agg=VAD_AGG, audio_rate = RATE)

        # Set up connection
        audio_in = self.mic_manager.connect(start=1)

        # Set up model
        asr_audio = queue.Queue()
        asr_thread = AsrProcThread(name='audioASR',model=self.recognizer, aud_q=asr_audio)
        asr_thread.start()

        
        rospy.loginfo('Listening ...')
        t_start = time.time()
        start_speech = False
        while sm_vad.current_state_id != vad_sm.ENDSTATE:
            if time.time() - t_start > timeout:
                self.recognition_server.set_aborted()
                rospy.loginfo('timeout reached')
                # Close asr thread
                asr_audio.put(None)
                asr_thread.join()
                return
                
            audio_block = audio_in.get()
            sm_vad.input_block(audio_block)

            #det = vad.is_speech(audio_block, RATE)
            #sm.run(det)

            if not start_speech:
                if sm_vad.current_state_id == vad_sm.SPEECHSTATE:
                    start_speech = True
                    for b in pre_buf:
                            aud_buf.append(b)
                            asr_audio.put(np.frombuffer(b, dtype=np.int16))
                    rospy.loginfo('Speech start')
                else:
                    pre_buf.append(audio_block)
            else:
                aud_buf.append(audio_block)
                asr_audio.put(np.frombuffer(audio_block, dtype=np.int16))
        rospy.loginfo('done')

        # End audio caption
        self.mic_manager.disconnect()
        asr_audio.put(None)

        # Wait for recognition
        asr_thread.join()
        recognized_sentence = asr_thread.result
        #print recognized_sentence
        #rospy.loginfo("Result: ", recognized_sentence)
        self.recognition_response.final_result = recognized_sentence
        self.recognition_server.set_succeeded(self.recognition_response)
        #self.is_recognizing = False

        # timeout = 15
        # if goal.timeout:
        #   timeout = goal.timeout
        #   rospy.loginfo("I have received a goal with timeout = "+str(timeout))
        # with sr.Microphone() as source:
        #   rospy.loginfo('Reconociendo')
        #   try:
        #       audio = self.recognizer.listen(source,timeout=timeout)
        #   except:
        #       rospy.logerr("Timeout of listening. I recommend to calibrate the recognizer (run uchile_speech_web calibrate.py)")
        #       self.recognition_server.set_aborted()
        #       self.is_recognizing = False
        #       return
        #   rospy.loginfo('Listoco, I am sending the audio to google. It might take a while')
        # try:
        #   recognized_sentence=self.recognizer.recognize_google(audio)
        #   self.recognition_response.final_result = recognized_sentence
        #   self.recognition_server.set_succeeded(self.recognition_response)
        #   print ('Recognized: ' + recognized_sentence)
        #   self.is_recognizing = False
        #   return
        # except sr.UnknownValueError:
        #   rospy.logwarn("Google Speech Recognition could not understand audio")
        #   self.recognition_server.set_aborted()
        #   self.is_recognizing = False
        # except sr.RequestError as e:
        #   rospy.logerr("Could not request results from Google Speech Recognition service; {0}".format(e))
        #   self.recognition_server.set_aborted()
        #   self.is_recognizing = False
        # except:
        #   rospy.logerr("Some error")
        #   self.recognition_server.set_aborted()
        #   self.is_recognizing = False


    # def calibrate(self,goal):
    #   duration = 1.0
    #   if goal.duration > 1.0 :
    #       duration = goal.duration
    #   if self.is_recognizing:
    #       self.threshold_server.set_preempted()
    #       rospy.logwarn("The recognizer is recognizing; I can't stole the power of the mic to calibrate it")
    #       return

    #   with sr.Microphone() as source:
    #       rospy.loginfo('Calibrating...')
    #       self.recognizer.adjust_for_ambient_noise(source,duration=duration)
    #   self.threshold_server.set_succeeded()
    #   rospy.loginfo('OK! the mic is calibrated')
    #   return

if __name__ == '__main__':
    rospy.init_node('recognizer')
    server = SpeechRecognitionServer()
    rospy.loginfo("Recognizer initialized")
    rospy.spin()
    
    # Close threads on exit
    server.terminate()
