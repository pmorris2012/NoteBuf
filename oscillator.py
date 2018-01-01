import numpy as np

from param import _Param


class Oscillator(_Param):
    def __init__(self, params):
        self._setup_param_list(["osc_type", "start", "duration", "amplitude", "frequency", "sample_rate"])
        self._setup_opt_param_list(["duty_cycle"])
        super().__init__(params)
        self.buff = np.arange(int(self.sample_rate * self.duration)).astype(np.float32)
        self.buff = getattr(self, "fn_" + self.osc_type)(self.buff)

    def fn_sine(self, buff):
        return np.sin(2 * np.pi * buff * self.frequency / self.sample_rate)

    def fn_sawtooth(self, buff):
        return np.mod(1 + 2 * buff * self.frequency / self.sample_rate, 2) - 1

    def fn_triangle(self, buff):
        return 2 * np.abs(np.mod(-0.5 + 2 * buff * self.frequency / self.sample_rate, 2) -1) - 1

    def fn_square(self, buff):
        assert self.duty_cycle >= 0 and self.duty_cycle <= 1
        return np.sign(self.fn_sawtooth(buff) + 1 - 2 * self.duty_cycle)

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("duty_cycle", params):
            self.duty_cycle = 0.5
        super()._set_opt_param_vals(params)
