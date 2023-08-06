#!/usr/bin/env python3
"""
oocli.base
--------------
"""

from argparse import ArgumentParser
from collections import deque
from .exceptions import NotImplementedException

class Command:
    """
    Base class for CLI classes.  Realistically, this really doesn't do anything other than
    establish basic metadata for the class and provide structure for subclasses to follow

    :param str name: The name of the command
    :param str cmd: The command text of the command.  If absent, it defaults to name.lower()

    .. testsetup:: *

        from collections import deque

        from oocli import base
        from oocli.exceptions import *

        baseCommand = base.Command(
            name="Test",
            description="Description")

    .. testcode::
        :hide:

        # Check that name / cmd are set correctly
        assert baseCommand.name == "Test"
        assert baseCommand.cmd == "test"
        assert baseCommand.description == "Description"
        assert baseCommand._stack == deque(["test"])

    """

    def __init__(self, name=None, description=None, cmd=None, stack=None):
        #pylint: disable=unused-argument

        assert name is not None

        self.name = name

        if isinstance(stack, deque):
            self._stack = stack
        else:
            self._stack = deque([])
            if stack is not None:
                self._stack.append(stack)

        if cmd is None:
            self.cmd = name.lower()
        else:
            self.cmd = cmd

        self._stack.append(self.cmd)

        if description is not None:
            self.description = description
        else:
            self.description = None

        self.initParser()

    def __call__(self, *args, **kwargs):
        return args[0](**self._constructorDict())

    def _constructorDict(self):
        return dict(filter(lambda x: not x[0].startswith("_"), self.__dict__.items()))

    def initParser(self):
        """
        Initalize the argument parser.  Subclasses should define any arguments for the command
        in this method. If you subclass this class, define your parser args here so that if the
        stack gets changed, everything is updated correctly.
        """
        self._parser = ArgumentParser(
            prog=" ".join(self._stack),
            description=self.description)

    def stackAppendleft(self, value):
        """
        Updates self._stack by prepending value to the list and re-initalizing the parser
        If you create a subclass that contains other commands (like the Interpreter class)

        :param str value: The item to prepend (deque.appendleft()) to the stack
        """
        self._stack.appendleft(value)
        self.initParser()

    def parse(self, *args):
        """
        Parse arguments through self._parser

        :param args: Sequential arguments to pass through the parser
        """
        return self._parser.parse_args(args)

    def do(self, *args):
        #pylint: disable=unused-argument,invalid-name
        """
        Execute the command (not implemented in BaseCommand)

        :param args: Sequential arguments passed from the CLI

        .. testcode::
            :hide:

            try:
                baseCommand.do()
            except NotImplementedException:
                pass
        """
        raise NotImplementedException(self)
