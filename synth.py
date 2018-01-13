import numpy as np

from param import _Param
from oscillator import *
from mixer import Mixer


class SynHarmonic(_Param):
    def __init__(self, params):
        self._setup_param_list(["start", "duration", "amplitude", "frequency", "sample_rate", "oscillator"])
        self._setup_opt_param_list(["harmonic_vol_list", "frequency_shift"])
        super().__init__(params)


        harmonics = []
        freq = self.frequency
        shift_ratio = self.frequency_shift / freq
        for volume in self.harmonic_vol_list:
            harm_params = params.copy()
            harm_params["frequency"] = freq
            harm_params["frequency_shift"] = shift_ratio * freq
            harmonics.append(self.oscillator(harm_params).buff * volume)
            freq += self.frequency
            if freq > self.sample_rate / 2:
                break

        self.buff = Mixer(params, *harmonics).buff

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("harmonic_vol_list", params):
            self.harmonic_vol_list = [1 / x for x in range(1, int(self.sample_rate / (2 * self.frequency)) + 1)]
        if not self._is_opt_param_set("frequency_shift", params):
            self.frequency_shift = 0
        super()._set_opt_param_vals(params)
