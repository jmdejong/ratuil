
from .splitbox import SplitBox

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
			width = min(width, child.style.get_width(target.width, width))
			if child.style.align_right:
				win = self.backend.create_window(target, end - width, 0, width, target.height)
				end -= width
			else:
				win = self.backend.create_window(target, start, 0, width, target.height)
				start += width
			child.resize(win)
