"""StartinBlox commit style parser"""

import re
from typing import Tuple
from semantic_release.errors import UnknownCommitMessageStyleError
from semantic_release.history.parser_helpers import parse_text_block

re_parser = re.compile(
    r'(?P<type>\w+)'
    r'(?:\((?P<scope>[\w _\-]+)\))?: '
    r'(?P<subject>[^\n]+)'
    r'(:?\n\n(?P<text>.+))?',
    re.DOTALL
)

TYPES = {
    'major': 'major',
    'minor': 'minor',
    'feature': 'feature',
    'update': 'update',
    'bugfix': 'bugfix',
    'ui': 'ui',
    'syntax': 'syntax',
    'other': 'other',
}

def parse_commit_message(message: str) -> Tuple[int, str, str, Tuple[str, str, str]]:
    """
    Parses a commit message according to the StartinBlox rules to define release
    :param message: A string of the commit message
    :return: A tuple of (level to bump, type of change, scope of change, a tuple with descriptions)
    :raises UnknownCommitMessageStyleError: if regular expression matching fails"""

    # parse message
    parsed = re_parser.match(message)
    if not parsed:
        raise  UnknownCommitMessageStyleError(
            'Unable to parse the given commit message: {}'.format(message)
        )

    # calculate release level
    level_bump = 0
    if parsed.group('type') == 'major':
        level_bump = max([level_bump, 3])

    elif parsed.group('type') == 'minor':
        level_bump = max([level_bump, 2])

    else:
        level_bump = 1

    body, footer = parse_text_block(parsed.group('text'))

    # set type to 'other' by default
    _type = TYPES['other']
    if parsed.group('type') in TYPES:
         _type = TYPES[parsed.group('type')]

    return (
        level_bump,
        _type,
        '',
        (parsed.group('subject'), body, footer)
    )
