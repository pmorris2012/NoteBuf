import numpy as np
import math
from decimal import Decimal

from .param import _Param
from .buffer import Buffer


class StereoMixer(_Param):
    def __init__(self, params):
        self._setup_opt_param_list(["start", "amplitude"])
        super().__init__(params)

    def mix(self, *args):
        start = min([x.start for x in args])
        duration = max([x.start + x.duration for x in args]) - start
        sample_rate = args[0].sample_rate
        lbuff = Buffer(self.params.copy_with({
            "start": self.start + start,
            "duration": duration,
            "sample_rate": sample_rate,
            "pan": 0
        }))
        lbuff.apply(lambda x: x * 0)

        rbuff = Buffer(self.params.copy_with({
            "start": self.start + start,
            "duration": duration,
            "sample_rate": sample_rate,
            "pan": 1
        }))
        rbuff.apply(lambda x: x * 0)

        for _buff in args:
            _start = int(Decimal(_buff.start) * Decimal(sample_rate))
            _end = _start + int(Decimal(_buff.duration) * Decimal(sample_rate))

            def _mix(x, pan):
                x[_start:_end] += _buff.buff * pan
                return x

            lpan = min(-1, -2 * _buff.pan) + 2
            rpan = min(1, 2 * _buff.pan)

            lbuff.apply(_mix, lpan)
            rbuff.apply(_mix, rpan)

        scale = self._calc_scale(lbuff, rbuff)
        lbuff.apply(self.scale, scale)
        rbuff.apply(self.scale, scale)

        return lbuff, rbuff

    def _calc_scale(self, lbuff, rbuff):
        scale = 1
        if not self.amplitude == None:
            max_sample = max(np.max(np.abs(lbuff.buff)), np.max(np.abs(rbuff.buff)))
            
            if max_sample != 0:
                scale = self.amplitude / max_sample
                
        return scale

    def scale(self, x, factor):
        x *= factor
        return x

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("amplitude", params):
            self.amplitude = None
        if not self._is_opt_param_set("start", params):
            self.start = 0
        super()._set_opt_param_vals(params)

class MonoMixer(StereoMixer):
    def mix(self, *args):
        lbuff, rbuff = super().mix(*args)
        
        start = min([x.start for x in args])
        duration = max([x.start + x.duration for x in args]) - start
        sample_rate = args[0].sample_rate
        pan = args[0].pan
        buff = Buffer(self.params.copy_with({
            "start": self.start + start,
            "duration": duration,
            "sample_rate": sample_rate
        }))
        buff.apply(lambda x: (lbuff.buff + rbuff.buff) / 2)

        return buff
