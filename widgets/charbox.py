
from . import Widget

class CharBox(Widget):
	
	def __init__(self, text=None):
		self.lines = []
		if text is not None:
			self.set_text(text)
	
	def set_text(self, text):
		self.lines = text.splitlines()
		self.change()
	
	def draw(self, target):
		lines = [line[:target.width-1] for line in self.lines][:target.height]
		for y, line in enumerate(lines):
			target.write(0, y, line)
		
			
