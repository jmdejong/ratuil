
from . import Widget
import textwrap

class TextBox(Widget):
	
	def __init__(self, text=None):
		self.lines = []
		if text is not None:
			self.set_text(text)
	
	def set_text(self, text):
		self.lines = text.splitlines()
		self.change()
	
	def draw(self, target):
		lines = []
		for line in self.lines:
			lines.extend(textwrap.wrap(line, target.width))
		
		for y, line in enumerate(lines):
			target.write(0, y, line)
		
			
