import numpy as np

from param import _Param


class _Oscillator(_Param):
    def __init__(self, params):
        self._setup_param_list(["start", "duration", "amplitude", "frequency", "sample_rate"])
        self._setup_opt_param_list(["frequency_shift", "slide_start", "slide_duration"])
        super().__init__(params)

        if self.frequency_shift != 0:
            assert self.slide_start + self.slide_duration < self.duration

        samples1 = int(self.slide_start * self.sample_rate)
        samples2 = int(self.slide_duration * self.sample_rate)
        samples3 = int(self.duration * self.sample_rate) - samples2 - samples1

        phase1, k1 = self._gen_phase(samples1, self.frequency, self.frequency)
        phase2, k2 = self._gen_phase(samples2, self.frequency, self.frequency + self.frequency_shift, k1)
        phase3, _ = self._gen_phase(samples3, self.frequency + self.frequency_shift, self.frequency + self.frequency_shift, k2)
        self.phase = np.concatenate((phase1, phase2, phase3))
        #else:
            #self.phase, _ = self._gen_phase(int(self.duration * self.sample_rate), self.frequency, self.frequency)

        print(self.phase)


    def _gen_phase(self, num_samples, fstart, fend, k=0):
        buff = np.arange(num_samples).astype(np.float32)
        buff = buff / num_samples
        t = num_samples * buff / self.sample_rate
        phase = t * (fstart + (fend - fstart) * buff / 2) + k
        return phase, ((phase[-1] % 1 + (phase[-1] - phase[-2])) % 1) if len(phase) > 0 else 0
    
    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("frequency_shift", params):
            self.frequency_shift = 0
        if not self._is_opt_param_set("slide_start", params):
            self.slide_start = 0
        if not self._is_opt_param_set("slide_duration", params):
            self.slide_duration = self.duration * 0.1
        super()._set_opt_param_vals(params)
        

class OscSine(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff = np.sin(2 * np.pi * self.phase)

class OscSawtooth(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff = np.mod(1 + 2 * self.phase, 2) - 1

class OscTriangle(_Oscillator):
    def __init__(self, params):
        super().__init__(params)
        self.buff = 2 * np.abs(np.mod(-0.5 + 2 * self.phase, 2) -1) - 1

class OscSquare(OscSawtooth, _Param):
    def __init__(self, params):
        self._setup_opt_param_list(["duty_cycle"])
        super().__init__(params)
        
        assert self.duty_cycle >= 0 and self.duty_cycle <= 1
        self.buff = np.sign(self.buff + 1 - 2 * self.duty_cycle)

    def _set_opt_param_vals(self, params):
        if not self._is_opt_param_set("duty_cycle", params):
            self.duty_cycle = 0.5
        super()._set_opt_param_vals(params)
