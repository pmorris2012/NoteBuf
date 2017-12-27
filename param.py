class _Param():
    param_list = []
    opt_param_list = []

    def __init__(self, params):
        self._import_params(params)
        self._assert_params(params)
        self._set_opt_param_vals(params)

    def _import_params(self, params):
        vars(self).update((k,v) for k,v in params.items() if k in self._all_params() and k not in vars(self))

    def _all_params(self):
        all_params = self.param_list[:]
        all_params.extend(self.opt_param_list)
        return all_params

    def _assert_params(self, params):
        for p in self.param_list:
            assert p in params

    def _set_opt_param_vals(self, params):
        if len(self.opt_param_list) > 0:
            raise NotImplmementedError
