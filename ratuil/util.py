

import unicodedata

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
