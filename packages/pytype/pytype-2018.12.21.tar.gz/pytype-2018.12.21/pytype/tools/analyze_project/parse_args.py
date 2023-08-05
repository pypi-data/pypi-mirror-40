"""Argument parsing for analyze_project."""

import argparse

from pytype import config as pytype_config
from pytype.tools.analyze_project import config


_ARG_PREFIX = '--'


class ParserWrapper(object):
  """Wrapper that adds arguments to a parser while recording them."""

  def __init__(self, parser):
    self.parser = parser
    self.actions = {}

  def add_argument(self, *args, **kwargs):
    try:
      action = self.parser.add_argument(*args, **kwargs)
    except argparse.ArgumentError:
      # We deliberately mask some pytype-single options with pytype-all ones.
      pass
    else:
      self.actions[action.dest] = action


def convert_string(s):
  s = s.replace('\n', '')
  try:
    return int(s)
  except ValueError:
    return config.string_to_bool(s)


class Parser(object):
  """pytype-all parser."""

  def __init__(self, parser, pytype_single_args):
    self.parser = parser
    self.pytype_single_args = pytype_single_args

  def parse_args(self, argv):
    """Parses argv.

    Commandline-only args are parsed normally. File-configurable args appear in
    the parsed args only if explicitly present in argv.

    Args:
      argv: sys.argv[1:]

    Returns:
      An argparse.Namespace.
    """
    file_config_names = set(config.ITEMS) | set(self.pytype_single_args)
    # Creates a namespace that we'll parse argv into, so that we can check for
    # a file configurable arg by whether the None default was overwritten.
    args = argparse.Namespace(**{k: None for k in file_config_names})
    self.parser.parse_args(argv, args)
    for k in file_config_names:
      if getattr(args, k) is None:
        delattr(args, k)
    self.postprocess(args)
    return args

  def config_from_defaults(self):
    defaults = self.parser.parse_args([])
    self.postprocess(defaults)
    conf = config.Config(*self.pytype_single_args)
    conf.populate_from(defaults)
    return conf

  def postprocess(self, args, from_strings=False):
    """Postprocesses the subset of pytype_single_args that appear in args.

    Args:
      args: an argparse.Namespace.
      from_strings: Whether the args are all strings. If so, we'll do our best
        to convert them to the right types.
    """
    names = set()
    for k in self.pytype_single_args:
      if hasattr(args, k):
        names.add(k)
        if from_strings:
          setattr(args, k, convert_string(getattr(args, k)))
    pytype_config.Postprocessor(names, args).process()


def make_parser():
  """Make parser for command line args.

  Returns:
    A Parser object.
  """

  parser = argparse.ArgumentParser(usage='%(prog)s [options] input [input ...]')
  parser.register('action', 'flatten', _FlattenAction)
  modes = parser.add_mutually_exclusive_group()
  modes.add_argument(
      '--tree', dest='tree', action='store_true', default=False,
      help='Display import tree.')
  modes.add_argument(
      '--unresolved', dest='unresolved', action='store_true', default=False,
      help='Display unresolved dependencies.')
  modes.add_argument(
      '--generate-config', dest='generate_config', type=str, action='store',
      default='',
      help='Write out a dummy configuration file.')
  parser.add_argument(
      '-v', '--verbosity', dest='verbosity', type=int, action='store',
      default=1,
      help='Set logging level: 0=ERROR, 1=WARNING (default), 2=INFO.')
  parser.add_argument(
      '--config', dest='config', type=str, action='store', default='',
      help='Configuration file.')
  parser.add_argument(
      '--version', action='store_true', dest='version', default=None,
      help=('Display pytype version and exit.'))

  # Adds options from the config file.
  types = config.make_converters()
  # For nargs=*, argparse calls type() on each arg individually, so
  # _FlattenAction flattens the list of sets of paths as we go along.
  for option in [
      (('-x', '--exclude'), {'nargs': '*', 'action': 'flatten'}),
      (('inputs',), {'metavar': 'input', 'nargs': '*', 'action': 'flatten'}),
      (('-k', '--keep-going'), {'action': 'store_true', 'type': None}),
      (('-o', '--output'),),
      (('-P', '--pythonpath'),),
      (('-V', '--python-version'),)
  ]:
    _add_file_argument(parser, types, *option)
  # Adds options from pytype-single.
  wrapper = ParserWrapper(parser)
  pytype_config.add_basic_options(wrapper)
  return Parser(parser, wrapper.actions)


class _FlattenAction(argparse.Action):
  """Flattens a list of sets. Used by --exclude and inputs."""

  def __call__(self, parser, namespace, values, option_string=None):
    items = getattr(namespace, self.dest, None) or set()
    # We want to keep items as None if values is empty, since that means the
    # argument was not passed on the command line. Note that an empty values
    # can occur for inputs but not --exclude because a positional argument
    # tries to overwrite any existing default with its own.
    if values:
      setattr(namespace, self.dest, items)
      for v in values:
        items.update(v)


def _add_file_argument(parser, types, args, custom_kwargs=None):
  """Add a file-configurable option to the parser.

  Args:
    parser: The parser.
    types: A map from option destination to type.
    args: The option's name(s). Either a 2-tuple of (short_arg, arg) or a
      1-tuple of (arg,).
    custom_kwargs: The option's custom kwargs.
  """
  custom_kwargs = custom_kwargs or {}
  arg = args[-1]
  dest = custom_kwargs.get('dest', arg.lstrip(_ARG_PREFIX).replace('-', '_'))
  kwargs = {'type': types.get(dest),
            'action': 'store',
            'default': config.ITEMS[dest].default,
            'help': config.ITEMS[dest].comment}
  kwargs.update(custom_kwargs)  # custom_kwargs takes precedence
  if kwargs['type'] is None:
    # None is the default anyway, and for some action types, supplying `type` is
    # a type error.
    del kwargs['type']
  if arg.startswith(_ARG_PREFIX):
    # For an optional argument, `dest` should be explicitly given. (For a
    # positional one, it's inferred from `arg`.)
    kwargs['dest'] = dest
  elif 'type' in kwargs:
    # For a positional argument, the type function isn't applied to the default,
    # so we do the transformation manually.
    kwargs['default'] = kwargs['type'](kwargs['default'])
  parser.add_argument(*args, **kwargs)
