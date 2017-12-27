class _Param():
    param_list = []
    opt_param_list = []

    def __init__(self, params):
        self._import_params(params)
        self._assert_params(param_list)
        self._set_opt_param_vals(params)

    def _import_params(self, params):
        vars(self).update((k,v) for k,v in params.items() if k in self._all_params() and k not in vars(self))

    def _assert_params(self, params):
        for p in self.param_list:
            assert params.get(p)

    def _set_opt_param_vals(self, params):
        if len(opt_param_list) > 0:
            raise NotImplmementedError
