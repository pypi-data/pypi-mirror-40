#!/usr/bin/env python

import re
from abc import ABCMeta
from .Module import Module
from .FControllerError import FControllerError


class Core(object):
    __metaclass__ = ABCMeta

    VERSION = '0.0.1'

    modules = {}

    services = {}

    storage = {}

    def register_module(self, name, module):
        if name not in self.modules and isinstance(module, Module):
            module.connect(self.services, self.storage)
            self.modules[name] = module
            return True
        return False

    def unregister_module(self, name):
        if name in self.modules:
            del self.modules[name]
            return True
        return False

    def register_service(self, name, service):
        if name not in self.services:
            self.services[name] = service
            return True
        return False

    def unregister_service(self, name):
        if name in self.services:
            del self.services[name]
            return True
        return False

    def run(self, path, data=[]):
        path = self.__route(path)
        return getattr(self.modules[path['module']], path['method'])(*data)

    def __route(self, path):
        if re.compile('^[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+$').search(path) is None:
            raise FControllerError('Incorrect module call pattern')

        call_path = path.split(".")

        if call_path[0] not in self.modules:
            raise FControllerError('Module instance not found')

        if call_path[1] not in dir(self.modules[call_path[0]]):
            raise FControllerError('Module method requested is not available')

        return {'module': call_path[0], 'method': call_path[1]}
