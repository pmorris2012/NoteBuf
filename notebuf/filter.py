import numpy as np
from scipy.signal import butter, sosfilt

from .param import _Param

class LowPass(_Param):
    def __init__(self, params):
        self._setup_param_list(["highcut", "sample_rate"])
        self._setup_opt_param_list(["order"])
        super().__init__(params)
        self.pass_type = 'low'
        
    def apply(self, buffer):
        buffer.apply(self._apply)
        return buffer

    def _apply(self, x):
        sos = butter(self.order, [self.highcut * 2 / self.sample_rate], btype=self.pass_type, output='sos')
        x = sosfilt(sos, x)
        return x

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("order", params):
            self.order = 6
        super()._set_opt_param_vals(params)

class HighPass(_Param):
    def __init__(self, params):
        self._setup_param_list(["lowcut", "sample_rate"])
        self._setup_opt_param_list(["order"])
        super().__init__(params)
        self.pass_type = 'high'
        
    def apply(self, buffer):
        buffer.apply(self._apply)
        return buffer

    def _apply(self, x):
        sos = butter(self.order, [self.lowcut * 2 / self.sample_rate], btype=self.pass_type, output='sos')
        x = sosfilt(sos, x)
        return x

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("order", params):
            self.order = 6
        super()._set_opt_param_vals(params)

class BandPass(_Param):
    def __init__(self, params):
        self._setup_param_list(["lowcut", "highcut", "sample_rate"])
        self._setup_opt_param_list(["order"])
        super().__init__(params)
        self.pass_type = 'band'
        
    def apply(self, buffer):
        buffer.apply(self._apply)
        return buffer

    def _apply(self, x):
        nyquist = self.sample_rate * 0.5
        sos = butter(self.order, [self.lowcut / nyquist, self.highcut / nyquist], btype=self.pass_type, output='sos')
        x = sosfilt(sos, x)
        return x

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("order", params):
            self.order = 6
        super()._set_opt_param_vals(params)

class BandStop(BandPass):
    def __init__(self, params):
        super().__init__(params)
        self.pass_type = 'bandstop'
