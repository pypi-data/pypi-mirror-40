#!/usr/bin/env python

from abc import ABCMeta


class Module:
    __metaclass__ = ABCMeta

    services = {}

    storage = {}

    def connect(self, services, storage):
        if len(self.services) == 0:
            self.services = services

        if len(self.storage) == 0:
            self.storage = storage

    def __getattr__(self, item):
        if item in self.services:
            return self.services[item]
        return None
