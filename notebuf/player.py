import sounddevice as sd
import numpy as np
import time
from threading import Thread

from .param import _Param

class Player(_Param):
    def __init__(self, params):
        self._setup_param_list(["sample_rate"])
        self._setup_opt_param_list(["volume"])
        super().__init__(params)

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("volume", params):
            self.volume = 1
        super()._set_opt_param_vals(params)

    def write(self, lbuff, rbuff=None):
        if not rbuff:
            buff = lbuff.buff
        else:
            buff = np.array([lbuff.buff, rbuff.buff]).T

        sd.play(self.volume * buff, self.sample_rate, mapping=[1, 2])

    def wait(self):
        try:
            thread = Thread(target=sd.wait)
            thread.start()
            while thread.isAlive():
                time.sleep(.1)
        except KeyboardInterrupt:
            sd.stop()
