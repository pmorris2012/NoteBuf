import numpy as np

from .param import _Param
from .buffer import Buffer


class Mixer(_Param):
    def __init__(self, params):
        self._setup_opt_param_list(["amplitude"])
        super().__init__(params)

    def mix(self, *args):
        buff = Buffer({
            "start": min([x.start for x in args]),
            "duration": max([x.start + x.duration for x in args]) - min([x.start for x in args]),
            "sample_rate": args[0].sample_rate
        }, buff=np.sum([x.buff for x in args], axis=0))

        buff.apply(self.scale)
        return buff

    def scale(self, x):
        if not self.amplitude == None:
            max_sample = np.max(np.abs(x))
            if max_sample >= self.amplitude:
                x *= self.amplitude / max_sample
        return x

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("amplitude", params):
            self.amplitude = None
        super()._set_opt_param_vals(params)
