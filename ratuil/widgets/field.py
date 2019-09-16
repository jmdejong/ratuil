
from . import Widget
from ..pad import Pad

class Field(Widget):
	
	
	def __init__(self, children, etree):
		self.width = 0
		self.height = 0
		self.char_size = int(etree.attrib.get("char-size", 1))
		self.pad = Pad(self.width * self.char_size, self.height)
		self.center = (0, 0)
		self.changed = False
		self.redraw = False
	
	def set_size(self, width, height):
		self.width = width
		self.height = height
		self.pad.resize(width * self.char_size, height)
		self.redraw = True
		self.change()
	
	def change_cell(self, x, y, char, style=None):
		if x < 0 or y < 0 or x >= self.width or y >= self.height:
			return
		self.pad.write(x * self.char_size, y, char, style)
		self.change()
	
	def set_center(self, x, y):
		self.center = (x, y)
		self.change()
	
	
	def _round_width(self, x):
		return x // self.char_size * self.char_size
	
	def draw(self, target):
		center_x, center_y = self.center
		target.draw_pad(
			self.pad,
			src_x = max(0, min(
				self._round_width(self.pad.width - target.width),
				self._round_width(center_x * self.char_size - target.width // 2)
			)),
			src_y = max(0, min(self.pad.height - target.height, center_y - target.height // 2)),
			width = self._round_width(target.width)
		)
