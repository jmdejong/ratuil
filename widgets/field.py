
from . import Widget
from pad import Pad

class Field(Widget):
	
	
	def __init__(self, children, etree):
		width = int(etree.attrib.get("width", 0))
		height = int(etree.attrib.get("height", 0))
		char_size = int(etree.attrib.get("char-size", 1))
		self.pad = Pad(width, height, char_size)
		self.char_size = char_size
		self.center = (0, 0)
		self.changed = False
		self.redraw = False
	
	def set_size(self, width, height):
		self.pad.resize(width, height)
		self.redraw = True
		self.change()
	
	def change_cell(self, x, y, char, style=None):
		""" sprites must always have at least one element """
		if x < 0 or y < 0 or x >= self.width or y >= self.height:
			return
		self.pad.write(x, y, char, style)
		self.change()
	
	def set_center(self, x, y):
		self.center = (x, y)
		self.change()
	
	@property
	def width(self):
		return self.pad.width
	
	@property
	def height(self):
		return self.pad.height
	
	def _round_width(self, x):
		return x // self.char_size * self.char_size
	
	def draw(self, target):
		center_x, center_y = self.center
		target.draw_pad(
			self.pad,
			src_x = max(0, min(
				self._round_width(self.width - target.width // self.char_size),
				self._round_width(center_x * self.char_size - target.width // 2)
			)),
			src_y = max(0, min(self.height - target.height, center_y - target.height // 2))
		)
