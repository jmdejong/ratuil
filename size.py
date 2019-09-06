

class Value:
	
	
	def __init__(self, val=0, relative=False):
		self.val = val
		self.relative = relative
	
	def to_actual_value(self, available_size):
		value = self.val
		if self.relative:
			value *= available_size
		return int(value)
	
	@classmethod
	def parse(self, text):
		text = str(text) # in case someone would enter a number
		text = "".join(text.split()) # remove whitespace
		if not text:
			return None
		relative = False
		modifier = 1
		if text[-1] == "/":
			relative = True
			text = text[:-1]
		elif text[-1] == "%":
			relative = True
			text = text[:-1]
			modifier = 0.01
		if not text:
			return None
		if '.' in text:
			val = float(text)
		else:
			val = int(text)
		return Value(val * modifier, relative)


#class Size:
	
	#def __init__(self, begin=None, end=None, length=None):
		#self.begin = begin
		#self.end = end
		#self.length = length
	
	#def get_size(self, minimum, maximum):
		#available_size = maximum - minimum
		#if self.begin is not None:
			#begin = self.begin.to_actual_value(available_size)
		#else:
			#begin = 0
		
		#if self.end is not None:
			#end = self.end.to_actual_value(available_size)
		#elif self.length is not None:
			#end = self.begin + self.length.to_actual_value(available_size)
		#else:
			#end = available_size
		
		#return (begin + minimum, end + minimum)
		
