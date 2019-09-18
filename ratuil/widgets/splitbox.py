
from . import Widget

class SplitBox(Widget):
	
	def __init__(self, children):
		self.children = children
	
	def resize(self, target):
		raise NotImplementedError
	
	def update(self, target, force=False):
		for child in self.children:
			child.update(force)
	
	@classmethod
	def from_xml(cls, children, attr, text):
		return cls(children)
