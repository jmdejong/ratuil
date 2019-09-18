
from .splitbox import SplitBox
from ..window import Window

class VBox(SplitBox):
	
	def resize(self, target):
		if target is None:
			for child in self.children:
				child.resize(None)
			return
		start = 0
		end = target.height
		for child in self.children:
			if start >= end:
				child.resize(None)
				continue
			height = end - start
			if child.box_style.height is not None:
				height = min(height, child.box_style.height.to_actual_value(target.height, height))
			if height <= 0:
				child.resize(None)
				continue
			if child.box_style.align_bottom:
				win = Window(target, 0, end - height, target.width, height)
				end -= height
			else:
				win = Window(target, 0, start, target.width, height)
				start += height
			child.resize(win)
