import numpy as np

from .param import _Param
from .buffer import Buffer


class _Oscillator(_Param):
    def __init__(self, params):
        self._setup_param_list(["duration", "amplitude", "frequency", "sample_rate"])
        super().__init__(params)
        self.buff = Buffer(params)
        

class OscSine(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff.apply(self.sin)

    def sin(self, x):
        return np.sin(2 * np.pi * x * self.frequency / self.sample_rate)

class OscSawtooth(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff.apply(self.sawtooth)
        
    def sawtooth(self, x):
        return np.mod(1 + 2 * x * self.frequency / self.sample_rate, 2) - 1

class OscTriangle(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff.apply(self.triangle)
    
    def triangle(self, x):
        return 2 * np.abs(np.mod(-0.5 + 2 * x * self.frequency / self.sample_rate, 2) -1) - 1

class OscSquare(OscSawtooth, _Param):
    def __init__(self, params):
        self._setup_opt_param_list(["duty_cycle"])
        super().__init__(params)
        
        assert self.duty_cycle >= 0 and self.duty_cycle <= 1
        self.buff.apply(self.square) 
        
    def square(self, x):
        return np.sign(x + 1 - 2 * self.duty_cycle)

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("duty_cycle", params):
            self.duty_cycle = 0.5
        super()._set_opt_param_vals(params)
