#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines a base registry interface for a prototype registry implementation.

**Prototype objects**:
    An object which is stored internally by the registry once. Each component that requests a reference to the
    prototype will receive some object created from the state of the prototype. Changing this object will not
    mutate the original prototype in any way, and thus provides a copy to every component that requires one.

    This is very similar to a normal instance, but instead of using a class to create an object, we use an
    existing object to derive a copy from.

    Likewise, these are much more difficult to track, as there is no implementation for tracking instances
    created from prototypes.
"""
__all__ = ["PrototypeContainer"]

import abc
from typing import Any, KeysView, Optional, Type

from metabeyond import hints


@hints.interface
class PrototypeContainer(abc.ABC):
    """
    Defines an object which maintains a collection of prototype objects. Prototype objects are instances of a class
    that exist as a template for producing copies for use at runtime. This allows us to encapsulate the state of an
    existing object and pass copies to multiple components across the application context.

    .. image:: resources_static/prototype-cardinality.png

    If one component changes the state of a prototype copy, it will not affect other components using copies of the
    same prototype. Likewise, an instance made from a prototype may only belong to a single object. This owning object
    is allowed to have multiple instances of the same prototype if desired.

    .. image:: resources_static/prototype-distribution.png

    Note:
        Due to the issue that keeping references to objects prevents their destruction, and that it is dangerous to
        provide direct access to weak reference objects as it is non deterministic as to whether they get garbage
        collected halfway through being used by an introspective algorithm, no interface for accessing instances of
        prototypes is implemented here. However, whether this is implemented or not is entirely up to you if you derive
        your own concrete implementations of this class.

    Note:
        The method of copying objects is determined by the implementation.

    Takes a generic TypeVar :attr:`PrototypeWrapperT` describing the base type to output when queried for a prototype
    instance. If no wrapper is provided, this can be omitted, in which case, it will default to `Any`.

    Note:
        No implementation is expected or should attempt to implement name aliasing.
        This is expected to be managed by a higher level abstraction that uses this registry internally.

    Warning:
        This interface is designed to not expose the prototype bases themselves once registered. If this behaviour
        is desired, then it is down to the implementation to provide this, however this is generally not recommended
        unless a good use case can be made.
    """

    @abc.abstractmethod
    def contains_prototype_named(self, canonical_name: str) -> bool:
        """
        Args:
            canonical_name:
                The canonical object name. This is the primary name the object is registered under and resolved by.
                This implements no form of alias lookup.

        Returns:
            `True` if a prototype with the canonical name is registered, `False` if not.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def contains_prototypes_typed(self, type: Type[Any]) -> bool:
        """
        Args:
            type:
                A class that a prototype is expected to be derived from.

        Returns:
            `True` if any prototype derived from the given type exists, `False` if not.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def create_instance_of_prototype(self, canonical_name: str) -> Optional[Any]:
        """
        Args:
            canonical_name:
                The canonical prototype name. This is the primary name the object is registered under and resolved by.
                This implements no form of alias lookup.

        Returns:
            A new instance of the prototype with the given name, or `None` if it doesn't exist...
        """
        raise NotImplementedError

    @abc.abstractmethod
    def register_new_prototype(self, canonical_name: str, prototype: Any) -> None:
        """
        Registers the given object as a prototype under the given name.

        Args:
           canonical_name:
               The canonical prototype's name. This is the primary name the object is registered under and resolved by.
           prototype:
               The object itself to register.

        Throws:
           :class:`ValueError`:
               if the prototype is `None`.
           :class:`NameError`:
               if the prototype is already registered.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_prototype_instance(self, candidate_prototype_instance: Any) -> bool:
        """
        Returns:
             `True` if the given object is an instance of a registered prototype, `False` otherwise.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def count_instances_of_prototype_named(self, canonical_name: str) -> int:
        """
        Args:
            canonical_name:
                The canonical object name. This is the primary name the object is registered under and resolved by.
                This implements no form of alias lookup.

        Returns:
            A count of prototype instances, if the prototype exists for that name.

        Raises:
            NameError if no prototype exists with that name.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_prototype_names(self) -> KeysView[str]:
        """
        Returns:
            View across all prototype names.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def prototype_count(self) -> int:
        """
        The number of objects registered as prototypes.
        """
        raise NotImplementedError
