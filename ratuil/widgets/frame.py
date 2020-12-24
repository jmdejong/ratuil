
from . import Widget
from ..textstyle import TextStyle
from ..strwidth import strwidth

class Frame(Widget):
	
	
	def __init__(self, attr):
		self.child = child
		self.vertchar = "|"
		self.horchar = "-"
		self.cornerchar = "+"
		self.style = TextStyle.from_str(attr.get("style"))
		char = attr.get("char")
		if char is not None:
			self.vertchar = char
			self.horchar = char
			self.cornerchar = char
		self.vertchar = attr.get("vertchar", self.vertchar)
		self.horchar = attr.get("horchar", self.horchar)
		self.cornerchar = attr.get("cornerchar", self.cornerchar)
		assert strwidth(self.horchar) == 1
		assert strwidth(self.vertchar) == 1
		assert strwidth(self.cornerchar) == 1
	
		
	def draw(self, target):
		target.write(0, 0, self.cornerchar + self.horchar * (target.width - 2) + self.cornerchar, self.style)
		target.write(0, target.height - 1, self.cornerchar + self.horchar * (target.width - 2) + self.cornerchar, self.style)
		for y in range(1, target.height - 1):
			target.write(0, y, self.vertchar, self.style)
			target.write(target.width-1, y, self.vertchar, self.style)

	@classmethod
	def from_xml(cls, children, attr, text):
		return cls(attr)
	
