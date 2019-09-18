
from . import Widget

class SplitBox(Widget):
	
	def __init__(self, children):
		self.children = children
	
	def is_changed(self):
		return False
	
	def resize(self, target):
		raise NotImplementedError
	
	def update(self, force=False):
		for child in self.children:
			child.update(force)
	
	@classmethod
	def from_xml(cls, children, tree):
		return cls(children)
