
from . import Widget
from window import Window

class HBox(Widget):
	
	def __init__(self, children, separators):
		self.children = children
		self.separators = separators
	
	def resize(self, target):
		x = 0
		for i, child in enumerate(self.children):
			if x >= target.width:
				break
			if i < len(self.separators) and self.separators[i] is not None:
				end = min(x + self.separators[i], target.width)
			else:
				end = target.width
			win = Window(target, x, 0, end, target.height)
			x += end
			child.resize(win)
			child.update()
	
	def update(self, force=False):
		for child in self.children:
			child.update(force)
