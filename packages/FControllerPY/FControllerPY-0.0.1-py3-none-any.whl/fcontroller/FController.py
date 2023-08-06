#!/usr/bin/env python

from .Core import Core


class FController(Core):
    def __new__(cls, *parameters):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls, *parameters)
        return it

    def set_module(self, name, module, parameters=[]):
        namespace = __import__(module)
        class_ = getattr(namespace, module)
        instance = class_(*parameters)
        return self.register_module(name, instance)

    def set_service(self, name, service, parameters=[]):
        namespace = __import__(service)
        class_ = getattr(namespace, service)
        instance = class_(*parameters)
        return self.register_service(name, instance)
