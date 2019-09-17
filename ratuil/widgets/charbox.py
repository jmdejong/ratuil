
from . import Widget

class CharBox(Widget):
	
	def __init__(self, children, etree):
		self.lines = []
		self.set_text(etree.text or "")
	
	def set_text(self, text):
		self.lines = text.splitlines()
		self.change()
	
	def draw(self, target):
		lines = [line[:target.width] for line in self.lines][:target.height]
		for y, line in enumerate(lines):
			target.write(0, y, line)
		
			
