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
            if backend is not None and backend not in BACKENDS:
                raise NotImplementedError('"' + function.__name__ + '" not implemented in "' + backend + '" backend.')
            if backend is None:
                exists = [
                    back for back, module in BACKENDS.items()
                    if hasattr(module, function.__name__)
                ]
                if len(exists) > 0:
                    back = getattr(BACKENDS[exists[0]], function.__name__)
                    return back(*args, **kwargs)
            if backend is None:
                return function(*args, **kwargs)

        return inner_wrapper
    
    return backend_wrapper
