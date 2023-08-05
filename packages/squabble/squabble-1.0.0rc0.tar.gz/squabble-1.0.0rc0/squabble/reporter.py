# coding: utf-8

import functools
import json
import sys

import pglast
from colorama import Fore, Style

import squabble

_REPORTERS = {}


class UnknownReporterException(squabble.SquabbleException):
    """Raised when a configuration references a reporter that doesn't exist."""
    def __init__(self, name):
        super().__init__('unknown reporter: "%s"' % name)


def reporter(name):
    """
    Decorator to register function as a callback when the config sets the
    `"reporter"` config value to `name`.

    The wrapped function will be called with each
    :class:`squabble.lint.LintIssue` and the contents of the file
    being linted. Each reporter should return a list of lines of
    output which will be printed to stderr.

    >>> from squabble.lint import LintIssue
    >>> @reporter('no_info')
    ... def no_info(issue, file_contents):
    ...     return ['something happened']
    ...
    >>> no_info(LintIssue(), file_contents='')
    ['something happened']
    """
    def wrapper(fn):
        _REPORTERS[name] = fn

        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            return fn(*args, **kwargs)
        return wrapped

    return wrapper


def report(reporter_name, issues):
    """
    Call the named reporter function for every issue in the list of issues.
    """
    if reporter_name not in _REPORTERS:
        raise UnknownReporterException(reporter_name)

    reporter = _REPORTERS[reporter_name]
    files = {}

    for i in issues:
        # Cache the file contents
        if i.file is not None and i.file not in files:
            with open(i.file, 'r') as fp:
                files[i.file] = fp.read()

        file_contents = files.get(i.file, '')
        for line in reporter(i, file_contents):
            _print_err(line)


def _location_for_issue(issue):
    """
    Return the offset into the file for this issue, or None if it
    cannot be determined.
    """
    if issue.node and issue.node.location != pglast.Missing:
        return issue.node.location.value

    return issue.location


def _issue_to_file_location(issue, contents):
    """
    Given an issue (which may or may not have a :class:`pglast.Node` with a
    ``location`` field) and the contents of the file containing that
    node, return the ``(line_str, line, column)`` that node is located at,
    or ``('', 1, 0)``.

    :param issue:
    :type issue: :class:`squabble.lint.LintIssue`
    :param contents: Full contents of the file being linted, as a string.
    :type contents: str
    """
    loc = _location_for_issue(issue)

    if loc is None:
        return ('', 1, 0)

    lines = contents.splitlines()

    for i, line in enumerate(lines, start=1):
        if loc <= len(line):
            return (line, i, loc)

        # Add 1 to count the newline char.
        # TODO: won't work with \r\n
        loc -= len(line) + 1

    return ('', 1, 0)


def _print_err(msg):
    print(msg, file=sys.stderr)


def _format_message(issue):
    if issue.message_text:
        return issue.message_text

    return issue.message.format()


def _issue_info(issue, file_contents):
    """Return a dictionary of metadata for an issue."""
    line, line_num, column = _issue_to_file_location(issue, file_contents)
    formatted = _format_message(issue)

    return {
        'line_text': line,
        'line': line_num,
        'column': column,
        'message_formatted': formatted,
        **issue._asdict(),
        **(issue.message.asdict() if issue.message else {})
    }


_SIMPLE_FORMAT = '{file}:{line}:{column} {severity}: {message_formatted}'

# Partially pre-format the message since the color codes will be static.
_COLOR_FORMAT = '{bold}{{file}}:{reset}{{line}}:{{column}}{reset} '\
    '{red}{{severity}}{reset}: {{message_formatted}}'\
    .format(bold=Style.BRIGHT, red=Fore.RED, reset=Style.RESET_ALL)


@reporter("plain")
def plain_text_reporter(issue, file_contents):
    """Simple single-line output format that is easily parsed by editors."""
    info = _issue_info(issue, file_contents)
    return [
        _SIMPLE_FORMAT.format(**info)
    ]


@reporter('color')
def color_reporter(issue, file_contents):
    """
    Extension of :func:`squabble.reporter.plain_text_reporter`, uses
    ANSI color and shows error location.
    """
    info = _issue_info(issue, file_contents)

    output = [_COLOR_FORMAT.format(**info)]

    if 'message_code' in info:
        output[0] += ' [{message_code}]'.format(**info)

    if info['line_text'] != '':
        arrow = ' ' * info['column'] + '^'
        output.append(info['line_text'])
        output.append(Style.BRIGHT + arrow + Style.RESET_ALL)

    return output


@reporter('json')
def json_reporter(issue, _file_contents):
    """Dump each issue as a JSON dictionary"""

    # pglast nodes aren't JSON serializable
    if issue.node:
        issue = issue._replace(node=issue.node.parse_tree)

    if issue.message:
        issue = issue.replace(message=issue.message.asdict())

    obj = {
        k: v for k, v in issue._asdict().items()
        if v is not None
    }

    return [
        json.dumps(obj)
    ]
