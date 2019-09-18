
from .splitbox import SplitBox
from ..window import Window

class HBox(SplitBox):
	
	def resize(self, target):
		if target is None:
			for child in self.children:
				child.resize(None)
			return
		start = 0
		end = target.width
		for child in self.children:
			if start >= end:
				child.resize(None)
				continue
			width = end - start
			if child.box_style.width is not None:
				width = min(width, child.box_style.width.to_actual_value(target.width, width))
			if width <= 0:
				child.resize(None)
				continue
			if child.box_style.align_right:
				win = Window(target, end - width, 0, width, target.height)
				end -= width
			else:
				win = Window(target, start, 0, width, target.height)
				start += width
			child.resize(win)
