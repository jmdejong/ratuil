
from .splitbox import SplitBox
from window import Window

class VBox(SplitBox):
	
	def resize(self, target):
		start = 0
		end = target.height
		for child in self.children:
			if start >= end:
				break
			height = end - start
			if child.box_style.height is not None:
				height = min(height, child.box_style.height.to_actual_value(target.height, height))
			if child.box_style.align_bottom:
				win = Window(target, 0, end - height, target.width, height)
				end -= height
			else:
				win = Window(target, 0, start, target.width, height)
				start += height
			child.resize(win)
