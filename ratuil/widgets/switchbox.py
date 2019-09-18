
from . import Widget

class SwitchBox(Widget):
	
	def __init__(self, children, etree):
		self.children = children
		try:
			self.selected = int(etree.attrib.get("selected", "0"))
		except ValueError:
			self.select(etree.attrib.get(selected))
	
	def select(self, selected):
		if isinstance(selected, str):
			key = selected.casefold()
			for i, child in enumerate(self.children):
				if child.box_style.key == key:
					selected = i
					break
		self.selected = selected
		self.change()
	
	def resize(self, target):
		for child in self.children:
			child.resize(target)
	
	def update(self, force):
		if self.is_changed():
			force = True
			self.changed = False
		self.children[self.selected].update(force)
