"""
A wrapper for another class that can be used to delay
instantiation of the wrapped class.

Copied from Django and modified to add thread safety.
https://github.com/django/django/blob/master/django/utils/functional.py

"""

import operator
import threading


empty = object()


def new_method_proxy(func):
    def inner(self, *args):
        self._setup_once()
        return func(self._wrapped, *args)
    return inner


class ThreadSafeLazyObject(object):
    """
    A wrapper for another class that can be used to delay
    instantiation of the wrapped class.

    Subclasses must implement a _setup() method.

    """

    # Avoid infinite recursion when tracing __init__ (#19456).
    _wrapped = None

    def __init__(self):
        self._wrapped = empty
        self._setup_lock = threading.Lock()

    __getattr__ = new_method_proxy(getattr)

    def __setattr__(self, name, value):
        if name == '_wrapped' or name == '_setup_lock':
            # Assign to __dict__ to avoid infinite __setattr__ loops.
            self.__dict__[name] = value
        else:
            self._setup_once()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == '_wrapped' or name == '_setup_lock':
            raise TypeError("can't delete %s." % name)
        self._setup_once()
        delattr(self._wrapped, name)

    def _setup_once(self):
        if self._wrapped is empty:
            with self._setup_lock:
                if self._wrapped is empty:
                    self._setup()

    def _setup(self):
        """
        Must be implemented by subclasses to initialize the wrapped object.

        """
        raise NotImplementedError('subclasses of %s must provide a _setup() method' % self.__class__.__name__)

    __str__ = new_method_proxy(str)
    __unicode__ = new_method_proxy(unicode)
    __nonzero__ = new_method_proxy(bool)

    # Introspection support
    __dir__ = new_method_proxy(dir)

    # Dictionary methods support
    __getitem__ = new_method_proxy(operator.getitem)
    __setitem__ = new_method_proxy(operator.setitem)
    __delitem__ = new_method_proxy(operator.delitem)

    __len__ = new_method_proxy(len)
    __contains__ = new_method_proxy(operator.contains)
