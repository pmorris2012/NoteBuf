import pyaudio
import numpy as np

from .param import _Param

class Player(_Param):
    def __init__(self, params):
        self._setup_param_list(["sample_rate"])
        self._setup_opt_param_list(["volume"])
        super().__init__(params)

        self._p = pyaudio.PyAudio()

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        self._stream = self._p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=int(self.sample_rate),
                        output=True)

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("volume", params):
            self.volume = 1
        super()._set_opt_param_vals(params)

    def write(self, buff):
        self._stream.write(self.volume * buff.buff.astype(np.float32), len(buff.buff))

    def __del__(self):
        self._stream.stop_stream()
        self._stream.close()

        self._p.terminate()
