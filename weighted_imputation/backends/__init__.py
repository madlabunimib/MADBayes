from functools import wraps
from importlib import import_module
from os.path import dirname
from pkgutil import iter_modules


def initialize_backend():
    return {
        module: import_module('.' + module, package='weighted_imputation.backends')
        for (_, module, _) in iter_modules([dirname(__file__)])    
    }

BACKENDS = initialize_backend()

def alternative_backend(backend=None):

    def backend_wrapper(function):

        @wraps(function)
        def wrapped(*args, **kwargs):
            if wrapped.backend is not None:
                if wrapped.backend == 'python':
                    return function(*args, **kwargs)
                if wrapped.backend in BACKENDS:
                    funct = getattr(BACKENDS[wrapped.backend], function.__name__)
                    return funct(*args, **kwargs)
                raise NotImplementedError('"' + function.__name__ + '" not implemented in "' + wrapped.backend + '" backend.')
            if wrapped.backend is None:
                modules = [
                    back for back, module in BACKENDS.items()
                    if hasattr(module, function.__name__)
                ]
                if len(modules) > 0:
                    funct = getattr(BACKENDS[modules[0]], function.__name__)
                    return funct(*args, **kwargs)
            return function(*args, **kwargs)
        
        wrapped.backend = backend

        return wrapped
    
    return backend_wrapper
