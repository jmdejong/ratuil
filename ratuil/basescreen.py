

from .window import Window
from .layout import Layout
from .drawtarget import DrawTarget
from .constants import INT_INFINITY

class BaseScreen(DrawTarget):
	
	def create_window(self, target, x=0, y=0, width=None, height=None):
		return Window(target, x, y, width, height)

	def create_pad(self, width, height):
		raise NotImplementedError()

	def initialize_terminal(self):
		raise NotImplementedError()

	def finalize_terminal(self):
		raise NotImplementedError()

	def get_key(self):
		raise NotImplementedError()

	def update_size(self):
		raise NotImplementedError()
		
	def write(self, x, y, text, style=None):
		raise NotImplementedError()
	
	def clear(self):
		raise NotImplementedError()
	
	def reset(self):
		self.update_size()
		self.clear()
	
	def draw_pad(self, pad, scr_x=0, scr_y=0, width=INT_INFINITY, height=INT_INFINITY, pad_x=0, pad_y=0):
		raise NotImplementedError()
	
	def update(self):
		raise NotImplementedError()
