
from . import Widget
import textwrap

class TextBox(Widget):
	
	def __init__(self, children, etree):
		self.lines = []
		self.set_text(etree.text or "")
	
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
		
			
