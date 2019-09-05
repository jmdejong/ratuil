



class Widget:
	
	changed = True
	screen = None
	
	def change(self):
		self.changed = True
	
	def resize(self, screen):
		self.screen = screen
		self.change()
	
	def update(self, force=False):
		if (self.changed or force) and self.screen is not None:
			self.draw(self.screen)
