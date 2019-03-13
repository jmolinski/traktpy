class Validator:
    def _validate(self, *args, **kwargs):  # pragma: no cover
        return True

    def validate(self, *args, **kwargs):
        return self._validate(*args, **kwargs) is not False


class AuthRequiredValidator(Validator):
    def _validate(self, client, *args, **kwargs):
        if not client.authenticated:
            return False


class RequiredArgsValidator(Validator):
    def _validate(self, *args, path=None, **kwargs):
        for p in path.req_args:
            arg_name = p[1:]
            if arg_name not in kwargs or kwargs[arg_name] in (None, [], {}):
                return False


class OptionalArgsValidator(Validator):
    """
    path: 'a/?b/?c'
    if c is provided then b must be provided
    """

    def _validate(self, *args, path=None, **kwargs):
        require_previous = False

        for p in path.opt_args[::-1]:
            arg_name = p[1:]
            if require_previous:
                if arg_name not in kwargs or kwargs[arg_name] in (None, [], {}):
                    return False
            elif arg_name in kwargs:
                require_previous = True


class PerArgValidator(Validator):
    def __init__(self, arg_name, f):
        self.arg_name = arg_name
        self.boolean_check = f

    def _validate(self, *args, **kwargs):
        if self.arg_name in kwargs:
            return self.boolean_check(kwargs[self.arg_name])
