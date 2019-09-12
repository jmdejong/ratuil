
from .splitbox import SplitBox
from window import Window
from size import Value

class VBox(SplitBox):
	
	def resize(self, target):
		start = 0
		end = target.height
		for childtree, child in zip(self.etree, self.children):
			childattr = childtree.attrib
			if start >= end:
				break
			height = end - start
			if "height" in childattr:
				height = min(height, Value.parse(childattr["height"]).to_actual_value(height))
			if "bottom" in childattr.get("align", "").casefold():
				win = Window(target, 0, end - height, target.width, height)
				end -= height
			else:
				win = Window(target, 0, start, target.width, height)
				start += height
			child.resize(win)
			#child.update(force=True)
