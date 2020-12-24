
import sys
import shutil
import tty
import termios

from ..screen import Screen
from ..window import Window
from ..pad import Pad
from ..layout import Layout

class DrawBackend():
	
	def __init__(self):
		self.oldterm = None
		self.fd = None
	
	def create_window(self, target, x=0, y=0, width=None, height=None):
		return Window(target, x, y, width, height)

	def create_pad(self, width, height):
		return Pad(width, height)

	def create_screen(self, *args, **kwargs):
		return Screen(*args, **kwargs)

	def initialize_terminal(self):
		self.fd = sys.stdin.fileno()
		self.oldterm = termios.tcgetattr(self.fd)
		tty.setraw(sys.stdin)
		Screen.default.hide_cursor()

	def finalize_terminal(self):
		if self.oldterm is not None and self.fd is not None:
			termios.tcsetattr(self.fd, termios.TCSADRAIN, self.oldterm)
		Screen.default.finalize()

	def layout(self, *args, **kwargs):
		return Layout(self, *args, **kwargs)
	
	def layout_from_xml_str(self, *args, **kwargs):
		return Layout.from_xml_str(self, *args, **kwargs)
	
	def layout_from_xml_file(self, *args, **kwargs):
		return Layout.from_xml_file(self, *args, **kwargs)

