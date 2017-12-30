import pyaudio
import random

from param import _Param
from oscillator import OscSine, OscSquare, OscSawtooth, OscTriangle
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
    "duration": 0.2,
    "amplitude": 0.8,
    "attack": 0.01,
    "decay": 0.02,
    "sustain": 0.4,
    "release": 0.08,
    "sample_rate": 44100
}

env = EnvExponential(note_params)
frequencies = [220, 246.94, 277.18, 293.66, 329.63, 369.99, 415.30, 440.0]
waves = [OscSine, OscSquare, OscSawtooth, OscTriangle]

for _ in range(20):
    note1 = random.choice(waves)({**note_params, **{"frequency": random.choice(frequencies)}})
    note2 = random.choice(waves)({**note_params, **{"frequency": random.choice(frequencies)}})
    note3 = random.choice(waves)({**note_params, **{"frequency": random.choice(frequencies)}})
    finalbuff = Mixer(note_params, env.apply(note1.buff), env.apply(note2.buff), env.apply(note3.buff)).buff
    stream.write(volume*finalbuff, len(finalbuff))

stream.stop_stream()
stream.close()

p.terminate()
