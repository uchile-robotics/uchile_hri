
import threading
import queue

from deepspeech import Model

class AsrProcThread(threading.Thread):
    def __init__(self, aud_q, model, group=None, target=None, name=None):
        super(AsrProcThread,self).__init__()
        self.target = target
        self.name = name
        self.q = aud_q
        self.model = model
        self.result = ""

    def run(self):
        stream = self.model.createStream()
        while True:
            # Get audio to send
            block = self.q.get()
            if block is None:
                break
            stream.feedAudioContent(block)
            self.q.task_done()
        self.result = stream.finishStream()