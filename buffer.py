from param import _Param

class Buffer(_Param):
    param_list = ["sample_rate", "duration"]
    def __init__(self, params):
        super.__init__(params)
    self.env = np.empty(int(self.sample_rate * self.duration)).astype(np.float32)