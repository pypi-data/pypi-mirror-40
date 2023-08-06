#!/usr/bin/env python3
"""
oocli.execptions
--------------------
"""

class CliException(Exception):
    """
    CliException
    """

class NotImplementedException(CliException):
    """
    NotImplementedException
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        #pylint: disable=unused-argument
        self.instance = args[0]

    def __str__(self):
        return "{}: Not implemented".format(self.instance.cmd)
