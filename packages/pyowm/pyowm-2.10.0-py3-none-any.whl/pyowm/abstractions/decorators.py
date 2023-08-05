import warnings
from functools import wraps


def deprecated(will_be=None, on_version=None, name=None):
    """
    Function decorator that warns about deprecation upon function invocation.
    :param will_be: str representing the target action on the deprecated function
    :param on_version: tuple representing a SW version
    :param name: name of the entity to be deprecated (useful when decorating
    __init__ methods so you can specify the deprecated class name)
    :return: callable
    """
    def outer_function(function):
        if name is None:
            _name = function.__name__
        else:
            _name = name
        warning_msg = '"%s" is deprecated.' % _name
        if will_be is not None and on_version is not None:
            warning_msg += " It will be %s on version %s" % (
                will_be,
                '.'.join(map(str, on_version)))

        @wraps(function)
        def inner_function(*args, **kwargs):
            warnings.warn(warning_msg,
                          category=DeprecationWarning,
                          stacklevel=2)
            return function(*args, **kwargs)

        return inner_function

    return outer_function

