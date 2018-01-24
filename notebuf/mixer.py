import numpy as np

from .param import _Param
from .buffer import Buffer


class Mixer(_Param):
    def __init__(self, params):
        self._setup_opt_param_list(["start", "amplitude"])
        super().__init__(params)

    def mix(self, *args):
        start = min([x.start for x in args])
        duration = max([x.start + x.duration for x in args]) - start
        sample_rate = args[0].sample_rate
        buff = Buffer({
            "start": self.start + start,
            "duration": duration,
            "sample_rate": sample_rate
        })
        buff.apply(lambda x: x * 0)

        for _buff in args:
            _start = int(_buff.start * sample_rate)
            _end = _start + int(_buff.duration * sample_rate)

            def _mix(x):
                x[_start:_end] += _buff.buff
                return x

            buff.apply(_mix)

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
        if not self._is_opt_param_set("start", params):
            self.start = 0
        super()._set_opt_param_vals(params)
