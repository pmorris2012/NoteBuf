import pyaudio
from random import randint

from param import _Param
from oscillator import OscSine, OscSquare, OscSawtooth, OscTriangle
from envelope import EnvLinear, EnvExponential


p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]


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
    "exp_factor": .623
}

env = EnvExponential(note_params)
notes = [OscTriangle({**note_params, **{"frequency": freq}}) for freq in map(lambda x: x, [220, 246.94, 277.18, 293.66, 329.63, 369.99, 415.30, 440.0])]
for note in notes:
    env.apply(note.buff)

for _ in range(20):
    n = randint(0, len(notes) - 1)
    stream.write(volume*notes[n].buff, len(notes[n].buff))

stream.stop_stream()
stream.close()

p.terminate()
