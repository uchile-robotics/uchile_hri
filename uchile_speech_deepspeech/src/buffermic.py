from queue import Queue 
from threading import Thread, Event 
from collections import deque

import pyaudio

class MicManager(Thread):
    def __init__(self, bps, rate, buff_duration=1.0, format=pyaudio.paInt16):
        super(MicManager,self).__init__()
        self.rate = rate
        self.bps = bps
        self.fpb = int(self.rate//self.bps)
        self.format = format
        deque_len = int(buff_duration * self.bps)
        self.q = deque(maxlen=deque_len)
        self.queue = Queue()
        self.q_enable = False
        self.n_blocks = 0
        self.feed = False
        self.empty = False
        
        self.on = True
        self.start()
        
    def close(self):
        self.on = False

    def run(self):
        p = pyaudio.PyAudio()
        mic_stream = p.open(format=self.format, 
                            channels=1, 
                            rate=self.rate, 
                            input=True, 
                            frames_per_buffer=2*self.fpb)

        while self.on:
            mic_data = mic_stream.read(self.fpb)
            self._proc_queue(mic_data)
            self.q.append(mic_data)

        mic_stream.stop_stream()
        mic_stream.close()
        p.terminate()

    def _proc_queue(self,data):
        if self.q_enable:
            self.queue.put(data)
        elif self.feed:
            try:
                for i in range(self.n_blocks):
                    self.queue.put( self.q[-(self.n_blocks) + i] )
            except IndexError:
                pass
            self.queue.put(data)
            self.feed = False
            self.q_enable = True
        elif self.empty:
            while not self.queue.empty():
                self.queue.get()
    
    def connect(self, start=0):
        self.n_blocks = int(start * self.bps)
        self.feed= True
        return self.queue
    
    def disconnect(self):
        self.q_enable = False
        self.empty = True