
from . import Widget
from .. textstyle import TextStyle
from .. import util

class Bar(Widget):
	
	def __init__(self, children, etree):
		self.title = etree.attrib.get("title", "")
		self.full_char = etree.attrib.get("full-char", "#")
		self.empty_char = etree.attrib.get("empty-char", " ")
		assert util.strwidth(self.full_char) == util.strwidth(self.empty_char) == 1
		self.full_style = TextStyle.from_str(etree.attrib.get("full-style", ""))
		self.empty_style = TextStyle.from_str(etree.attrib.get("empty-style", ""))
		self.total = int(etree.attrib.get("total", "-1"))
		self.filled = int(etree.attrib.get("filled", "0"))
		self.header = etree.attrib.get("header", "{title} ({filled}/{total})")
		
	
	def set_total(self, total):
		self.total = total
		self.change()
	
	def set_filled(self, filled):
		self.filled = filled
		self.change()
	
	def draw(self, target):
		target.clear()
		width = target.width
		height = target.height
		
		bar_end = round(self.filled / self.total * width) if self.total > 0 else 0
		target.write(0, 0, self.header.format(title=self.title, filled=self.filled, total=self.total)[:width])
		target.write(0, 1, self.full_char * bar_end , self.full_style)
		target.write(bar_end, 1, self.empty_char[0]*(width - bar_end), self.empty_style)
