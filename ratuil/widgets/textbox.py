
from . import Widget
from ..strwidth import wrap, wrap_words

class TextBox(Widget):
	
	def __init__(self, text="", wrap=None):
		self.lines = []
		self.set_text(text)
		if wrap is None or wrap == "":
			wrap = "crop"
		assert wrap in {"crop", "words", "chars"}
		self.wrap = wrap
	
	def set_text(self, text):
		self.lines = text.splitlines()
		self.change()
	
	def draw(self, target):
		target.clear()
		lines = []
		if self.wrap == "crop":
			lines = [line[:target.width] for line in self.lines][:target.height]
		elif self.wrap == "chars":
			for line in self.lines:
				lines.extend(wrap(line, target.width))
		elif self.wrap == "words":
			for line in self.lines:
				lines.extend(wrap_words(line, target.width))
		
		for y, line in enumerate(lines[:target.height]):
			target.write(0, y, line)
	
	@classmethod
	def from_xml(cls, children, attr, text):
		wrap = attr.get("wrap")
		return cls((text or "").strip(), wrap)
