#!/usr/bin/env python
import qi
import os

import roslib
import rospy
import actionlib
import uchile_speech_web.speech_recognizer as sr

from uchile_speech_web_pepper.msg import DoRecognitionAction, DoRecognitionResult, CalibrateThresholdAction, CalibrateThresholdResult
from threading import Thread
import thread
import time
import io

#48000 es la tasa de refrezco
class SpeechRecognitionServer:
	def __init__(self):
		
		rospy.loginfo("##########INIT#############")
		# Config naoqi
		self.session=qi.Session()
		self.connection_url = "tcp://" + os.environ["robot_ip"] + ":" + os.environ["robot_port"]
		self.session.connect(self.connection_url)

		#Audio record
		self.record_delay = 2
		self.record_time = 0
		self.recording = False

		self.audio_player = self.session.service("ALAudioPlayer")
		self.audio_recorder = self.session.service("ALAudioRecorder")
		self.leds = self.session.service("ALLeds")

		self.audio_recorder.stopMicrophonesRecording()

		self.recognition_server = actionlib.SimpleActionServer('~recognizer_action', DoRecognitionAction, self.execute,False)
		self.threshold_server = actionlib.SimpleActionServer('~calibrate_threshold',CalibrateThresholdAction,self.calibrate,False)
		self.recognition_server.start()
		self.threshold_server.start()
		
		#
		self.ALMEM = self.session.service("ALMemory")
		IP=os.environ["robot_ip"]
		PORT=os.environ["robot_port"]
		# Esto se debe modificar
		#self.recognizer = sr.Recognizer()
		#self.recognizer.operation_timeout = 15.0
		#self.recognizer.energy_threshold = 4000
		#self.recognizer.dynamic_energy_threshold = True
		#self.is_recognizing = False

		self.recognition_response = DoRecognitionResult()
		self.calibrate_response = CalibrateThresholdResult()
		self.beep_volume = 70
		#init_speech_recognition(0.3)

	def init_speech_recognition(self,sensitivity=0.3):
		# sound detection
		self.enable_speech_recog = True
		self.sound_det_s = self.session.service("ALSoundDetection")
		self.sound_det_s.setParameter("Sensitivity", sensitivity)
		self.sound_det_s.subscribe('sd')
		self.sound_det = self.ALMEM.subscriber("SoundDetected")
		self.sound_det.signal.connect(self.callback_sound_det)
		#self.thread_headfix.start()

		#self.say('Speech recognition start')
		rospy.loginfo("Speech Recognition start")
		self.sr_flag = True

	def callback_sound_det(self,msg):
		rospy.loginfo("Call back sound")
		ox = 0		
		for i in range(len(msg)):
			if msg[i][1] == 1 :
				ox = 1
			rospy.loginfo(self.enable_speech_recog)
		if ox == 1 and self.enable_speech_recog:
			self.record_time = time.time()+self.record_delay
			rospy.loginfo(self.record_time)

			if not self.thread_recording.is_alive() :
				self.start_recording(reset=True)
			
		else : 
			self.there_was_detection=1
			self.time_last_detection=time.time()
			rospy.loginfo("Salgo del callback_sound_det")
			return None

	
	def set_sound_sensitivity(self,sensitivity=0.3):
		self.sound_det_s.setParameter("Sensitivity", sensitivity)


	def start_recording(self,reset=False,base_duration=3, withBeep=True):
		if reset :
			self.kill_recording_thread()
			self.audio_recorder.stopMicrophonesRecording()
			self.record_time = time.time()+base_duration

		if not self.thread_recording.is_alive():
			self.thread_recording = Thread(target=self.record_audio,args=())
			self.thread_recording.daemon = False
			self.thread_recording.start()
			self.thread_recording.join()
			return ''
		return ''

	def kill_recording_thread(self):
		if self.thread_recording.is_alive() :
			self.audio_terminate = True
			time.sleep(0.3)
			self.audio_terminate = False

	def record_audio(self, withBeep=False):
		#while self.there_was_detection==0:
			#rospy.sleep(0.1)
		#init_time=time.time()
		while time.time() < self.init_time + self.timeout:
			if withBeep:
				self.audio_player.playSine(1000,self.beep_volume,1,0.3)
				time.sleep(0.5)
			print 'Speech Detected : Start Recording'
			rospy.loginfo("Speech detected State")
			channels = [0,0,1,0] #left,right,front,rear
			fileidx = "recog"
			self.audio_recorder.startMicrophonesRecording("/home/nao/record/"+fileidx+".wav", "wav", 48000, channels)
			rospy.sleep(3)
			print time.time()
			print str(self.record_time)+"record_time"
			self.leds.rotateEyes(255,1,2)
			while self.there_was_detection==0 and time.time() < self.init_time + self.timeout:
				rospy.sleep(0.1)
				self.leds.rotateEyes(255,1,0.1)
			while time.time() < self.record_time and time.time() < self.init_time + self.timeout:
				self.leds.rotateEyes(255,1,0.1)
				if self.audio_terminate :
					self.audio_recorder.stopMicrophonesRecording()
					print 'kill!!'
					return None
				time.sleep(0.1)
			
			self.audio_recorder.stopMicrophonesRecording()
			self.audio_recorder.recording_ended = True
			self.finish = True
			if not os.path.exists('./audio_record'):
				os.mkdir('./audio_record', 0755)

			
			rospy.loginfo("End recording")
			self.leds.on("AllLeds")
			#self.thread_concept = Thread(target=self.record_concepts,args=(stamp,spp,))
			#self.thread_concept.daemon = False
			#self.thread_concept.start()
			#self.speech_memory = self.stt2("audio_record/recog.wav",hints)
			
			# if self.enable_concept_map and self.speech_memory != '' : 
			# 	stamp = str(time.time()).replace('.','')
			# 	spp = self.speech_memory.split(' ')			
			# 	self.text_concepts.append([int(stamp),self.speech_memory])
			# 	if len(self.text_concepts) > 1000 : del self.text_concepts[0]
			# 	for ww in spp : 
			# 		self.text_corpus.append(ww)
					
					
			# 	self.text_corpus = list(set(self.text_corpus))
					
			# 	f = open('concept_map/raw_data/'+stamp+'.txt','w')
			# 	for iii in range( len(spp)-1 ) :
			# 		f.write(spp[iii]+'\n')
			# 	f.write(spp[-1])
			# 	f.flush()
			# 	f.close
				
				# self.thread_concept = Thread(target=self.record_concepts,args=(stamp,spp,))
				# self.thread_concept.daemon = False
				# self.thread_concept.start()

					
			#if self.data_recording and self.data_recording_dir != '' :
				#now = datetime.datetime.now()
				#strnow = now.strftime('%Y-%m-%d_%H-%M-%S-%f')[:-3]
				#shutil.copy2('audio_record/recog.wav' , self.data_recording_dir + '/audio/AUPAIR_AUDIO_'+ strnow + '.wav')
			if withBeep:
				self.audio_player.playSine(250,self.beep_volume,1,0.3)
				time.sleep(1)
				rospy.loginfo("Second beep")
			return None
		self.audio_recorder.stopMicrophonesRecording()
		self.audio_recorder.recording_ended = True
		self.finish = True
		return None

	def execute(self, goal):
		self.there_was_detection=0
		self.finish = False
		self.init_time=time.time()
		if goal.timeout:
			timeout = goal.timeout
			self.timeout=goal.timeout
			rospy.loginfo("I have received a goal with timeout = "+str(timeout))
		self.time_last_detection=time.time()
		self.thread_recording = Thread(target=self.record_audio,args=())
		self.thread_recording.daemon = True
		self.audio_terminate = False
		self.thread_recording.start()
		#self.audio_player.playSine(250,self.beep_volume,1,0.3)
		time.sleep(0.5)
		self.audio_initial_time=time.time()
		self.init_speech_recognition()
		rospy.loginfo("Speech detected State second one")
		channels = [0,0,1,0] #left,right,front,rear
		fileidx = "recog"
		#self.audio_recorder.startMicrophonesRecording("/home/nao/record/"+fileidx+".wav", "wav", 48000, channels)
		#rospy.sleep(5)
		#self.audio_recorder.stopMicrophonesRecording()
		delta=0.5
		
		self.init_time=time.time()

		#max len audio vacio
		maxlen=3

		while self.there_was_detection==0 and time.time() < self.init_time+timeout:
			rospy.sleep(0.1)
			if self.audio_initial_time+maxlen<time.time():
				self.audio_recorder.stopMicrophonesRecording()
				time.sleep(0.1)
				self.audio_recorder.startMicrophonesRecording("/home/nao/record/"+fileidx+".wav", "wav", 48000, channels)
				self.audio_initial_time=time.time()
				rospy.loginfo("Restart Audio because it was empty")
		while time.time()<self.time_last_detection+delta:
			while not self.finish:
				rospy.loginfo("AUN NO TERMINO DE GRABAAAAAAAAR")
				rospy.sleep(0.1)
		
		self.leds.on("AllLeds")

		audio=sr.AudioFile(os.environ['HOME']+"/record/recog.wav")
		audio_blank=sr.AudioFile(os.environ['HOME']+"/record/blank.wav")

		try:
			with audio as source:
				s.adjust_for_ambient_noise(source)
				rospy.loginfo('Reconociendo')
		except:
			audio=audio_blank
		
		with audio as source:
			s.adjust_for_ambient_noise(source)
			rospy.loginfo('Reconociendo')	
			audio_wav = s.listen(source)
			try:
				audio_wav = s.listen(source)
			except:
				rospy.logerr("Timeout of listening. I recommend to calibrate the recognizer (run uchile_speech_web calibrate.py)")
				self.recognition_server.set_aborted()
				self.is_recognizing = False
			rospy.loginfo('Listoco, I am sending the audio to google. It might take a while')
		try:
			with audio as source: 
				s.adjust_for_ambient_noise(source)
			with audio as source: 
				input_google = s.listen(source)
			self.recognition_response.final_result = s.recognize_google(input_google)
			self.recognition_server.set_succeeded(self.recognition_response)
			print ('Recognized: ' + self.recognition_response.final_result)
			self.ALMEM.raiseEvent("WordRecognized", [str(self.recognition_response.final_result)])

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
	s=sr.Recognizer()
	audio=sr.AudioFile(os.environ['HOME']+"/record/test.wav")
	with audio as source: 
		s.adjust_for_ambient_noise(source)
	with audio as source: 
		input_google = s.listen(source)
	try:
		result=s.recognize_google(input_google)
		if result=='what is your name':
			rospy.loginfo("Google Speech working")
		else:
			rospy.loginfo("Google Speech not recognizing very well")
	except Exception as e:
		rospy.loginfo("Google Speech not working")
		pass
	server = SpeechRecognitionServer()
	#server.init_speech_recognition(0.3)
	rospy.loginfo("Remember to calibrate me if you have trouble")
	rospy.spin()
