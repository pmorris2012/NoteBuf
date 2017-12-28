import numpy as np

from param import _Param


class _Oscillator(_Param):
    def __init__(self, params):
        self.param_list.extend(["start", "duration", "amplitude", "frequency", "sample_rate"])
        super().__init__(params)
        self.buff = np.arange(int(self.sample_rate * self.duration)).astype(np.float32)
        

class OscSine(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff = np.sin(2 * np.pi * self.buff * self.frequency / self.sample_rate)

class OscSquare(OscSine):
    def __init__(self, params):
        super().__init__(params)
        self.buff = np.sign(self.buff)

class OscSawtooth(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff = np.mod(1 + 2 * self.buff * self.frequency / self.sample_rate, 2) - 1

class OscTriangle(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff = 2 * np.abs(np.mod(-0.5 + 2 * self.buff * self.frequency / self.sample_rate, 2) -1) - 1
