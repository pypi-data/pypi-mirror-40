import pkgutil
import sys

import os
from argparse import ArgumentParser
from importlib import import_module

from robot_cli import get_version


class CommandError(Exception):
    """
    Exception class indicating a problem while executing a command.
    """

    def __init__(self, msg='', *args, **kwargs):
        self.msg = msg
        super(CommandError, self).__init__(*args, **kwargs)


def get_commands():
    command_dir = os.path.join(__path__[0], "commands")
    subcommands = [name for _, name, is_pkg in
                   pkgutil.iter_modules([command_dir])
                   if not is_pkg and not name.startswith("_")]
    subcommands.append("help")
    subcommands.append("version")
    subcommands.sort()
    return subcommands


def load_command_class(prog, subcommand):
    cmd_module = import_module("robot_cli.core.commands.%s" % subcommand)
    return cmd_module.Command(prog=prog)


class ManagementUtility(object):
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog = "robot-cli"

    def main_help_text(self):
        """
        Returns the script's main help text, as a string.
        """
        usage = [
            "",
            "Type '%s help <subcommand>' for help on a specific subcommand." % self.prog,
            "",
            "Available subcommands:",
        ]
        for subcommand in get_commands():
            usage.append("  %s" % subcommand)
        usage.append("")

        return "\n".join(usage)

    def fetch_command(self, subcommand):
        subcommands = get_commands()
        if subcommand not in subcommands:
            sys.stderr.write(
                "Unknown command: %r\nType '%s help' for usage.\n" % (
                    subcommand, self.prog))
            sys.exit(1)
        return load_command_class(self.prog, subcommand)

    def execute(self):
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = "help"  # Display help if no arguments were given.

        parser = ArgumentParser(
            prog=self.prog,
            usage="%s subcommand [options] [args]" % self.prog,
            add_help=False)
        parser.add_argument("args", nargs="*")  # catch-all
        try:
            opts, args = parser.parse_known_args(self.argv[2:])
        except CommandError:
            pass

        if subcommand == "help":
            if len(opts.args) < 1:
                sys.stdout.write(self.main_help_text())
            else:
                self.fetch_command(opts.args[0]).print_help()
        elif subcommand == "version" or self.argv[1:] == ["--version"]:
            sys.stdout.write("%s %s\n" % (self.prog, get_version()))
        elif self.argv[1:] in (["--help"], ["-h"]):
            sys.stdout.write(self.main_help_text())
        else:
            self.fetch_command(subcommand).run_from_argv(self.argv)


def execute_from_command_line(argv=None):
    utility = ManagementUtility(argv)
    utility.execute()
