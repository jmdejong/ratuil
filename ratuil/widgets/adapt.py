
from . import Widget

class Adapt(Widget):
	
	def __init__(self, children, selected=0):
		self.layouts = []
		self.replacements = {}
		for child in self.children:
			if isinstance(child.widget, Layout):
				self.layouts.append(child)
			elif child.key is not None:
				self.replacements[child.key] = child
			else:
				raise ValueError("children of Adapt element should be Layout elements or have a key")
	
	def resize(self, target):
		for child in self.layouts:
			if child.widget.match_size(target.width, target.height
	
	def update(self, target, force):
		if self.is_changed():
			force = True
			self.unchange()
		return self.children[self.selected].update(force) or force
	
	
	@classmethod
	def from_xml(cls, children, attr, text):
		return cls(children, attr.get("selected", int(attr.get("selected-val", 0))))
