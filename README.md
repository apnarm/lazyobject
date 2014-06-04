lazyobject 0.0.1
================

A thread-safe LazyObject class for Python.

The LazyObject class is a wrapper for another
class that can be used to delay instantiation
of the wrapped class.

This was copied from Django and modified to add
thread safety.
https://github.com/django/django/blob/master/django/utils/functional.py

Why
---

This lets you create module-level objects
that will not initialize until first accessed.
This library simply adds thread-safety to Django's
version, to ensure that only 1 thread will initialize
the object.

Installation
------------

    pip install lazyobject

Usage
-----

    from lazyobject import ThreadSafeLazyObject

    class MyLazyClass(ThreadSafeLazyObject):
      def _setup(self):
        my_real_object = create_my_object()
        self._wrapped = my_real_object

    my_lazy_object = MyLazyClass()
