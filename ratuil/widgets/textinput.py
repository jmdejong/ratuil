
from . import Widget
from ..textstyle import TextStyle

class TextInput(Widget):
	
	def __init__(self, children, etree):
		self.text = ""
		self.cursor = -1

	def set_text(self, text, cursor=-1):
		self.text = text
		self.cursor = cursor
		self.change()
	
	def draw(self, target):
		target.clear()
		target.write(0, 0, self.text[:target.width])
		if isinstance(self.cursor, int) and self.cursor >= 0 and self.cursor <= len(self.text):
			target.write(min(self.cursor, target.width - 1), 0, self.text[self.cursor], TextStyle(reverse=True))
