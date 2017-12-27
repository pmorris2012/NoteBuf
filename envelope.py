import numpy as np
import math

from param import _Param


class EnvExponential(_Param):
    param_list = ["duration", "amplitude", "sample_rate"]
    opt_param_list = ["attack", "decay", "sustain", "release", "exp_factor"]

    def __init__(self, params):
        super().__init__(params)

        assert self.attack + self.decay + self.release < self.duration or math.isclose(self.attack + self.decay + self.release, self.duration)
        
        self.env = np.empty(int(self.sample_rate * self.duration)).astype(np.float32)

        a = int(self.attack * self.sample_rate)
        _d = int(self.decay * self.sample_rate)
        d = int((self.attack+self.decay) * self.sample_rate)
        s = int((self.duration-self.release) * self.sample_rate)
        r = int(self.release * self.sample_rate)

        self.env[:a] = self._env_exp(np.linspace(0.0, self.attack, a), 0.0, self.amplitude, 0.0, self.attack)
        self.env[a:d] = self._env_exp(np.linspace(self.attack, self.attack + self.decay, _d), self.amplitude, self.sustain, self.attack, self.attack + self.decay)
        self.env[d:s] = self.sustain
        self.env[s:] = self._env_exp(np.linspace(self.duration - self.release, self.duration, r), self.sustain, 0.0, self.duration - self.release, self.duration)

    def _set_opt_param_vals(self, params):
        if not "attack" in params:
            self.attack = 0.1 * params["duration"]
        if not "decay" in params:
            self.decay = 0.1 * params["duration"]
        if not "sustain" in params:
            self.sustain = params["amplitude"]
        if not "release" in params:
            self.release = 0.1 * params["duration"]
        if not "exp_factor" in params:
            self.exp_factor = 0.326

    def apply(self, buffer):
        assert buffer.size == self.env.size
        buffer *= self.env

    def _env_exp(self, x, a0, a1, t0, t1):
        assert self.exp_factor > 0 and self.exp_factor <= 1
        assert a0 >= 0 and a0 <= 1
        assert a1 >= 0 and a1 <= 1
        assert t0 >= 0 and t1 > 0

        #magic gradual start term dissapear factor
        #   -too large = start not gradual enough
        #   -too small = does not reach a1 by t1
        #g = 5

        #m = (x - t0) / (b * (t1 - t0))
        #n = (1-b) * np.exp(-g * (x - t0) / b)

        #gradual start term - starts at linear envelope slope near t0 - causes clipping
        #d = n * m * (a1 - a0) / np.exp(m)

        return (a0 - a1) * np.power(1 - (x - t0) / (t1 - t0), 1 / self.exp_factor) + a1


class EnvLinear(_Param):
    param_list = ["duration", "amplitude", "sample_rate"]
    opt_param_list = ["attack", "decay", "sustain", "release"]

    def __init__(self, params):
        super().__init__(params)

        assert self.attack + self.decay + self.release < self.duration or math.isclose(self.attack + self.decay + self.release, self.duration)
        
        self.env = np.empty(int(self.sample_rate * self.duration)).astype(np.float32)

        a = int(self.attack * self.sample_rate)
        _d = int(self.decay * self.sample_rate)
        d = int((self.attack+self.decay) * self.sample_rate)
        s = int((self.duration-self.release) * self.sample_rate)
        r = int(self.release * self.sample_rate)

        self.env[:a] = np.linspace(0.0, self.amplitude, a)
        self.env[a:d] = np.linspace(self.amplitude, self.sustain, _d)
        self.env[d:s] = self.sustain
        self.env[s:] = np.linspace(self.sustain, 0.0, r)

    def _set_opt_param_vals(self, params):
        if not "attack" in params:
            self.attack = 0.1 * params["duration"]
        if not "decay" in params:
            self.decay = 0.1 * params["duration"]
        if not "sustain" in params:
            self.sustain = params["amplitude"]
        if not "release" in params:
            self.release = 0.1 * params["duration"]

    def apply(self, buffer):
        assert buffer.size == self.env.size
        buffer *= self.env
