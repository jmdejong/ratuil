

import unicodedata

# taken from textwrap
_whitespace = '\t\n\x0b\x0c\r '

#class WideString:
	
	#def __init__(self, text):
		#self.text = text



def charwidth(char):
	eaw = unicodedata.east_asian_width(char)
	if eaw == "Na" or eaw == "H":
		return 1
	if eaw == "F" or eaw == "W":
		return 2
	if eaw == "A":
		return 1
	if eaw == "N":
		return 1
	raise Exception("unknown east easian width for character {}: {}".format(ord(char), char))

def strwidth(text):
	return sum(charwidth(ch) for ch in text)


def width(text):
	return stringwidth(text)
	
def width_index(text, width):
	""" The largest index i for which the string is smaller than or equal to width """
	l = 0
	for i, char in enumerate(text):
		w = charwidth(char)
		if l + w > width:
			return i
		l += w
	return len(text)
	
def crop(text, width):
	return text[:width_index(text, width)]
	
	#def split(self, *args, **kwargs):
		#return [WideString(word) for word in self.text.split(*args, **kwargs)]
	
	#def splitlines(self, *args, **kwargs):
		#return [WideString(line) for line in self.text.splitlines(*args, **kwargs)]

def wrap(text, width, separators=None):
	lines = []
	for line in text.splitlines():
		while line:
			cutoff = width_index(line, width)
			if separators is not None:
				last_sep = max(line.rfind(c, 0, cutoff) for c in separators)
				if last_sep > 0:
					cutoff = last_sep
			lines.append(line[:cutoff])
			line = line[cutoff+1:]
	return lines

def wrap_words(text, width):
	return wrap(text, width, separators=_whitespace)

		#lines = []
		#line = lines
		#words = self.split()
		#while True:
			#wi = width_index(text, width)
		#l = 0
		#last_sep = None
		#for i, char in enumerate(self.text):
			#w = charwidth(char)
			#if l + w > width:
				#return i
			#l += w
			
