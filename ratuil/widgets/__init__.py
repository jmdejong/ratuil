



class Widget:
	
	changed = True
	screen = None
	box_style = None
	
	def change(self):
		self.changed = True
	
	def set_box_style(self, style):
		self.box_style = style
	
	def is_changed(self):
		return self.changed
	
	def resize(self, screen):
		self.screen = screen
		self.change()
	
	def update(self, force=False):
		if (self.is_changed() or force) and self.screen is not None:
			self.draw(self.screen)
			self.changed = False
	
	@classmethod
	def from_xml(cls, children, tree):
		raise NotImplementedError
