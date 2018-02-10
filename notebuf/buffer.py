import numpy as np
import math
from decimal import Decimal

from .param import _Param


class Buffer(_Param):
    def __init__(self, params, buff=None):
        self._setup_param_list(["duration", "sample_rate"])
        self._setup_opt_param_list(["start"])
        super().__init__(params)

        if not isinstance(buff, np.ndarray):
            self.buff = np.arange(int(Decimal(self.sample_rate) * Decimal(self.duration)), dtype=np.float64) / self.sample_rate
        else:
            self.buff = buff

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("start", params):
            self.start = 0
        super()._set_opt_param_vals(params)

    def apply(self, fn):
        self.buff = fn(self.buff)
        return self

    def __getitem__(self, key):
        return self.buff[key]
    
    def __setitem__(self, key, value):
        self.buff[key] = value

    def __repr__(self):
        return 'Buffer({})'.format(self.buff)
