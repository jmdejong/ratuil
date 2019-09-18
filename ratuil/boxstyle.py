

from enum import Enum



class Relativity(Enum):
	ABSOLUTE = 0
	RELATIVE = 1
	VERY_RELATIVE = 2

class Value:
	
	
	def __init__(self, val=0, relative=Relativity.ABSOLUTE):
		self.val = val
		self.relative = relative
	
	def to_actual_value(self, available_size, remaining_size):
		value = self.val
		if self.relative == Relativity.VERY_RELATIVE:
			value *= remaining_size
		elif self.relative == Relativity.RELATIVE:
			value *= available_size
		return int(value)
	
	@classmethod
	def parse(self, text):
		text = str(text) # in case someone would enter a number
		text = "".join(text.split()) # remove whitespace
		if not text:
			return None
		relative = Relativity.ABSOLUTE
		modifier = 1
		if text[-1] == "/":
			relative = Relativity.RELATIVE
			text = text[:-1]
			if text[-1] == "/":
				relative = Relativity.VERY_RELATIVE
				text = text[:-1]
		elif text[-1] == "%":
			relative = Relativity.RELATIVE
			text = text[:-1]
			modifier = 0.01
			if text[-1] == "%":
				relative = Relativity.VERY_RELATIVE
				text = text[:-1]
		if not text:
			return None
		if '.' in text:
			val = float(text)
		else:
			val = int(text)
		return Value(val * modifier, relative)


class BoxStyle():
	
	LEFT = "left"
	RIGHT = "right"
	TOP = "top"
	BOTTOM = "bottom"
	
	def __init__(self, width=None, height=None, align_right=False, align_bottom=False, granularity=1, key=None):
		self.width = width
		self.height = height
		self.granularity = granularity
		self.align_right = align_right
		self.align_bottom = align_bottom
		if isinstance(key, str):
			key = key.casefold()
		self.key = key
	
	
	@classmethod
	def from_attrs(self, attrs):
		width = Value.parse(attrs.get("width", ""))
		height = Value.parse(attrs.get("height", ""))
		granularity = int(attrs.get("granularity", "1"))
		align_right = ("right" in attrs.get("align", "").casefold() or "right" in attrs.get("hor-align", "").casefold())
		align_bottom = ("bottom" in attrs.get("align", "").casefold() or "bottom" in attrs.get("vert-align", "").casefold())
		key = attrs.get("key")
		return BoxStyle(width, height, align_right, align_bottom, granularity, key)
