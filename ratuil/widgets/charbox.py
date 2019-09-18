
from . import Widget

class CharBox(Widget):
	
	def __init__(self, text=""):
		self.lines = []
		self.set_text(text)
	
	def set_text(self, text):
		self.lines = text.splitlines()
		self.change()
	
	def draw(self, target):
		target.clear()
		lines = [line[:target.width] for line in self.lines][:target.height]
		for y, line in enumerate(lines):
			target.write(0, y, line)
	
	@classmethod
	def from_xml(cls, children, attr, text):
		return cls(text or "")
	
		
			
