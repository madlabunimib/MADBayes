from functools import update_wrapper
from importlib import import_module
from os.path import dirname
from pkgutil import iter_modules

BACKENDS = {
    module: import_module('.' + module, package='weighted_imputation.backends')
    for (_, module, _) in iter_modules([dirname(__file__)])    
}


class AlternativeBackend():

    def __init__(self, backend: str = None):
        self.backend = backend
    
    def __call__(self, function):
        update_wrapper(self, function)
        self.function = function
        def wrapper(*args, **kwargs):
            if self.backend is not None:
                if self.backend == 'python':
                    return self.function(*args, **kwargs)
                if self.backend in BACKENDS:
                    funct = getattr(BACKENDS[self.backend], self.function.__name__)
                    return funct(*args, **kwargs)
                raise NotImplementedError('"' + self.function.__name__ + '" not implemented in "' + self.backend + '" backend.')
            if self.backend is None:
                modules = [
                    back for back, module in BACKENDS.items()
                    if hasattr(module, self.function.__name__)
                ]
                if len(modules) > 0:
                    funct = getattr(BACKENDS[modules[0]], self.function.__name__)
                    return funct(*args, **kwargs)
            return self.function(*args, **kwargs)
        return wrapper
