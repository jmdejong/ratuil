
from . import Widget
import textwrap

class TextBox(Widget):
	
	def __init__(self, text=""):
		self.lines = []
		self.set_text(text)
	
	def set_text(self, text):
		self.lines = text.splitlines()
		self.change()
	
	def draw(self, target):
		target.clear()
		lines = []
		for line in self.lines:
			lines.extend(textwrap.wrap(line, target.width))
		
		for y, line in enumerate(lines[:target.height]):
			target.write(0, y, line)
	
	@classmethod
	def from_xml(cls, children, attr, text):
		return cls(text.strip() or "")
