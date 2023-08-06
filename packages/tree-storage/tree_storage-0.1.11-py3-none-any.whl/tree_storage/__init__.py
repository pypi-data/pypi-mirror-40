"""
Tree Hash Storage

Tree hash-storage of a large number of files

Tree it is the library for who wants to save
a large number of files. For preservation
it is enough to you to transfer a binary code
of the file and the Tree will keep him.

:copyright: Copyright 2018-2019 Valerii Duz.
:license: MIT, see LICENSE for details.
"""

import sys

from tree_storage.__version__ import VERSION
from tree_storage.tree import TreeStorage
from tree_storage import utils

if sys.version_info.major < 3:
    raise RuntimeError(
        'Tree does not support Python 2.x. '
        'Please use Python 3.')

__title__ = 'tree-storage'
__author__ = 'Valerii Duz'
__license__ = 'MIT'
__version__ = VERSION
__copyright__ = 'Copyright 2019 ValeriiDuz'
