#!/usr/bin/env python3
"""
oocli.entrypoint
--------------------
"""

import sys
from . import base

class Command(base.Command):
    """
    Entrypoint - Defines the entrypoint for your program and processes sys.argv into said entrypoint
    """

    def __init__(self, description=None, command=None):
        super().__init__(name=sys.argv[0], description=description)
        assert isinstance(command, base.Command)
        self.command = command

    def do(self):
        """
        Execute the entrypoint command's .do() method
        """
        #pylint: disable=arguments-differ

        self.command.do(*sys.argv[1:])
