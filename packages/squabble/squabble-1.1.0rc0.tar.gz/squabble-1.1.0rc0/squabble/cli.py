"""
Usage:
  squabble [options] [PATHS...]
  squabble (-h | --help)

Arguments:
  PATHS  Paths to check. If given a directory, will recursively traverse the
         path and lint all files ending in `.sql` [default: -].

Options:
  -h --help               Show this screen.
  -V --verbose            Turn on debug level logging.
  -v --version            Show version information.

  -e --explain=CODE       Show detailed explanation of a message code.
  --list-presets          List available preset configurations.
  --list-rules            List available rules.
  --show-rule=RULE        Show detailed information about RULE.

  -c --config=PATH        Path to configuration file.
  -p --preset=PRESET      Start with a base preset rule configuration.
  -r --reporter=REPORTER  Use REPORTER for output rather than one in config.
"""

import glob
import json
import os.path
import sys

import docopt
from colorama import Style
from pkg_resources import get_distribution

import squabble
import squabble.message
from squabble import config, lint, reporter, rule


def main():
    version = get_distribution('squabble').version
    args = docopt.docopt(__doc__, version=version)
    return dispatch_args(args)


def dispatch_args(args):
    """
    Handle the command line arguments as parsed by ``docopt``. Calls the
    subroutine implied by the combination of command line flags and returns the
    exit status (or ``None``, if successful) of the program.

    Note that some exceptional conditions will terminate the program directly.
    """
    if args['--verbose']:
        squabble.logger.setLevel('DEBUG')

    if args['--list-presets']:
        return list_presets()

    config_file = args['--config'] or config.discover_config_location()
    if config_file and not os.path.exists(config_file):
        sys.exit('%s: no such file or directory' % config_file)

    base_config = config.load_config(
        config_file,
        preset_name=args['--preset'],
        reporter_name=args['--reporter'])

    # Load all of the rule classes into memory (need to do this now to
    # be able to list all rules / show rule details)
    rule.load_rules(plugin_paths=base_config.plugins)

    if args['--list-rules']:
        return list_rules()

    if args['--show-rule']:
        return show_rule(name=args['--show-rule'])

    if args['--explain']:
        return explain_message(code=args['--explain'])

    return run_linter(base_config, args['PATHS'])


def run_linter(base_config, paths):
    """
    Run linter against all SQL files contained in ``paths``.

    ``paths`` may contain both files and directories.

    If ``paths`` is empty or only contains ``"-"``, squabble will read
    from stdin instead.
    """
    if not paths:
        paths = ['-']

    files = collect_files(paths)

    issues = []
    for file_name, contents in files:
        file_config = config.apply_file_config(base_config, contents)
        issues += lint.check_file(file_config, file_name, contents)

    reporter.report(base_config.reporter, issues, dict(files))

    # Make sure we have an error status if something went wrong.
    return 1 if issues else 0


def _slurp_file(file_name):
    """Read entire contents of ``file_name`` as text."""
    with open(file_name, 'r') as fp:
        return fp.read()


def collect_files(paths):
    """
    Given a list of files or directories, find all named files as well as
    any files ending in `.sql` in the directories.

    The return format is a list of tuples containing the file name and
    file contents.

    The value ``'-'`` is treated specially as stdin.
    """
    files = []

    for path in map(os.path.expanduser, paths):
        if path == '-':
            files.append(('stdin', sys.stdin.read()))

        elif not os.path.exists(path):
            sys.exit('%s: no such file or directory' % path)

        elif os.path.isdir(path):
            sql_glob = os.path.join(path, '**/*.sql')
            sql_files = glob.iglob(sql_glob, recursive=True)

            files.extend(collect_files(sql_files))

        else:
            files.append((path, _slurp_file(path)))

    return files


def show_rule(name):
    """Print information about rule named ``name``."""
    color = {
        'bold': Style.BRIGHT,
        'reset': Style.RESET_ALL,
    }

    try:
        meta = rule.Registry.get_meta(name)
    except squabble.UnknownRuleException:
        sys.exit('{bold}Unknown rule:{reset} {name}'.format(**{
            'name': name,
            **color
        }))

    print('{bold}{name}{reset} - {description}\n\n{help}'.format(**{
        **meta,
        **color
    }))


def list_rules():
    """Print out all registered rules and brief description of what they do."""
    color = {
        'bold': Style.BRIGHT,
        'reset': Style.RESET_ALL,
    }

    all_rules = sorted(rule.Registry.all(), key=lambda r: r['name'])

    for meta in all_rules:
        print('{bold}{name: <32}{reset} {description}'.format(**{
            **color,
            **meta
        }))


def explain_message(code):
    """Print out the more detailed explanation of the given message code."""
    try:
        code = int(code)
        cls = squabble.message.Registry.by_code(code)
    except (ValueError, KeyError):
        sys.exit('{bold}Unknown message code:{reset} {code}'.format(
            bold=Style.BRIGHT,
            reset=Style.RESET_ALL,
            code=code
        ))

    print('{bold}{name}{reset}\n'.format(
        bold=Style.BRIGHT,
        reset=Style.RESET_ALL,
        name=cls.__name__
    ))

    print(cls.explain() or 'No additional info.', sep='')


def list_presets():
    """Print out all the preset configurations."""
    for name, preset in config.PRESETS.items():
        print('{bold}{name}{reset} - {description}'.format(
            name=name,
            description=preset.get('description', ''),
            bold=Style.BRIGHT,
            reset=Style.RESET_ALL
        ))

        # npm here i come
        left_pad = '    '
        cfg = json.dumps(preset['config'], indent=4)\
                  .replace('\n', '\n' + left_pad)
        print(left_pad + cfg)
