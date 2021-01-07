import webrtcvad


class State(object):
    """
    Sate base class
    """
    def __init__(self, id, next_state, prev_state):
        self.id = id
        self.next_state = next_state
        self.prev_state = prev_state

    def next(self, input):
        assert 0, "next not implemented"

class StateMachine(object):
    """
    Simple state machine class
    """
    def __init__(self, states_table):
        self.states = states_table
        self.current_state = states_table[0]

    def run(self, input):
        """
        Pass input to current state to update
        """
        self.current_state = self.states[self.current_state.next(input)]

class SilenceState(State):
    """
    Initial state with no speech
    """
    def next(self, input):
        if input:
            return self.next_state
        else:
            return self.id

class PossibleStartState(State):
    """
    State to filter false short speech detections
    """
    def __init__(self,id, next_state, prev_state, th):
        super(PossibleStartState, self).__init__(id, next_state, prev_state)
        self.th  = th
        self.count = 0

    def next(self, input):
        self.count += input
        if self.count == self.th:
            return self.next_state
        elif input:
            return self.id
        else:
            self.count = 0
            return self.prev_state

class SpeechState(State):
    """
    State during speech
    """
    def next(self, input):
        if input:
            return self.id
        else:
            return self.next_state

class PossibleEndState(State):
    """
    State to remain in speech during short silence, changes state on long silence
    """
    def __init__(self,id, next_state, prev_state, th):
        super(PossibleEndState,self).__init__(id, next_state, prev_state)
        self.th  = th
        self.count = 0

    def next(self, input):
        self.count += not input
        if self.count == self.th:
            return self.next_state
        elif input:
            self.count = 0
            return self.prev_state
        else:
            return self.id

class EndState(State):
    """
    Final state affter a long silence
    """
    def next(self, input):
        return self.id


SPEECHSTATE = 2
ENDSTATE = 4
class VADsm(StateMachine):
    """
    State machine with the VAD states and webrtcvad VAD system
    """
    def __init__(self, vad_agg, audio_rate):
        states = [
            SilenceState(id=0, next_state=1, prev_state=0),
            PossibleStartState(id=1, next_state=SPEECHSTATE, prev_state=0,th=10),
            SpeechState(id=SPEECHSTATE, next_state=3, prev_state=SPEECHSTATE),
            PossibleEndState(id=3, next_state=ENDSTATE, prev_state=SPEECHSTATE,th=10),
            EndState(id=ENDSTATE, prev_state=ENDSTATE, next_state=ENDSTATE)
        ]
        super(VADsm, self).__init__(states)

        self.vad = webrtcvad.Vad(mode=vad_agg)
        self.rate = audio_rate

    def input_block(self, audio_block):
        """
        Recieves audio block as input, detects voice activity with webrtcvad and
        runs the state machine
        """
        det = self.vad.is_speech(audio_block, self.rate)
        self.run(det)

    @property
    def current_state_id(self):
        return self.current_state.id

