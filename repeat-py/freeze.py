# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "setuptools",
#     "py2exe",
# ]
# ///

import os

import py2exe  # noqa: F401

# Run from anywhere
import os.path
import sys
path = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
sys.path.insert(0, path)
os.chdir(path)

bootstrap = py2exe.runtime.Runtime.bootstrap_modules
bootstrap.remove('encodings.*')
bootstrap.add('encodings.utf_8')
bootstrap.add('encodings.cp1252')

try:
    os.replace('repeat.exe', 'old.exe')
except FileNotFoundError:
    pass
except OSError:
    os.remove('repeat.exe')

py2exe.freeze(
    console=['repeat.py'],
    zipfile=None,
    options={
        'dist_dir': '.',
        'bundle_files': 0,
        # Fast startup
        'compressed': 0,
        'optimize': 2,
        # Minimum filesize
        'dll_excludes': ['w9xpopen.exe', 'libcrypto-1_1.dll'],
        'excludes': [
            # Importlib
            'importlib._bootstrap_external',
            'importlib._bootstrap',
            'importlib.metadata',
            'importlib.readers',
            # Big modules
            'typing',
            'unicodedata',
            # Everything else
            '_py_abc',
            '_threading_local',
            'bz2',
            'collections.abc',
            'copy',
            'difflib',
            'doctest',
            'encodings.mbcs',
            'heapq',
            'inspect',
            'linecache',
            'lzma',
            'pdb',
            'pickle',
            'select',
            'selectors',
            'string',
            'tarfile',
            'token',
            'tokenize',
            'traceback',
            'tracemalloc',
            'unittest',
            'weakref',
            'zipfile',
            'zipimport',
            'zlib',
        ],
    },
)
