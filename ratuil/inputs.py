
import sys
import string

BEFORE_LETTERS = ord('A') - 1

def name_char(char):
	n = ord(char)
	if n > 31 and n != 127:
		return char
	if n == 8 or n == 127:
		return "backspace"
	if n == 10 or n == 13:
		return "enter"
	if n > 0 and n <= 26:
		return "^" + chr(n + BEFORE_LETTERS)
	return "chr({})".format(n)

def get_key(stream=sys.stdin, combine_escape=True, do_interrupt=False):
	char = stream.read(1)
	if do_interrupt and ord(char) == 3:
		raise KeyboardInterrupt
	if ord(char) == 27:
		if not combine_escape:
			return "escape"
		nextchar = stream.read(1)
		while ord(nextchar) == 27: # avoid deep recursion
			nextchar = stream.read(1)
		if nextchar != "[":
			return "\\e" + name_char(nextchar)
		rest = ""
		last = "\0"
		while last not in string.ascii_letters + "~":
			last = stream.read(1)
			rest += last
		if rest == "A":
			return "up"
		elif rest == "B":
			return "down"
		elif rest == "C":
			return "right"
		elif rest == "D":
			return "left"
		else:
			return "\\e[" + rest
	else:
		return name_char(char)
		
	
