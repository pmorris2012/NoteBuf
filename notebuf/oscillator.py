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

    def fn(self, x):
        return self.amplitude * x

    def band_limited_fn(self, x):
        return self.amplitude * self.fn(x)

    def _check_sigma(self):
        return self.sigma_approx and self._get_n_harmonics() >= self.sigma_approx_min_harmonics

    def _get_n_harmonics(self):
        return math.floor(self.sample_rate / (2 * self.frequency))

    def _get_fn(self):
        return self.band_limited_fn if self.band_limited else self.fn

class OscSine(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff.apply(self._get_fn())

    def fn(self, x):
        return self.amplitude * np.sin(2 * np.pi * x * self.frequency)

class OscSawtooth(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff.apply(self._get_fn())
        
    def fn(self, x):
        return self.amplitude * np.mod(1 + 2 * x * self.frequency, 2) - 1

    def band_limited_fn(self, x):
        harm_params = self.params.copy()
        harm_params["oscillator"] = OscSine

        if self._check_sigma():
            l = self._get_n_harmonics()
            sigmas = [np.sin(n * np.pi / l) / (n * np.pi / l) for n in range(1, l + 1)]
            harm_params["harmonic_vol_list"] = [sigma / (i + 1) for i, sigma in enumerate(sigmas)]
        else:
            harm_params["harmonic_vol_list"] = [1 / x for x in range(1, self._get_n_harmonics() + 1)]
        
        return self.amplitude * SynHarmonic(harm_params).buff.apply(lambda x: x * -1).buff

class OscTriangle(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff.apply(self._get_fn())
    
    def fn(self, x):
        return self.amplitude * 2 * np.abs(np.mod(-0.5 + 2 * x * self.frequency, 2) -1) - 1

    def band_limited_fn(self, x):
        harm_params = self.params.copy()
        harm_params["oscillator"] = OscSine
        harm_params["harmonic_vol_list"] = [(0 if x % 2 == 0 else (math.pow(-1, (x-1)/2) / (x * x))) for x in range(1, self._get_n_harmonics() + 1)]
        
        return self.amplitude * SynHarmonic(harm_params).buff.buff

class OscSquare(_Oscillator):
    def __init__(self, params):
        self._setup_opt_param_list(["duty_cycle"])
        super().__init__(params)

        assert self.duty_cycle >= 0 and self.duty_cycle <= 1
        self.buff.apply(self._get_fn())

    def fn(self, x):
        return self.amplitude * np.sign(np.mod(1 + 2 * x * self.frequency, 2) - 2 * self.duty_cycle)
        
    def band_limited_fn(self, x):
        harm_params = self.params.copy()
        harm_params["oscillator"] = OscSine

        if self._check_sigma():
            l = self._get_n_harmonics()
            sigmas = [(0 if n % 2 == 0 else (np.sin(n * np.pi / l) / (n * np.pi / l))) for n in range(1, l + 1)]
            harm_params["harmonic_vol_list"] = [sigma / (i + 1) for i, sigma in enumerate(sigmas)]
        else:
            harm_params["harmonic_vol_list"] = [(0 if x % 2 == 0 else (1 / x)) for x in range(1, self._get_n_harmonics() + 1)]
        
        return self.amplitude * SynHarmonic(harm_params).buff.buff

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("duty_cycle", params):
            self.duty_cycle = 0.5
        super()._set_opt_param_vals(params)
