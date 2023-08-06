#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of a :class:`ricochet.registries.prototype_and_singleton_registry.DualRegistry`
that uses the basic prototype registry and basic singleton registry internally.
"""
__all__ = ["DualRegistryImpl"]

from ricochet.registries import dual_registry
from ricochet.registries.impl import prototype_container_impl, singleton_container_impl


class DualRegistryImpl(
    dual_registry.DualRegistry,
    prototype_container_impl.PrototypeContainerImpl,
    singleton_container_impl.SingletonContainerImpl,
):
    """
    Implements the :class:`dual_registry.DualRegistry` wrapper using a
    :class:`prototype_container_impl.PrototypeContainerImpl` and a
    :class`singleton_container_impl.SingletonContainerImpl` internally.
    """
