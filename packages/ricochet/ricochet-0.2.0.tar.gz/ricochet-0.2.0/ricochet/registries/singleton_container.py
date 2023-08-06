#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines a base registry interface for a singleton registry.

**Singleton objects**:
    Global objects created once and shared. Often these refer to classes that may only ever have one instance,
    whereas in this framework, it refers to an object with a specific name. Zero or more managed components
    may store a reference to zero or more singleton instances. If one component changes the state of a singleton,
    then this change seen by all components that store a reference to the same singleton.
"""
__all__ = ["SingletonContainer"]

import abc
from typing import Any, Iterator, ItemsView, KeysView, Optional, Type, ValuesView

from metabeyond import hints


@hints.interface
class SingletonContainer(abc.ABC):
    """
    Defines an object which maintains some collection of singleton objects. These are registered
    and then kept for the lifetime of the object unless otherwise specified, and are stored as a mapping
    of a string name to an object instance. Thus, only one object may have the same name.

    .. image:: resources_static/singleton-cardinality.png

    Singletons are shared among multiple components across the application context. If one component alters the
    state of a singleton, it will alter the state for all references, as singletons will be initialised once and shared.

    Note:
        Singleton objects are defined as objects that exist once per registry, and are provided as references
        to anything that requires the dependency.

    .. image:: resources_static/singleton-distribution.png

    Takes a generic TypeVar :attr:`SingletonWrapperT` describing the base type to output when queried for a singleton
    instance. If no wrapper is provided (i.e. the singleton is just output "as is"), this can be omitted, in which case,
    it will default to `Any`.

    Note:
        No implementation is expected or should attempt to implement lazy initialisation support, or name aliasing.
        This is expected to be managed by a higher level abstraction that uses this registry internally.
    """

    @abc.abstractmethod
    def contains_singleton_named(self, canonical_name: str) -> bool:
        """
        Args:
            canonical_name:
                The canonical object name. This is the primary name the object is registered under and resolved by.
                This implements no form of alias lookup.

        Returns:
            `True` if this registry contains the singleton object with the given name, or `False` if not.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def contains_singletons_typed(self, type: Type[Any]) -> bool:
        """
        Args:
            type:
                A class that a singleton is expected to be derived from.

        Returns:
            `True` if this registry contains a singleton object derived from the given type, or `False` if not.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_singleton_named(self, canonical_name: str) -> Optional[Any]:
        """
        Args:
            canonical_name:
                The canonical singleton name. This is the primary name the object is registered under and resolved by.
                This implements no form of alias lookup.

        Returns:
            The singleton with the given name, or `None` if it doesn't exist...
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_singletons_typed(self, type: Type[Any]) -> Iterator[Any]:
        """
        Returns:
             An iterator across any singleton objects derived from the given type that exist in
             this registry.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def register_new_singleton(self, canonical_name: str, singleton: Any) -> None:
        """
        Registers the given object as a singleton object under the given name.

        Args:
            canonical_name:
                The canonical singleton's name. This is the primary name the object is registered under and resolved by.
            singleton:
                The object itself to register.

        Throws:
            :class:`ValueError`:
                if the singleton object is `None`.
            :class:`NameError`:
                if the singleton is already registered.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_singleton(self, candidate_singleton: Any) -> bool:
        """
        Returns:
             `True` if the given object is a registered singleton, `False` otherwise.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_singletons(self) -> ItemsView[str, Any]:
        """
        Gets an immutable mapping of singleton names to singleton object instances in this registry.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_singleton_names(self) -> KeysView[str]:
        """
        Gets an immutable key view of singleton names in this registry.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_singleton_instances(self) -> ValuesView[Any]:
        """
        Gets an immutable value view of singleton instances in this registry.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def singleton_count(self) -> int:
        """
        The number of objects registered as singletons.
        """
        raise NotImplementedError
