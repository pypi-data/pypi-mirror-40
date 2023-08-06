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
        Execute the entrypoint command's .do() method, and translate bool return values
        for Linux's sanity (0 is true, 1 is false).
        """
        #pylint: disable=arguments-differ

        returnCode = self.command.do(*sys.argv[1:])

        # Translate into zero/nonzero return codes
        # Linux, zero is true, nonzero is false
        if isinstance(returnCode, bool):
            if returnCode:
                sys.exit(0)
            else:
                sys.exit(1)

        else:
            # String and int are handled correctly
            sys.exit(returnCode)
