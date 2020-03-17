from functools import wraps
from os.path import dirname
from pkgutil import iter_modules
from importlib import import_module

BACKENDS = {
    module: import_module('.' + module, package='weighted_imputation.backends')
    for (_, module, _) in iter_modules([dirname(__file__)])    
}

def alternative_backend(backend=None):

    def backend_wrapper(function):

        @wraps(function)
        def inner_wrapper(*args, **kwargs):
            if backend is not None:
                if backend in BACKENDS:
                    funct = getattr(BACKENDS[backend], function.__name__)
                    return funct(*args, **kwargs)
                raise NotImplementedError('"' + function.__name__ + '" not implemented in "' + backend + '" backend.')
            if backend is None:
                modules = [
                    funct for funct, module in BACKENDS.items()
                    if hasattr(module, function.__name__)
                ]
                if len(modules) > 0:
                    funct = getattr(BACKENDS[modules[0]], function.__name__)
                    return funct(*args, **kwargs)
            return function(*args, **kwargs)

        return inner_wrapper
    
    return backend_wrapper
