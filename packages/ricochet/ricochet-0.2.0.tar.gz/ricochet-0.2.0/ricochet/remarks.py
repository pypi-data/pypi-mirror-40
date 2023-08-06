#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remark decorators used for introspection/reflection at runtime.
"""
__all__ = ["Configuration", "Component", "SingletonBean", "PrototypeBean"]

import inspect

from metabeyond import remarks

from ricochet.utils import hints


@hints.class_only_decorator
@hints.discovery
class Configuration(remarks.Remark, constraint=inspect.isclass):
    """
    Applied to a class to mark it as a configuration.

    A configuration is a class containing zero or more "Bean" functions. These are detected and autowired into any
    managed class component that requires them.
    """

    pass


@hints.method_only_decorator
@hints.discovery
class SingletonBean(remarks.Remark, constraint=inspect.isfunction):
    """
    Applies to a method within a configuration class, marking it. The function is evaluated and expected to return a
    non-None object of some kind at runtime. This result is expected to be stored in some
    :mod:`ricochet.abstract_singleton_registry` implementation as a singleton.

    Args:
        lazy:
            Defaulting to `False`, if `True` then the function is only evaluated when we actually need it. If this
            is `False`, then the function is evaluated as soon as we detect it. This could be used to prevent
            initialising a resource until we actually know if we need to use it in our application.

    Note:
        The library is not expected to handle coroutines. The default implementation in this framework will not
        provide support for this directly.
    """

    def __init__(self, *, lazy: bool = False) -> None:
        super().__init__()
        self.lazy = lazy


@hints.method_only_decorator
@hints.discovery
class PrototypeBean(remarks.Remark, constraint=inspect.isfunction):
    """
    Applies to a method within a configuration class, marking it. The function is evaluated and expected to return a
    non-None object of some kind at runtime. This result is expected to be stored in some
    :mod:`ricochet.abstract_prototype_registry` implementation as a prototype object.

    Note:
        The library is not expected to handle coroutines. The default implementation in this framework will not
        provide support for this directly.
    """

    def __init__(self) -> None:
        super().__init__()


@hints.class_only_decorator
@hints.discovery
class Component(remarks.Remark, constraint=inspect.isclass):
    """
    Applies to a class, marking it. The class can then be detected at runtime and loaded into a ricochet application
    automatically by the framework. These classes are expected to implement some form of task, role, or other
    form of importance in your application.

    You may wish to derive from this class to produce your own meaningful remark names, such as `Controller`,
    `View`, `Repository`, `Service`, `Flyweight`, etc. This is left to your own discretion. Equally, this can be used
    directly, and will still be valid.
    """

    pass


@hints.method_only_decorator
@hints.discovery
class AfterConstruct(remarks.Remark, constraint=inspect.isfunction):
    """
    Decorates a class method.

    Invoke this method once a registry creates an object. This is assumed to only have one argument (self or cls).

    Warning:
        It is down to the registry you are using to provide this functionality. Objects not managed by this framework
        in a compliant registry will not have any effect from implementing this remark on a method.
    """

    pass
