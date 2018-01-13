import pyaudio
import random

from param import _Param
from oscillator import OscSine, OscSquare, OscSawtooth, OscTriangle
from synth import SynHarmonic
from envelope import EnvLinear, EnvExponential
from mixer import Mixer


p = pyaudio.PyAudio()

volume = 1     # range [0.0, 1.0]


# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True)

note_params = {
    "start": 0.0,
    "duration": 2,
    "amplitude": 0.8,
    "attack": 0.01,
    "decay": 0.02,
    "sustain": 0.4,
    "release": 0.08,
    "sample_rate": 44100,
    "harmonic_vol_list": [.06, 1, .38, 0, .13, .15, 0, .04, .23, .18, 0, .12]
}

env = EnvExponential(note_params)
frequencies = list(map(lambda x: x, [220, 246.94, 277.18, 293.66, 329.63, 369.99, 415.30, 440.0]))
waves = [OscSine]#, OscSquare, OscSawtooth, OscTriangle]

params = {**note_params, **{"frequency": 220, "oscillator": OscSine}}
params["frequency_shift"] = 10
params["slide_start"] = 0.5
params["slide_duration"] = .5
s = SynHarmonic(params)
stream.write(volume*env.apply(s.buff), len(s.buff))

for _ in range(0):
    note1 = SynHarmonic({**note_params, **{"frequency": random.choice(frequencies), "oscillator": random.choice(waves)}})
    note2 = SynHarmonic({**note_params, **{"frequency": random.choice(frequencies), "oscillator": random.choice(waves)}})
    note3 = SynHarmonic({**note_params, **{"frequency": random.choice(frequencies), "oscillator": random.choice(waves)}})
    finalbuff = Mixer(note_params, env.apply(note1.buff), env.apply(note2.buff), env.apply(note3.buff)).buff
    stream.write(volume*finalbuff, len(finalbuff))

stream.stop_stream()
stream.close()

p.terminate()
