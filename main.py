import pyaudio
import numpy as np
from random import randint
import math

from param import _Param
from oscillator import OscSine
from envelope import EnvLinear, EnvExpontial


p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = 1.0   # in seconds, may be float
f = 220.0        # sine frequency, Hz, may be float

def env_exp(x, b, a0, a1, t0, t1):
    assert b > 0 and b <= 1
    assert a0 >= 0 and a0 <= 1
    assert a1 >= 0 and a1 <= 1
    assert t0 >= 0 and t1 > 0

    #magic gradual start term dissapear factor
    #   -too large = start not gradual enough
    #   -too small = does not reach a1 by t1
    #g = 5

    #m = (x - t0) / (b * (t1 - t0))
    #n = (1-b) * np.exp(-g * (x - t0) / b)

    #gradual start term - starts at linear envelope slope near t0 - causes clipping
    #d = n * m * (a1 - a0) / np.exp(m)

    return (a0 - a1) * np.power(1 - (x - t0) / (t1 - t0), 1 / b) + a1

class Note(_Param):
    param_list = ["start", "duration", "amplitude"]
    opt_param_list = ["attack", "decay", "sustain", "release", "envelope"]

    def __init__(self, params):
        super().__init__(params)

        assert self.attack + self.decay + self.release < self.duration or math.isclose(self.attack + self.decay + self.release, self.duration)
        
        self.buff = np.arange(int(fs*duration)).astype(np.float32)
        self.env = np.empty(int(fs*duration)).astype(np.float32)

    def _set_opt_param_vals(self, params):
        if not "attack" in params:
            self.attack = 0.1 * params["duration"]
        if not "decay" in params:
            self.decay = 0.1 * params["duration"]
        if not "sustain" in params:
            self.sustain = params["amplitude"]
        if not "release" in params:
            self.release = 0.1 * params["duration"]
        if not "envelope" in params:
            self.envelope = EnvExponential

    def envelope(self):
        a = int(self.attack*fs)
        _d = int(self.decay*fs)
        d = int((self.attack+self.decay)*fs)
        s = int((self.duration-self.release)*fs)
        r = int(self.release*fs)

        self.env[:a] = np.linspace(0.0, self.amplitude, a)
        self.env[a:d] = np.linspace(self.amplitude, self.sustain, _d)
        self.env[d:s] = self.sustain
        self.env[s:] = np.linspace(self.sustain, 0.0, r)
        self.buff *= self.env

    def envelope_exp(self):
        a = int(self.attack*fs)
        _d = int(self.decay*fs)
        d = int((self.attack+self.decay)*fs)
        s = int((self.duration-self.release)*fs)
        r = int(self.release*fs)
        b = .326

        self.env[:a] = env_exp(np.linspace(0.0, self.attack, a), b, 0.0, self.amplitude, 0.0, self.attack)
        self.env[a:d] = env_exp(np.linspace(self.attack, self.attack + self.decay, _d), b, self.amplitude, self.sustain, self.attack, self.attack + self.decay)
        self.env[d:s] = self.sustain
        self.env[s:] = env_exp(np.linspace(self.duration - self.release, self.duration, r), b, self.sustain, 0.0, self.duration - self.release, self.duration)
        self.buff *= self.env
        

class Sine(Note):
    def __init__(self, params):
        super().__init__(params)
        self.buff = np.sin(2*np.pi*self.buff*frequency/fs)
        self.envelope_exp()

# generate samples, note conversion to float32 array
#samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

note_params = {
    "start": 0.0,
    "duration": 0.2,
    "amplitude": 0.1,
    "attack": 0.1,
    "decay": 0.02,
    "sustain": 1,
    "release": 0.08,
    "envelope": EnvExponential
}
notes = [Sine({**note_params, **{"frequency": freq}}) for freq in [220, 246.94, 277.18, 293.66, 329.63, 369.99, 415.30, 440.0]]

for _ in range(1):
    n = randint(0, len(notes) - 1)
    stream.write(volume*notes[n].buff, len(notes[n].buff))

stream.stop_stream()
stream.close()

p.terminate()
