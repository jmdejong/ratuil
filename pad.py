
from style import Style
from constants import INT_INFINITY
from drawtarget import DrawTarget


class Pad(DrawTarget):
	
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.clear()
	
	def resize(self, width, height):
		self.width = width
		self.height = height
		self.clear()
	
	def fill(self, value):
		self.data = [value for i in range(self.width*self.height)]
	
	def clear(self):
		self.fill(None)
	
	def write(self, x, y, text, style=None):
		if style is None:
			style = Style.default
		if y >= self.height:
			return
		for i, char in enumerate(text):
			if x + i >= self.width:
				break
			self.data[x+i+y*self.width] = (style, char)
	
	
	def get(self, x, y):
		if y >= self.height or x >= self.width:
			return None
		return self.data[x + y * self.width]
	
	def get_line(self, x, y, length=None):
		if length is None:
			length = self.width - x
		if x >= self.width:
			return []
		start = x + y * self.width
		return self.data[start:start+length]
	
	def draw_pad(self, src, dest_x=0, dest_y=0, width=INT_INFINITY, height=INT_INFINITY, src_x=0, src_y=0):
		dest = self
		width = min(dest.width - dest_x, src.width - src_x)
		height = min(dest.height - dest_y, src.height - src_y)
		for y in range(height):
			for x, cell in enumerate(src.get_line(src_x, y, width)):
				if cell is not None:
					style, char = cell
					self.write(x, y, char, style)
