import numpy as np

from param import _Param
from oscillator


class SynHarmonic(_Param):
    def __init__(self, params):
        self._setup_param_list(["start", "duration", "amplitude", "frequency", "sample_rate"])
        super().__init__(params)
