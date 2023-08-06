#!/usr/bin/env python3
"""
oocli.echo
--------------
"""

from . import base

class Command(base.Command):
    """
    Simple echo command (for demonstration purposes)
    """

    def __init__(self):
        super().__init__(
            name="Echo",
            description="Print the input to the terminal")

    def _constructorDict(self):
        return {}

    def initParser(self):
        super().initParser()
        self._parser.add_argument("args", nargs='*', help="Things to be echoed")

    def do(self, *args):
        opts = self.parse(*args)
        print(*opts.args)
