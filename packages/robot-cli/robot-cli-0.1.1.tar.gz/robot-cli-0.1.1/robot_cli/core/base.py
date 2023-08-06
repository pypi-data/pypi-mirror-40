import sys
from argparse import ArgumentParser

from robot_cli.core import CommandError


class BaseCommand(object):
    # Metadata about this command.
    help = ""
    args = ""
    subcommand = ""

    def __init__(self, prog="robot-cli"):
        self.prog = prog

    def usage(self):
        """
        Return a brief description of how to use this command, by
        default from the attribute ``self.help``.
        """
        usage = "%s %s [options] %s" % (self.prog, self.subcommand, self.args)
        if self.help:
            return "%s\n\n%s" % (usage, self.help)
        else:
            return usage

    def create_parser(self):
        """
        Create and return the ``ArgumentParser`` which will be used to
        parse the arguments to this command.
        """
        parser = ArgumentParser(prog=self.prog, usage=self.usage())
        self.add_arguments(parser)
        return parser

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        pass

    def print_help(self):
        """
        Print the help message for this command, derived from ``self.usage()``.
        """
        parser = self.create_parser()
        parser.print_help()

    def run_from_argv(self, argv):
        parser = self.create_parser()

        options, args = parser.parse_known_args(argv[2:])
        cmd_options = vars(options)
        try:
            self.execute(*args, **cmd_options)
        except Exception as e:
            if not isinstance(e, CommandError):
                raise e
            sys.stderr.write(e.msg + "\n")
            sys.exit(1)

    def execute(self, *args, **options):
        """
        Try to execute this command.
        """
        output = self.handle(*args, **options)
        if output:
            sys.stdout.write(output)

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        raise NotImplementedError(
            "subclasses of BaseCommand must provide a handle() method")
