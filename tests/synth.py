import random
import numpy as np

from notebuf.oscillator import OscSine, OscSquare, OscSawtooth, OscTriangle
from notebuf.envelope import EnvExponential
from notebuf.synth import SynHarmonic
from notebuf.mixer import Mixer
from notebuf.player import Player

def test_osc_bandl():
    player = Player({ "sample_rate": 44100 })

    note_params = {
        "start": 0.0,
        "duration": .5,
        "amplitude": 1,
        "sample_rate": 44100,
        "frequency": 100,
        "band_limited": False
    }

    env_params = {
        "duration": .5,
        "amplitude": 0.8,
        "sample_rate": 44100,
        "attack": 0.01,
        "decay": 0.02,
        "sustain": 0.4,
        "release": 0.08,
    }

    env = EnvExponential(env_params)
    note1 = OscSquare(note_params)
    print(note1.buff.buff.max())
    player.write(env.apply(note1.buff))

def test_synth_1():
    player = Player({ "sample_rate": 44100 })

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
    frequencies = list(map(lambda x: x/2, [220, 246.94, 277.18, 293.66, 329.63, 369.99, 415.30, 440.0]))
    waves = [OscSine, OscSquare, OscSawtooth, OscTriangle]

    for _ in range(20):
        note1 = SynHarmonic({**note_params, **{"frequency": random.choice(frequencies), "oscillator": random.choice(waves)}})
        note2 = SynHarmonic({**note_params, **{"frequency": random.choice(frequencies), "oscillator": random.choice(waves)}})
        note3 = SynHarmonic({**note_params, **{"frequency": random.choice(frequencies), "oscillator": random.choice(waves)}})
        finalbuff = Mixer(note_params, env.apply(note1.buff), env.apply(note2.buff), env.apply(note3.buff))
        player.write(finalbuff)

def test_synth_2():
    player = Player({ "sample_rate": 44100 })

    note_params = {
        "amplitude": 0.7,
        "attack": 0.06,
        "decay": 0.08,
        "sustain": 0.6,
        "release": 0.04,
        "sample_rate": 44100,
        "harmonic_vol_list": [1, .8, .82, .6, .4, .2, .1, .02]
    }

    env1 = EnvExponential({**note_params, **{"duration": 0.6}})
    env2 = EnvExponential({**note_params, **{"duration": 0.4}})
    env3 = EnvExponential({**note_params, **{"duration": 0.2}})

    start_freq = 220
    steps1 = [ 0, -5, 7, 14]
    steps2 = [ 0, -1, -3, 19, -7]
    steps3 = [ 0,  4, 11, 16, 14, 12]

    freq_shift = lambda x, y: x * (2 ** (y / 12))

    buffs = []
    for _ in range(60):
        note1 = SynHarmonic({**note_params, **{"frequency": freq_shift(start_freq, steps1[_ % len(steps1)]), "oscillator": OscSine, "start": 0.0, "duration":0.6}})
        note2 = SynHarmonic({**note_params, **{"frequency": freq_shift(start_freq, steps2[_ % len(steps2)]), "oscillator": OscSine, "start": 0.2, "duration":0.4}})
        note3 = SynHarmonic({**note_params, **{"frequency": freq_shift(start_freq, steps3[_ % len(steps3)]), "oscillator": OscSine, "start": 0.4, "duration":0.2}})
        buffs.append(Mixer({**note_params, **{"start": 0.6 * _}}).mix(env1.apply(note1.buff), env2.apply(note2.buff), env3.apply(note3.buff)))
    finalbuff = Mixer({}).mix(*buffs)
    player.write(finalbuff)
