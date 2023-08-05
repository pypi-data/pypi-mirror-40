#!/usr/bin/env python3
## Public domain
# See https://unlicense.org and UNLICENSE.txt
__license__ = "Unlicense"
__docformat__ = "reStructuredText"

from .bg import *

def run():
	"""Run this module.

	:returns: Nothing
	:rtype: none
	.. todo::Implement this.
	"""
	session_bus = pydbus.SessionBus()
	control = controlBus()
	session_bus.publish("moe.hattshire.bg", control)

	mainloop = GLib.MainLoop()
	mainloop.run()

