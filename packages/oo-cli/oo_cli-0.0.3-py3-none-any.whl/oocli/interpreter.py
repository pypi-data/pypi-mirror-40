#!/usr/bin/env python3
"""
oocli.interpreter
---------------------
"""

import sys
import argparse
from . import base
from .exceptions import CliException

class Command(base.Command):
    """
    Interprets commands given (by, for example, sys.argv[]) into running subcommands in classes.
    Can be nested to create a hierarchy of commands

    :param str name: The name of the interpreter command
    :param str description: Overrides the default description of "interpet subcommands"
    :param list commands: List of commands to contain within the interpreter

    Example:

    .. testcode::

        from oocli import base, interpreter, echo

        command = interpreter.Command(
            name=None,
            commands=[
                echo.Command(),
                interpreter.Command(
                    name="Outer",
                    commands=[
                        echo.Command(),
                        interpreter.Command(
                            name="Inner",
                            commands=[
                                echo.Command()
                            ]
                        )
                    ]
                )
            ]
        )

        # Normally you'd do this with *sys.argv[1:]
        command.do("echo", "TEST (root)")
        command.do("outer", "echo", "TEST (outer)")
        command.do("outer", "inner", "echo", "TEST (inner)")

    Output:

    .. testoutput::

        TEST (root)
        TEST (outer)
        TEST (inner)

    """

    def __init__(self, name=None, description=None, commands=None):
        assert commands is not None
        assert isinstance(commands, list)
        assert commands != []

        if name is None:
            name = sys.argv[0].split("/")[-1]

        if description is None:
            description = "Interpret subcommands"

        super().__init__(
            name=name,
            description=description)

        self.commands = {}
        for item in commands:
            assert isinstance(item, base.Command)
            item.stackAppendleft(self.cmd) # Insert the interpreter into the command's stack
            self.commands.update({item.cmd: item})

    def initParser(self):
        super().initParser()
        self._parser.add_argument(
            "-l", "--list",
            action="store_const",
            default=False,
            const=True,
            help="List commands that can be run")
        self._parser.add_argument(
            "cmd",
            nargs='?',
            help="The command to run")
        self._parser.add_argument(
            "args",
            nargs=argparse.REMAINDER,
            help="Arguments to <command>")

    def call(self, cmd, *args):
        """
        Call member command <cmd> with *args
        """
        try:
            assert cmd is not None
            self.commands[cmd].do(*args)
        except AssertionError:
            raise CliException("You must specify a command to run")
        except KeyError:
            raise CliException("{}: Command not found".format(cmd))

    def printList(self, prefix=""):
        """
        Print the list of commands that the interpreter has
        """
        for cmd, obj in self.commands.items():
            if isinstance(obj, self.__class__):
                print(prefix + obj.cmd + ": " + obj.description)
                if prefix == "":
                    newprefix = "- "
                else:
                    newprefix = "  " + prefix

                obj.printList(prefix=newprefix)

            else:
                print("{}{}: {}".format(prefix, cmd, obj.description))

    def do(self, *args):
        opts = self.parse(*args)
        if opts.list:
            self.printList()

        else:
            try:
                self.call(opts.cmd, *opts.args)
            except CliException as exception:
                print(exception)
                self._parser.print_help()
                sys.exit(1)
