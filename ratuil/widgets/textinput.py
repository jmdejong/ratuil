
from . import Widget
from ..textstyle import TextStyle

class TextInput(Widget):
	
	def __init__(self):
		self.text = ""
		self.cursor = -1

	def set_text(self, text, cursor=-1):
		self.text = text
		self.cursor = cursor
		self.change()
	
	def draw(self, target):
		target.clear()
		target.write(0, 0, self.text[:target.width])
		if isinstance(self.cursor, int) and self.cursor >= 0 and self.cursor < target.width:
			
			if self.cursor < len(self.text):
				c = self.text[self.cursor]
			else:
				c = ' '
			target.write(self.cursor, 0, c, TextStyle(reverse=True))
	
	@classmethod
	def from_xml(cls, children, attr, text):
		return cls()
