#!/usr/bin/env python
import qi
import os

import roslib
import rospy
import actionlib
import uchile_speech_web.speech_recognizer as sr

#from uchile_speech_web.msg import DoRecognitionAction, DoRecognitionResult, CalibrateThresholdAction, CalibrateThresholdResult


#48000 es la tasa de refrezco

import io

#ocupado para google


class SpeechRecognitionServer:
	def __init__(self):
		
		# Config naoqi
		self.session=qi.Session()
		self.connection_url = "tcp://" + environ["robot_ip"] + ":" + environ["robot_port"]
		self.session.connect(self.connection_url)

		#Audio record
		self.record_delay = 2
		self.record_time = 0
		self.recording = False

		self.audio_player = self.session.service("ALAudioPlayer")
		self.audio_recorder = self.session.service("ALAudioRecorder")
		self.audio_recorder.stopMicrophonesRecording()

		self.thread_recording = Thread(target=self.record_audio,args=(None,))
		self.thread_recording.daemon = True
		self.audio_terminate = False


		self.recognition_server = actionlib.SimpleActionServer('~recognizer_action', DoRecognitionAction, self.execute, False)
		self.threshold_server = actionlib.SimpleActionServer('~calibrate_threshold',CalibrateThresholdAction,self.calibrate,False)
		self.recognition_server.start()
		self.threshold_server.start()
		# Esto se debe modificar
		self.recognizer = sr.Recognizer()
		self.recognizer.operation_timeout = 15.0
		self.recognizer.energy_threshold = 4000
		self.recognizer.dynamic_energy_threshold = True
		self.is_recognizing = False

		self.recognition_response = DoRecognitionResult()
		self.calibrate_response = CalibrateThresholdResult()

	def get_audio(self,timeout):


	def execute(self, goal):
		self.is_recognizing = True
		timeout = 15
		if goal.timeout:
			timeout = goal.timeout
			rospy.loginfo("I have received a goal with timeout = "+str(timeout))
		audio=sr.AudioFile(os.environ['HOME']+"/record/recog.wav")
		with audio as source:
			s.adjust_for_ambient_noise(source)
			rospy.loginfo('Reconociendo')
			try:
				audio_wav = self.recognizer.listen(source)
			except:
				rospy.logerr("Timeout of listening. I recommend to calibrate the recognizer (run uchile_speech_web calibrate.py)")
				self.recognition_server.set_aborted()
				self.is_recognizing = False
				return
			rospy.loginfo('Listoco, I am sending the audio to google. It might take a while')
		try:
			recognized_sentence=self.recognizer.recognize_google(audio_wav)
			self.recognition_response.final_result = recognized_sentence
			self.recognition_server.set_succeeded(self.recognition_response)
			print ('Recognized: ' + recognized_sentence)
			self.is_recognizing = False
			return
		except sr.UnknownValueError:
			rospy.logwarn("Google Speech Recognition could not understand audio")
			self.recognition_server.set_aborted()
			self.is_recognizing = False
		except sr.RequestError as e:
			rospy.logerr("Could not request results from Google Speech Recognition service; {0}".format(e))
			self.recognition_server.set_aborted()
			self.is_recognizing = False
		except:
			rospy.logerr("Some error")
			self.recognition_server.set_aborted()
			self.is_recognizing = False

	#TODO revisar calibrate para pepper
	def calibrate(self,goal):
		duration = 1.0
		if goal.duration > 1.0 :
			duration = goal.duration
		if self.is_recognizing:
			self.threshold_server.set_preempted()
			rospy.logwarn("The recognizer is recognizing; I can't stole the power of the mic to calibrate it")
			return

		with sr.Microphone() as source:
			rospy.loginfo('Calibrating...')
			self.recognizer.adjust_for_ambient_noise(source,duration=duration)
		self.threshold_server.set_succeeded()
		rospy.loginfo('OK! the mic is calibrated')
		return

	

	

if __name__ == '__main__':
	rospy.init_node('recognizer')
	rospy.loginfo("I AM ALIVE!!!!!!!!!!!!")
	rospy.loginfo("So master, I am expecting your command")
	#server = SpeechRecognitionServer()
	s=sr.Recognizer()
	audio=sr.AudioFile(os.environ['HOME']+"/record/recog.wav")
	with audio as source: s.adjust_for_ambient_noise(source)
	with audio as source: input_google = s.listen(source)
	value = s.recognize_google(input_google)
	print value
	rospy.loginfo("Remember to calibrate me if you have trouble")
	rospy.spin()
