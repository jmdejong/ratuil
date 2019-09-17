
from . import Widget

class SwitchBox(Widget):
	
	def __init__(self, children, etree):
		self.children = children
		self.selected = int(etree.attrib.get("selected", "0"))
	
	def select(self, selected):
		self.selected = selected
		self.change()
	
	def resize(self, target):
		start = 0
		end = target.width
		for child in self.children:
			child.resize(target)
	
	def update(self, force):
		if self.is_changed():
			force = True
			self.changed = False
		self.children[self.selected].update(force)
