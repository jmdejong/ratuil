
from . import Widget

class Listing(Widget):
	
	def __init__(self, children, etree):
		if etree.text is not None:
			self.items = [line.strip() for line in etree.text.splitlines() if line.strip()]
		else:
			self.items = []
		self.selector = int(etree.attrib.get("select", "0"))
		self.selector_char = etree.attrib.get("selector", "*")
	
	def set_items(self, items):
		self.items = items
		self.change()
	
	def select(self, index):
		self.selector = index
		self.change()
	
	def draw(self, target):
		target.clear()
		width = target.width
		height = target.height
		
		start = min(self.selector - height//2, len(self.items) - height)
		start = max(start, 0)
		end = start + height
		#win.erase()
		for i, item in enumerate(self.items[start:end]):
			if i + start == self.selector:
				target.write(0, i, self.selector_char)
			target.write(len(self.selector_char), i, item)
		if end < len(self.items):
			target.write(width-1, height-1, "+")
		if start > 0:
			target.write(width-1, 0, "-")
		
