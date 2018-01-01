import numpy as np

from param import _Param


class Oscillator(_Param):
    def __init__(self, params):
        self._setup_param_list(["osc_type", "start", "duration", "amplitude", "frequency", "sample_rate"])
        self._setup_opt_param_list(["duty_cycle", "frequency_shift", "slide_start", "slide_duration"])
        super().__init__(params)

        if self.frequency_shift != 0:
            assert self.slide_start + self.slide_duration < self.duration

            freqbuff = np.empty(int(self.sample_rate * self.duration)).astype(np.float32)

            start = int(self.slide_start * self.sample_rate)
            end = int((self.slide_start + self.slide_duration) * self.sample_rate)

            freqbuff[:start] = self.frequency
            freqbuff[start:end] = np.linspace(self.frequency, self.frequency + self.frequency_shift, end - start)
            freqbuff[end:] = self.frequency + self.frequency_shift

            self.frequency = freqbuff

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
        if not self._is_opt_param_set("frequency_shift", params):
            self.frequency_shift = 0
        if not self._is_opt_param_set("slide_start", params):
            self.slide_start = 0
        if not self._is_opt_param_set("slide_duration", params):
            self.slide_duration = self.duration * 0.1
        super()._set_opt_param_vals(params)
