import random
import numpy as np

from notebuf.oscillator import OscSine, OscSquare, OscSawtooth, OscTriangle
from notebuf.envelope import EnvExponential
from notebuf.synth import SynHarmonic
from notebuf.mixer import MonoMixer, StereoMixer
from notebuf.player import Player
from notebuf.filter import LowPass, HighPass, BandPass, BandStop
from notebuf.param import ParamGroup

def test_synth_sub():
    params = ParamGroup({
        "duration": .08,
        "sample_rate": 44100 })
    
    player = Player(params)

    env_params = params.copy_with({
        "amplitude": 1,
        "attack": 0.02,
        "decay": 0.01,
        "sustain": 0.6,
        "release": 0.03 })

    filt_params = params.copy_with({
        "lowcut": 1000,
        "highcut": 2000 })

    filt_params2 = params.copy_with({
        "highcut": 3000 })

    mix_params = ParamGroup({"amplitude": 0.7})

    beat_params = params.copy_with({
        "duration": .07,
        "amplitude": 1,
        "frequency": 30 })

    beat_env_params = beat_params.copy_with({
        "amplitude": 1,
        "attack": 0,
        "decay": 0.03,
        "sustain": 0.1,
        "release": 0.01 })

    beat_filt_params = beat_params.copy_with({
        "lowcut": 300,
        "highcut": 800 })

    beat_filt_params2 = beat_params.copy_with({
        "lowcut": 1200,
        "highcut": 10000 })

    def apply(buff):
        BandStop(filt_params).apply(buff)
        LowPass(filt_params2).apply(buff)
        EnvExponential(env_params).apply(buff)
        return buff

    def beat_apply(buff):
        BandStop(beat_filt_params).apply(buff)
        BandStop(beat_filt_params2).apply(buff)
        EnvExponential(beat_env_params).apply(buff)
        return buff

    beats = [beat_apply(OscSquare(beat_params).buff)]
    for i in range(1, 8):
        beats.append(beats[0].copy({"start": i * 0.40}))

    buffs1, buffs2 = [], []
    for i in range(32):
        i_params = params.copy_with({
            "start": 0.025 + i * 0.10,
            "amplitude": 1 - (i / 64),
            "frequency": 860 - (i * 2),
            "pan": 0.45 })

        buffs1.append(apply(OscSawtooth(i_params).buff))

    for i in range(32):
        i_params = params.copy_with({
            "start": i * 0.10,
            "amplitude": 1 - (i / 64),
            "frequency": 220 + (i * i * 2),
            "pan": 0.55 })

        buffs2.append(apply(OscSawtooth(i_params).buff))

    sm = StereoMixer(mix_params)

    lbuff_beat, rbuff_beat = sm.mix(*beats)

    lbuff, rbuff = sm.mix(*buffs1, *buffs2)

    lbuff, rbuff = sm.mix(lbuff, rbuff, lbuff_beat, rbuff_beat)

    buffs = [lbuff, rbuff]
    for i in range(1, 8):
        buffs.append(lbuff.copy({"start": lbuff.duration * i}))
        buffs.append(rbuff.copy({"start": rbuff.duration * i}))
    
    lbuff, rbuff = sm.mix(*buffs)

    player.write(lbuff, rbuff)
    player.wait()
