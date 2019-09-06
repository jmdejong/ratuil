
from .splitbox import SplitBox
from window import Window
from size import Value

class HBox(SplitBox):
	
	def resize(self, target):
		start = 0
		end = target.width
		for childtree, child in zip(self.etree, self.children):
			childattr = childtree.attrib
			if start >= end:
				break
			width = end - start
			if "width" in childattr:
				width = min(width, Value.parse(childattr["width"]).to_actual_value(width))
			if "right" in childattr.get("align", "").casefold():
				win = Window(target, end - width, 0, width, target.height)
				end -= width
			else:
				win = Window(target, start, 0, width, target.height)
				start += width
			child.resize(win)
			#child.update()
