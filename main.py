import pyaudio
import random

from param import _Param
from oscillator import Oscillator
from synth import SynHarmonic
from envelope import EnvLinear, EnvExponential
from effect import EffPitchSlide
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
    "sample_rate": 44100,
    "harmonic_vol_list": [.06, 1, .38, 0, .13, .15, 0, .04, .23, .18, 0, .12]
}

env = EnvExponential(note_params)
frequencies = list(map(lambda x: x/4, [220, 246.94, 277.18, 293.66, 329.63, 369.99, 415.30, 440.0]))
waves = ["sine", "sawtooth", "triangle", "square"]

<<<<<<< HEAD
s = SynHarmonic({**note_params, **{"frequency": EffPitchSlide({**note_params, **{"frequency": random.choice(frequencies)}}).freq, "oscillator": OscSine}})

for _ in range(0):
    note1 = SynHarmonic({**note_params, **{"frequency": random.choice(frequencies), "oscillator": random.choice(waves)}})
    note2 = SynHarmonic({**note_params, **{"frequency": random.choice(frequencies), "oscillator": random.choice(waves)}})
    note3 = SynHarmonic({**note_params, **{"frequency": random.choice(frequencies), "oscillator": random.choice(waves)}})
=======
for _ in range(20):
    note1 = SynHarmonic({**note_params, **{"frequency": random.choice(frequencies), "osc_type": random.choice(waves)}})
    note2 = SynHarmonic({**note_params, **{"frequency": random.choice(frequencies), "osc_type": random.choice(waves)}})
    note3 = SynHarmonic({**note_params, **{"frequency": random.choice(frequencies), "osc_type": random.choice(waves)}})
>>>>>>> master
    finalbuff = Mixer(note_params, env.apply(note1.buff), env.apply(note2.buff), env.apply(note3.buff)).buff
    stream.write(volume*finalbuff, len(finalbuff))

stream.stop_stream()
stream.close()

p.terminate()
