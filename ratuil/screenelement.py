
from .boxstyle import BoxStyle

class ScreenElement:
	
	def __init__(self, widget, attr):
		self.widget = widget
		self.style = BoxStyle.from_attrs(attr)
		self.id = attr.get("id")
		self.key = attr.get("key")
	
	# temporary; until I changed all box_style into style
	@property
	def box_style(self):
		return self.style
	
	def resize(self, target):
		if target is not None and (target.width <= 0 or target.height <= 0):
			target = None
		self.target = target
		self.widget.resize(target)
	
	def update(self, force):
		if self.target:
			self.widget.update(self.target, force)
