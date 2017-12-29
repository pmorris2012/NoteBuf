import numpy as np

from param import _Param


class Mixer(_Param):
    def __init__(self, params, *args):
        self._setup_opt_param_list(["amplitude"])
        super().__init__(params)

        self.buff = np.sum(args, axis=0)

        if not self.amplitude == None:
            max_sample = np.max(np.abs(self.buff))
            if max_sample >= self.amplitude:
                self.buff = self.buff * self.amplitude / max_sample

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("amplitude", params):
            self.amplitude = None
        super()._set_opt_param_vals(params)
