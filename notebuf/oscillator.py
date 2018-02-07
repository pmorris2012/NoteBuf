import numpy as np
import math

from .param import _Param
from .buffer import Buffer
from .synth import SynHarmonic


class _Oscillator(_Param):
    def __init__(self, params):
        self._setup_param_list(["duration", "amplitude", "frequency", "sample_rate"])
        self._setup_opt_param_list(["band_limited", "sigma_approx", "sigma_approx_min_harmonics"])
        super().__init__(params)
        self.buff = Buffer(params)

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("band_limited", params):
            self.band_limited = True
        if not self._is_opt_param_set("sigma_approx", params):
            self.sigma_approx = True
        if not self._is_opt_param_set("sigma_approx_min_harmonics", params):
            self.sigma_approx_min_harmonics = 4

    def _fn(self, x):
        return x

    def _band_limited_fn(self, x):
        return self._fn(x)

    def fn(self, x):
        return self.amplitude * self._get_fn()(x)

    def _check_sigma(self):
        return self.sigma_approx and self._get_n_harmonics() >= self.sigma_approx_min_harmonics

    def _get_n_harmonics(self):
        return math.floor(self.sample_rate / (2 * self.frequency))

    def _get_fn(self):
        return self._band_limited_fn if self.band_limited else self._fn

class OscSine(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff.apply(self.fn)

    def _fn(self, x):
        return np.sin(2 * np.pi * x * self.frequency)

class OscSawtooth(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff.apply(self.fn)
        
    def _fn(self, x):
        return np.mod(1 + 2 * x * self.frequency, 2) - 1

    def _band_limited_fn(self, x):
        harm_params = self.params.copy()
        harm_params["oscillator"] = OscSine

        if self._check_sigma():
            harm_params["harmonic_vol_list"] = [(math.pow(-1, x) / x) for x in range(1, self._get_n_harmonics() + 1)]
        else:
            harm_params["harmonic_vol_list"] = [(math.pow(-1, x) / x) for x in range(1, self._get_n_harmonics() + 1)]
        
        return SynHarmonic(harm_params).buff.apply(lambda x: x * -1).buff

class OscTriangle(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff.apply(self.fn)
    
    def _fn(self, x):
        return 2 * np.abs(np.mod(-0.5 + 2 * x * self.frequency, 2) -1) - 1

class OscSquare(_Oscillator):
    def __init__(self, params):
        self._setup_opt_param_list(["duty_cycle"])
        super().__init__(params)

        assert self.duty_cycle >= 0 and self.duty_cycle <= 1
        self.buff.apply(self.fn)

    def _fn(self, x):
        return np.sign(np.mod(1 + 2 * x * self.frequency, 2) - 2 * self.duty_cycle)
        
    def _band_limited_fn(self, x):
        N_harmonics = math.floor(self.sample_rate / (2 * self.frequency))
        return (4 / np.pi) * np.sum([(np.sin(2 * np.pi * k * self.frequency * x) / k) for k in range(1, N_harmonics + 1, 2)], axis=0)

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("duty_cycle", params):
            self.duty_cycle = 0.5
        super()._set_opt_param_vals(params)
