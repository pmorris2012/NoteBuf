import numpy as np
import math

from .param import _Param
from .buffer import Buffer
from .synth import SynHarmonic


class _Oscillator(_Param):
    def __init__(self, params):
        self._setup_param_list(["duration", "amplitude", "frequency", "sample_rate"])
        self._setup_opt_param_list(["band_limited"])
        super().__init__(params)
        self.buff = Buffer(params)

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("band_limited", params):
            self.band_limited = True

class OscSine(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff.apply(self.sin)

    def sin(self, x):
        return np.sin(2 * np.pi * x * self.frequency)

class OscSawtooth(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        #self.buff.apply(self.sawtooth)
        N_harmonics = math.floor(self.sample_rate / (2 * self.frequency))
        harm_params = params.copy()
        harm_params["oscillator"] = OscSine
        harm_params["harmonic_vol_list"] = [(math.pow(-1, x) / x) for x in range(1, N_harmonics + 1)]
        self.buff = SynHarmonic(harm_params).buff.apply(lambda x: x * -1)
        
    def sawtooth(self, x):
        N_harmonics = math.floor(self.sample_rate / (2 * self.frequency))
        return (self.amplitude / 2) - (self.amplitude / np.pi) * np.sum([(math.pow(-1, k) * np.sin(2 * np.pi * k * self.frequency * x) / k) for k in range(1, N_harmonics + 1)], axis=0)

class OscTriangle(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff.apply(self.triangle)
    
    def triangle(self, x):
        return 2 * np.abs(np.mod(-0.5 + 2 * x * self.frequency, 2) -1) - 1

class OscSquare(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff.apply(self.square)
        
    def square(self, x):
        N_harmonics = math.floor(self.sample_rate / (2 * self.frequency))
        return (4 / np.pi) * np.sum([(np.sin(2 * np.pi * k * self.frequency * x) / k) for k in range(1, N_harmonics + 1, 2)], axis=0)
