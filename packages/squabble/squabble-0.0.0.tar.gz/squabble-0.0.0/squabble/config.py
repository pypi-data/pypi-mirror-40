import collections
import copy
import json
import os.path
import re
import subprocess

from squabble import logger, SquabbleException


Config = collections.namedtuple('Config', [
    'reporter',
    'plugins',
    'rules'
])


# TODO: Move these out somewhere else, feels gross to have them hardcoded.
DEFAULT_CONFIG = dict(
    reporter='plain',
    plugins=[],
    rules={}
)

PRESETS = {
    'postgres': {
        'description': ('A sane set of defaults that checks for obviously '
                        'dangerous Postgres migrations.'),
        'config': {
            'rules': {
                'AddColumnDisallowConstraints': {
                    'disallowed': ['DEFAULT', 'NOT NULL', 'UNIQUE']
                },
                'RequirePrimaryKey': {},
                'RequireConcurrentIndex': {},
                'DisallowRenameEnumValue': {},
                'DisallowChangeColumnType': {},
            }
        }
    }
}


class UnknownPresetException(SquabbleException):
    def __init__(self, preset):
        super().__init__('unknown preset: "%s"' % preset)


def discover_config_location():
    logger.debug('No config file given, trying to discover')

    possible_dirs = [
        '.',
        get_vcs_root(),
        os.path.expanduser('~')
    ]

    for d in possible_dirs:
        if d is None:
            continue

        logger.debug('Checking %s for a config file', d)

        file_name = os.path.join(d, '.squabblerc')
        if os.path.exists(file_name):
            return file_name

    return None


def get_vcs_root():
    return subprocess.getoutput(
        'git rev-parse --show-toplevel 2>/dev/null ||'
        'echo ""')


def get_base_config(preset_name=None):
    """Return a basic config value that can be overridden by users."""

    if not preset_name:
        return Config(**DEFAULT_CONFIG)

    if preset_name not in PRESETS:
        raise UnknownPresetException(preset_name)

    return Config(**{
        **DEFAULT_CONFIG,
        **PRESETS[preset_name]['config']
    })


def parse_config_file(config_file):
    if not config_file:
        return {}

    with open(config_file, 'r') as fp:
        return json.load(fp)


def load_config(config_file, preset_name=None):
    base = get_base_config(preset_name)
    config = parse_config_file(config_file)

    rules = copy.deepcopy(base.rules)
    for name, rule in config.get('rules', {}).items():
        rules[name] = rule

    return Config(
        reporter=config.get('reporter', base.reporter),
        plugins=config.get('plugins', base.plugins),
        rules=rules
    )


def apply_file_config(base, file_name):
    """
    Given a base configuration object and a file, return a new config that
    applies any file-specific rule additions/deletions
    """

    # Operate on a copy so we don't mutate the base config
    file_rules = copy.deepcopy(base.rules)

    rules = parse_file_rules(file_name)

    for rule, opts in rules['enable'].items():
        file_rules[rule] = opts

    for rule in rules['disable']:
        del file_rules[rule]

    return base._replace(rules=file_rules)


def parse_file_rules(file_name):
    with open(file_name, 'r') as fp:
        text = fp.read()

    return extract_file_rules(text)


def extract_file_rules(text):
    """
    Try to extract any file-level rule additions/suppressions.

    Valid lines are SQL line comments that enable or disable specific rules.

    >>> rules = extract_file_rules('...\\n-- enable:rule1 opt=foo arr=a,b,c')
    >>> rules == {'disable': [], 'enable': {'rule1': {'opt': 'foo', 'arr': ['a','b','c']}}}
    True
    """

    rules = {
        'enable': {},
        'disable': [],
    }

    comment_re = re.compile(r'--\s*(enable|disable):(\w+)(.*?)$', re.I)

    for line in text.splitlines():
        line = line.strip()

        m = re.match(comment_re, line)
        if m is None:
            continue

        action, rule, opts = m.groups()

        if action == 'disable':
            rules['disable'].append(rule)

        elif action == 'enable':
            rules['enable'][rule] = _parse_options(opts)

    return rules


def _parse_options(opts):
    """
    Given a string of space-separated `key=value` pairs, return a dictionary of
    `{"key": "value"}`. Note the value will always be returned as a string, and
    no further parsing will be attempted.

    >>> opts = _parse_options('k=v abc=1,2,3')
    >>> opts == {'k': 'v', 'abc': ['1', '2', '3']}
    True
    >>> _parse_options('k="1,2","3,4"')
    {'k': ['1,2', '3,4']}
    """

    options = {}

    # Either a simple quoted string or a bare value
    value = r'(?:(?:"([^"]+)")|([^,\s]+))'

    # Value followed by zero or more values
    value_list = r'{0}(?:,{0})*'.format(value)

    value_regex = re.compile(value)
    kv_regex = re.compile(r'(\w+)=({0})'.format(value_list))

    # 'k=1,2' => ('k', '1,2')
    for match in re.finditer(kv_regex, opts):
        key, val = match.group(1, 2)

        # value_regex will return ('string', '') or ('', 'value')
        values = [a or b for a, b in re.findall(value_regex, val)]

        # Collapse single len lists into scalars
        options[key] = values[0] if len(values) == 1 else values

    return options
