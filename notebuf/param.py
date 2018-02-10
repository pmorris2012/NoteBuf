class UnsetParam(Exception):
    pass

class UnsetOptParam(Exception):
    pass


class _Param():
    def __init__(self, params):
        self.params = params
        self._setup_param_list([])
        self._setup_opt_param_list([])
        self._import_params(params)
        self._assert_params(params)
        self._set_opt_param_vals(params)

    def _setup_param_list(self, param_list):
        if "param_list" not in vars(self):
            self.param_list = param_list
        else:
            self.param_list.extend(param_list)

    def _setup_opt_param_list(self, opt_param_list):
        if "opt_param_list" not in vars(self):
            self.opt_param_list = opt_param_list
        else:
            self.opt_param_list.extend(opt_param_list)

    def _import_params(self, params):
        vars(self).update((k,v) for k,v in params.items() if k in self._all_params() and k not in vars(self))

    def _all_params(self):
        all_params = self.param_list[:]
        all_params.extend(self.opt_param_list)
        return all_params

    def _assert_params(self, params):
        for p in self.param_list:
            if p not in params:
                raise UnsetParam(p)

    def _set_opt_param_vals(self, params):
        for param in self.opt_param_list:
            if param not in vars(self):
                raise UnsetOptParam()

    def _is_opt_param_set(self, param, params):
        return param in params or param in vars(self)

class ParamGroup(dict):
    def copy_with(self, dictionary):
        p = self.copy()
        p.update(dictionary)
        return ParamGroup(p)

