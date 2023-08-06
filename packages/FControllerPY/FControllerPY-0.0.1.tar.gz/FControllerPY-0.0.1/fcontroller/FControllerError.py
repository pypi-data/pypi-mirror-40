#!/usr/bin/env python


class FControllerError(Exception):
    def __init__(self, message, code=0):
        self.message = message
        self.code = code
