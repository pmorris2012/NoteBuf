from .param import _Param

class LowPass(_Param):
    def __init__(self, params):
        self._setup_param_list([])
        super().__init__(params)

        
    def apply(self, x):
        x[1:] += x[:-1]
        return x
