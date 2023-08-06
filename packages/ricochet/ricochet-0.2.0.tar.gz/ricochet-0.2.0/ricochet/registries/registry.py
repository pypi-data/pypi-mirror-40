#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Represents a generic registry. This is an interface that an application context can be expected to interface with.

There is no requirement to implement all of the methods, only some need to be implemented. This is designed to allow
a Singleton registry and a Prototype registry to interop together, or for only one implementation to be used.
"""
__all__ = ["Registry"]

import abc
from typing import Iterator, Type, Any

from ricochet.utils import hints


@hints.interface
class Registry(abc.ABC):
    """
    A generic type of registry that is expected to be the interface used in an application.
    """

    @abc.abstractmethod
    def contains_object_named(self, canonical_name: str) -> bool:
        """
        Args:
            canonical_name:
                The canonical object name. This is the primary name the object is registered under and resolved by.
                This implements no form of alias lookup.

        Returns:
            `True` if a prototype or singleton with the canonical name is registered, `False` if not.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def contains_objects_typed(self, type: Type[Any]) -> bool:
        """
        Args:
            type:
                A class that a prototype or singleton is expected to be derived from.

        Returns:
            `True` if any prototype or singleton derived from the given type exists, `False` if not.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def count_objects_named(self, canonical_name: str) -> int:
        """
        Args:
            canonical_name:
                The canonical object name. This is the primary name the object is registered under and resolved by.
                This implements no form of alias lookup.

        Returns:
            A count of object instances, if the prototype or singleton exists for that name.

        Raises:
            NameError if no prototype or singleton exists with that name.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_object(self, candidate_object: Any) -> bool:
        """
        Args:
            candidate_object: The potential singleton or prototype instance to look for.

        Returns:
            `True` if this object is a prototype instance or a singleton object in this registry, or `False` otherwise.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_object_names(self) -> Iterator[str]:
        """
        Yields all object names. These are expected to be unique as long as the internal representations that are
        protected have not been tampered with directly.
        """
        raise NotImplementedError
