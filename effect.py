import numpy as np

from param import _Param


class EffPitchSlide(_Param):
    def __init__(self, params):
        self._setup_param_list(["duration", "frequency", "sample_rate"])
        self._setup_opt_param_list(["frequency_end", "slide_start", "slide_duration"])
        super().__init__(params)

        self.freq = np.empty(int(self.sample_rate * self.duration)).astype(np.float32)

        assert self.slide_start + self.slide_duration < self.duration

        start = int(self.slide_start * self.sample_rate)
        end = int((self.slide_start + self.slide_duration) * self.sample_rate)

        self.freq[:start] = self.frequency
        self.freq[start:end] = np.linspace(self.frequency, self.frequency_end, end - start)
        self.freq[end:] = self.frequency_end


    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("frequency_end", params):
            self.frequency_end = min(self.frequency * 1.05, self.sample_rate / 2)
        if not self._is_opt_param_set("slide_start", params):
            self.slide_start = 0
        if not self._is_opt_param_set("slide_duration", params):
            self.slide_duration = self.duration * 0.1
