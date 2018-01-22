import numpy as np
import math

from .param import _Param
from .buffer import Buffer


class _Envelope(_Param):
    def __init__(self, params):
        self._setup_param_list(["duration", "amplitude", "sample_rate"])
        self._setup_opt_param_list(["attack", "decay", "sustain", "release"])
        super().__init__(params)
        assert self.attack + self.decay + self.release < self.duration or math.isclose(self.attack + self.decay + self.release, self.duration)
        
        self.env = Buffer(params)

        self.a = int(self.attack * self.sample_rate)
        self._d = int(self.decay * self.sample_rate)
        self.d = self.a + self._d
        self.r = int(self.release * self.sample_rate)
        self._s = int((self.duration * self.sample_rate) - self.a - self._d - self.r)
        self.s = self._s + self._d + self.a
    
    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("attack", params):
            self.attack = 0.1 * params["duration"]
        if not self._is_opt_param_set("decay", params):
            self.decay = 0.1 * params["duration"]
        if not self._is_opt_param_set("sustain", params):
            self.sustain = params["amplitude"]
        if not self._is_opt_param_set("release", params):
            self.release = 0.1 * params["duration"]
        super()._set_opt_param_vals(params)

    def shape(self, x):
        return x

    def apply(self, buffer):
        buffer.apply(self._apply)
        return buffer

    def _apply(self, x):
        assert x.size == self.env.buff.size
        return x * self.env.buff


class EnvExponential(_Envelope, _Param):
    def __init__(self, params):
        self._setup_opt_param_list(["exp_factor"])
        super().__init__(params)

        self.env.apply(self.shape)

    def shape(self, x):
        x[:self.a] = self._env_exp(np.linspace(0.0, self.attack, self.a), 0.0, self.amplitude, 0.0, self.attack)
        x[self.a:self.d] = self._env_exp(np.linspace(self.attack, self.attack + self.decay, self._d), self.amplitude, self.sustain, self.attack, self.attack + self.decay)
        x[self.d:self.s] = self.sustain
        x[self.s:] = self._env_exp(np.linspace(self.duration - self.release, self.duration, self.r), self.sustain, 0.0, self.duration - self.release, self.duration)
        return x

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("exp_factor", params):
            self.exp_factor = 0.623
        super()._set_opt_param_vals(params)

    def _env_exp(self, x, a0, a1, t0, t1):
        assert self.exp_factor > 0 and self.exp_factor <= 1
        assert a0 >= 0 and a0 <= 1
        assert a1 >= 0 and a1 <= 1
        assert t0 >= 0 and t1 >= 0

        return (a0 - a1) * np.power(1 - (x - t0) / (t1 - t0), 1 / self.exp_factor) + a1


class EnvLinear(_Envelope):
    def __init__(self, params):
        super().__init__(params)

        self.env.apply(self.shape)

    def shape(self, x):
        x[:a] = np.linspace(0.0, self.amplitude, a)
        x[a:d] = np.linspace(self.amplitude, self.sustain, _d)
        x[d:s] = self.sustain
        x[s:] = np.linspace(self.sustain, 0.0, r)
        return x
