import sys

import argparse
from argparse import ArgumentParser
from collections import defaultdict, MutableMapping
from functools import reduce, partial
from operator import getitem

from argus_cli.parser import parse_function
from argus_cli.helpers.log import log


class Command(object):
    """A callable with an accompanying argument parser."""
    def __init__(self, name, func, module, providers=None):
        self.name = name
        self.function = func
        self.argument_parser = module.subparser.add_parser(name, parents=providers or [])

    def __call__(self, *args, **kwargs):
        self.function(*args, **kwargs)


class _ModuleDefaultDict(defaultdict):
    """A defaultdict that is specialized for use with the Module class

    The key has to be passed to the module.
    The key isn't passed to the class in a normal defaultdict.
    """
    def __missing__(self, key):
        self[key] = self.default_factory(name=key)
        return self[key]


class _ModuleAction(argparse._SubParsersAction):
    """Stores the name of the plugin to a attribute on the namespace

    Will add the name of the module to the _modules attribute of the namespace.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        super().__call__(parser, namespace, values, option_string)
        try:
            namespace._modules.insert(0, values[0])
        except AttributeError:
            namespace._modules = [values[0]]


class Module(MutableMapping):
    """Storage for argument parsers.

    This is basically a dict with argparse support.
    """
    def __init__(self, name=None, parent=None, providers=None):
        if parent:
            self.argument_parser = parent.add_parser(name, parents=providers or [])
        else:
            # If there are no parent, then this is the root module
            self.argument_parser = ArgumentParser(parents=providers or [])
        self.subparser = self.argument_parser.add_subparsers(action=_ModuleAction)
        # Make sure that sub-modules automatically gets a parent
        self._dict = _ModuleDefaultDict(partial(Module, parent=self.subparser))

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        if key in self._dict and (
                not isinstance(value, Command)
                or value.function.__code__ != self._dict[key].function.__code__
        ):
            # Due to the fact that plugin.py loads every single file,
            # a command can be loaded twice. Thus we'll have to check the code object as well.
            raise KeyError("A function with the name {} already exists.".format(key))

        self._dict[key] = value

    def __delitem__(self, key):
        del self._dict[key]

    def __len__(self):
        return len(self._dict)

    def __iter__(self):
        return iter(self._dict)


#: The top level module of our arguments.
commands = Module()
#: Module providers that bring some extra commandline arguments.
providers = {
    "argus_cli": ArgumentParser(add_help=False)
}

# FIXME: Hardcoded for the time being. Waiting for @register_provider() to be implemented. ARGUS-11914
# FIXME: Handle that provider arguments might have duplicated arguments to a command.
providers["argus_cli"].add_argument(
    "--debug",
    action="store_true",
    help="Adds debug logging to the program"
)
providers["argus_cli"].add_argument(
    "--apikey",
    help="Manually define the argus-api key"
)


def register_command(plugin_sequence: tuple, command_name: str, func: callable) -> None:
    """Registers a command towards a plugin.

    :param plugin_sequence: The name of the plugin that the function belongs to
    :param command_name: The name of the function
    :param func: The actual function
    """
    log.debug("Registering command \"%s\" in plugin \"%s\"" % (command_name, "/".join(plugin_sequence)))

    module = reduce(getitem, plugin_sequence, commands)
    module[command_name] = Command(command_name, func, module)


def _register_arguments(parser: ArgumentParser, metadata: dict):
    parser.help = metadata.get("help")
    parser.description = metadata.get("description")

    for argument, options in metadata["arguments"].items():
        names = options.pop("names")

        if options.get("required") is False:
            prefixed_names = []
            for name in names:
                prefix = "-" if len(name) is 1 else "--"
                prefixed_names.append(prefix + name)
            names = prefixed_names
        elif len(names) > 1:
            log.warn("%s is a positional argument, and can thus not have an alias. Ignoring aliases." % names[0])
            names = [names[0]]

        # FIXME: Fix for ARGUSUSER-1747, but this doesn't seem the way its supposed to work.
        # Argparse doesn't accept BOTH action='store_true' AND a type keyword argument
        if options.get("action") == "store_true" or options.get("action") == "store_false":
            if options.get("type"):
                del options["type"]
        parser.add_argument(*names, **options)


# FIXME: Provider arguments should be handled in a different fashion.
#        Will be fixed with the register_provider() decorator. ARGUS-11914
def get_provider_arguments() -> dict:
    """Parse arguments that concern the program itself"""
    log.debug("Parsing program arguments")
    arguments = vars(providers["argus_cli"].parse_known_args()[0])

    return arguments


def _error_or_help(parser):
    if any(keyword in sys.argv for keyword in ("--help", "-h")):
        parser.print_help()
        parser.exit()
    parser.error("Not enough arguments")


def parse_arguments() -> (Command, dict):
    """Two parts: Module args and command args"""
    # Remove --help to be able to get the whole help-text for commands.
    # (The command parsing has not happened yet)
    log.debug("Parsing module arguments")
    base_args = [arg for arg in sys.argv[1:] if arg != "--help"]
    arguments = commands.argument_parser.parse_known_args()[0]
    if not hasattr(arguments, "_modules"):
        _error_or_help(commands.argument_parser)

    command = reduce(getitem, arguments._modules, commands)
    if not isinstance(command, Command):
        _error_or_help(command.argument_parser)

    # Registering the metadata is done at a later point to not do unnecessary operations with _parse_function().
    # A single call to _parse_function() takes quite some time, so it's better to do it JIT.
    log.debug("Registering metadata for {}".format(command))
    _register_arguments(
        command.argument_parser,
        parse_function(command.function)
    )

    log.debug("Parsing command arguments")
    arguments = vars(commands.argument_parser.parse_args())
    # Remove plugin arguments as they aren't necessary for the command arguments
    # FIXME: Find another way of storing the plugin sequence.
    arguments.pop("_modules")

    return command, arguments
