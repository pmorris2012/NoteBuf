import numpy as np

from .param import _Param


class Buffer(_Param):
    def __init__(self, params, buff=None):
        self._setup_param_list(["duration", "sample_rate"])
        self._setup_opt_param_list(["start"])
        super().__init__(params)

        if not isinstance(buff, np.ndarray):
            self.buff = np.arange(int(self.sample_rate * self.duration), dtype=np.float32)
        else:
            self.buff = buff

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("start", params):
            self.start = 0
        super()._set_opt_param_vals(params)

    def apply(self, fn):
        self.buff = fn(self.buff)
        return self