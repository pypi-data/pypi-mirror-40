#!/usr/bin/env python
from cleo import Application

from . import __version__
from .commands import ListCommand

application = Application("licencia", __version__, complete=True)
application.add(ListCommand())
