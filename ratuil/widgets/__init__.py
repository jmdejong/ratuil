



class Widget:
	
	_changed = True
	
	def change(self):
		self._changed = True
	
	def is_changed(self):
		return self._changed
	
	def unchange(self):
		self._changed = False
	
	def resize(self, screen):
		pass
	
	def update(self, target, force=False):
		if self.is_changed() or force:
			self.draw(target)
			self.unchange()
	
	@classmethod
	def from_xml(cls, children, attr, text):
		raise NotImplementedError
