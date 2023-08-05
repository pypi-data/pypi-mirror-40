from os import path

from . import version
from .errors import CannotReadFileError

try:
    __version__ = version.read(path.dirname(__file__))
except CannotReadFileError:
    # VERSION file was not created yet
    __version__ = '0.dev0'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)
