import os
from typing import Any


def write_version(command: Any) -> None:
    version = command.egg_version

    version_path = os.path.join(os.path.dirname(__file__), 'version.py')

    with open(version_path, 'r') as fp:
        lines = fp.read().split('\n')

    for i, line in enumerate(lines):
        if line.startswith('__version__ ='):
            lines[i] = '__version__ = %r' % (version,)

    with open(version_path, 'w') as fp:
        fp.write('\n'.join(lines))
