
from . import Widget
from window import Window
from textstyle import TextStyle

class Border(Widget):
	
	
	def __init__(self, children, etree):
		assert len(children) == 1
		self.child = children[0]
		self.vertchar = "|"
		self.horchar = "-"
		self.cornerchar = "+"
		self.style = TextStyle.from_str(etree.attrib.get("style"))
		char = etree.attrib.get("char")
		if char is not None:
			self.vertchar = char
			self.horchar = char
			self.cornerchar = char
		self.vertchar = etree.attrib.get("vertchar", self.vertchar)
		self.horchar = etree.attrib.get("horchar", self.horchar)
		self.cornerchar = etree.attrib.get("cornerchar", self.cornerchar)
		assert len(self.horchar) == 1
		assert len(self.vertchar) == 1
		assert len(self.cornerchar) == 1
	
	def resize(self, target):
		self.screen = target
		win = Window(target, 1, 1, target.width - 2, target.height - 2)
		self.child.resize(win)
		self.change()
	
	def update(self, force=False):
		if (self.is_changed() or force) and self.screen is not None:
			#raise Exception(self.is_changed(), self.screen)
			self.draw(self.screen)
			self.changed = False
		self.child.update(force)
		
	def draw(self, target):
		target.write(0, 0, self.cornerchar + self.horchar * (target.width - 2) + self.cornerchar, self.style)
		target.write(0, target.height - 1, self.cornerchar + self.horchar * (target.width - 2) + self.cornerchar, self.style)
		for y in range(1, target.height - 1):
			target.write(0, y, self.vertchar, self.style)
			target.write(target.width-1, y, self.vertchar, self.style)
