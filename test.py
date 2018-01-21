import pyaudio
import numpy as np

p = pyaudio.PyAudio()

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True)

dt = 1./44100
time = np.linspace(0., 10., 10*44100, dtype=np.float32)
f = 440. + 100*time/6  # a 1Hz oscillation
delta_phase = f * dt
phase = np.cumsum(delta_phase)  # add up the phase differences along timeline (same as np.add.accumulate)
wav = np.sin(2 * np.pi * phase)

print((time[1:] - time[:-1]).min())

stream.write(wav * 0.5, len(wav))
