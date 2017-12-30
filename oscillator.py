import numpy as np

from param import _Param


class _Oscillator(_Param):
    def __init__(self, params):
        self._setup_param_list(["start", "duration", "amplitude", "frequency", "sample_rate"])
        super().__init__(params)
        self.buff = np.arange(int(self.sample_rate * self.duration)).astype(np.float32)
        

class OscSine(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff = np.sin(2 * np.pi * self.buff * self.frequency / self.sample_rate)

class OscSawtooth(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff = np.mod(1 + 2 * self.buff * self.frequency / self.sample_rate, 2) - 1

class OscTriangle(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff = 2 * np.abs(np.mod(-0.5 + 2 * self.buff * self.frequency / self.sample_rate, 2) -1) - 1

class OscSquare(OscSawtooth, _Param):
    def __init__(self, params):
        self._setup_opt_param_list(["duty_cycle"])
        super().__init__(params)
        
        assert self.duty_cycle >= 0 and self.duty_cycle <= 1
        self.buff = np.sign(self.buff + 1 - 2 * self.duty_cycle)

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("duty_cycle", params):
            self.duty_cycle = 0.5
        super()._set_opt_param_vals(params)
