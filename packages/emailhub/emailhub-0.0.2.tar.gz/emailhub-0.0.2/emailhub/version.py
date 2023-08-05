"""
EmailHub version file
"""
import io
import os

from emailhub.constants import PACKAGE_PATH

VERSION_FILE_NAME = "__version__"

with io.open(os.path.join(PACKAGE_PATH, VERSION_FILE_NAME)) as f:
    __version__ = f.readline().strip()
