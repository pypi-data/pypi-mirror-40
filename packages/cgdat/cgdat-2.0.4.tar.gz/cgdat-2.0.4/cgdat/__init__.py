"""
This package contains a simple GUI for analysing csv game data. It contains the DataAnalyserGUI gui class and
all the modules and functions that are used in creating this class.
"""

### Set all ###
__all__ = ['qt_ui', 'qt_custom', 'cgdat']

### Import submodules ###
from . import qt_ui
from . import qt_custom
from . import cgdat
from .cgdat import *
