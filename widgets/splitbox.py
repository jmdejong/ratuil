
from . import Widget

class SplitBox(Widget):
	
	def __init__(self, children, etree):
		self.children = children
		self.etree = etree
		#self.separators = [Value.parse(separator) for separator in separators]
	
	def is_changed(self):
		return False
		#return any(child.is_changed() for child in self.children)
	
	def resize(self, target):
		raise NotImplementedError
	
	def update(self, force=False):
		for child in self.children:
			child.update(force)
