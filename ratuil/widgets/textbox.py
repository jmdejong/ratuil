
from . import Widget
import textwrap

class TextBox(Widget):
	
	def __init__(self, text="", wrap=None):
		self.lines = []
		self.set_text(text)
		if wrap is None or wrap == "":
			wrap = "crop"
		assert wrap in {"crop", "words"}
		self.wrap = wrap
	
	def set_text(self, text):
		self.lines = text.splitlines()
		self.change()
	
	def draw(self, target):
		target.clear()
		if self.wrap == "crop":
			lines = [line[:target.width] for line in self.lines][:target.height]
		elif self.wrap == "words":
			lines = []
			for line in self.lines:
				lines.extend(textwrap.wrap(line, target.width))
		
		for y, line in enumerate(lines[:target.height]):
			target.write(0, y, line)
	
	@classmethod
	def from_xml(cls, children, attr, text):
		wrap = attr.get("wrap")
		return cls((text or "").strip(), wrap)
