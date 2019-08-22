#!/usr/bin/env -S python3 -u

import sys
import shutil
import io
import signal

INT_INFINITY = 2**64

class Attr:
	
	RESET = "0"
	BOLD = "1"
	UNDERSCORE = "4"
	BLINK = "5"
	REVERSE = "7"
	CONCEALED = "8"
	
	FG_BLACK = "30"
	FG_RED = "31"
	FG_GREEN = "32"
	FG_YELLOW = "33"
	FG_BLUE = "34"
	FG_MAGENTA = "35"
	FG_CYAN = "36"
	FG_WHITE = "37"
	
	BG_BLACK = "40"
	BG_RED = "41"
	BG_GREEN = "42"
	BG_YELLOW = "43"
	BG_BLUE = "44"
	BG_MAGENTA = "45"
	BG_CYAN = "46"
	BG_WHITE = "47"
	
	FG_BRIGHT_BLACK = "90"
	FG_BRIGHT_RED = "91"
	FG_BRIGHT_GREEN = "92"
	FG_BRIGHT_YELLOW = "93"
	FG_BRIGHT_BLUE = "94"
	FG_BRIGHT_MAGENTA = "95"
	FG_BRIGHT_CYAN = "96"
	FG_BRIGHT_WHITE = "97"
	
	BG_BRIGHT_BLACK = "100"
	BG_BRIGHT_RED = "101"
	BG_BRIGHT_GREEN = "102"
	BG_BRIGHT_YELLOW = "103"
	BG_BRIGHT_BLUE = "104"
	BG_BRIGHT_MAGENTA = "105"
	BG_BRIGHT_CYAN = "106"
	BG_BRIGHT_WHITE = "107"
	
	FG_DEFAULT = "39"
	BG_DEFAULT = "49"
	
	FG_COLORS = [str(i) for i in list(range(30, 38)) + list(range(90, 98))]
	BG_COLORS = [str(i) for i in list(range(40, 48)) + list(range(100, 108))]


class Style:
	
	BLACK = 0
	RED = 1
	GREEN = 2
	YELLOW = 3
	BLUE = 4
	MAGENTA = 5
	CYAN = 6
	WHITE = 7
	
	BRIGHT_BLACK = 8
	BRIGHT_RED = 9
	BRIGHT_GREEN = 10
	BRIGHT_YELLOW = 11
	BRIGHT_BLUE = 12
	BRIGHT_MAGENTA = 13
	BRIGHT_CYAN = 14
	BRIGHT_WHITE = 15
	
	COLORS = list(range(16))
	
	def __init__(self, fg=None, bg=None, bold=False):
		self.fg = fg
		self.bg = bg
		self.bold = bold
	
	def __eq__(self, other):
		return isinstance(other, Style) and other.fg == fg and other.bg == bg and other.bold == bold

class Screen:
	
	
	def __init__(self, out=sys.stdout):
		self.out = out
		self.width = 0
		self.height = 0
		self.size_changed = True
		self.update_size()
	
	def update_size(self):
		size = shutil.get_terminal_size()
		self.width = size.columns
		self.height = size.lines
		self.size_changed = True
	
	def move(self, x, y):
		self.out.write("\033[{};{}f".format(y+1, x+1))
	
	def write(self, text):
		self.out.write(text)
	
	def style(self, style, previous=None):
		if style == previous:
			return
		parts = []
		reset = False
		if style.fg is None or style.bg is None or previous is None or previous.bold and not style.bold:
			parts.append(Attr.RESET)
			reset = True
		if style.fg is not None and (reset or style.fg != previous.fg):
			parts.append(Attr.FG_COLORS[style.fg])
		if style.bg is not None and (reset or style.bg != previous.bg):
			parts.append(Attr.BG_COLORS[style.bg])
		if style.bold and (reset or not previous.bold):
			parts.append(Attr.BOLD)
		ansistyle = "\033[" + ";".join(parts) + "m"
		self.out.write(ansistyle)
	
	def clear(self):
		self.out.write("\033[0m\033[2J")
	
	def clear_line(self):
		self.out.write("\033[K")
	
	def skip(self, amount=1):
		if amount == 0:
			return
		if amount == 1:
			stramount = ""
		else:
			stramount = str(amount)
		self.out.write("\033[{}C".format(stramount))
	
	def draw_pad(self, pad, scr_x=0, scr_y=0, width=INT_INFINITY, height=INT_INFINITY, pad_x=0, pad_y=0):
		screen = self
		width = min(screen.width - scr_x, pad.width - pad_x)
		height = min(screen.height - scr_y, pad.height - pad_y)
		
		last_style = None
		for y in range(height):
			screen.move(scr_x, scr_y+y)
			skip = 0
			line_y = pad_y + y
			for cell in pad.get_line(pad_x, line_y, width):
				if cell is None:
					skip += 1
					continue
				if skip:
					screen.skip(skip)
					skip = 0
				style, char = cell
				screen.style(style, last_style)
				screen.write(char)

class ScreenPad:
	
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.clear()
	
	def resize(self, width, height):
		self.width = width
		self.height = height
		self.clear()
	
	def fill(self, value):
		self.data = [value for i in range(self.width*self.height)]
	
	def clear(self):
		self.fill(None)
	
	def write(self, x, y, text, style=None):
		if y >= self.height:
			return
		for i, char in enumerate(text):
			if x + i >= self.width:
				break
			self.data[x+i+y*self.width] = (style, char)
	
	def get(self, x, y):
		if y >= self.height or x >= self.width:
			return None
		return self.data[x + y * self.width]
	
	def get_line(self, x, y, length=None):
		if length is None:
			length = self.width - x
		if x >= self.width:
			return []
		start = x + y * self.width
		return self.data[start:start+length]
	



class BufferedScreen:
	
	def __init__(self, out=sys.stdout):
		self.out = out
		self.screen = Screen(io.StringIO())
		self.on_screen = Pad(self.screen.width, self.screen.height)
		self.buff = Pad(self.screen.width, self.screen.height)
	
	def write(self, x, y, text, style=None):
		self.buff.write(x, y, text, style)
	
	def clear(self):
		self.on_screen = Pad(self.screen.width, self.screen.height)
		#self.on_screen.fill(
		self.buff = Pad(self.screen.width, self.screen.height)
		self.screen.clear()
	
	def reset(self):
		self.screen.update_size()
		self.clear()
	
	def _do_write(self):
		self.out.write(self.screen.out.getvalue())
		self.screen.out = io.StringIO()
	
	def redraw(self):
		self.screen.clear()
		self.screen.draw_pad(self.on_screen)
		self.screen.draw_pad(self.buff)
		self._do_write()
	
	def update(self):
		BEGIN = "BEGIN" # before anything on the line has been done
		RUNNING = "RUNNING" # while changing current characters
		POSTRUN = "POSTRUN" # after changing some characters. Unsure whether to jump to next place or just continue
		POSTPOSTRUN = "POSTPOSTRUN" # same, but now the style has been changed
		BETWEEN = "BETWEEN" # run finished, but not worth to continue. Looking for the next changes
		last_style = None
		for y in range(self.on_screen.height):
			#runs = []
			#current_run = None
			running = False
			last_run = None
			post_run = ""
			postpost_run = ""
			post_style = None
			extra = 0
			
			STATE = BEGIN
			#last_style = None
			#cursor_x = None
			for x, (scr_cell, buff_cell) in enumerate(zip(
					self.on_screen.get_line(0, y),
					self.buff.get_line(0, y))):
				
				scr_style, scr_char = scr_cell
				buff_style, buff_char = buff_cell
				while True:
				
					if  state == BEGIN or state == BETWEEN:
						if scr_cell == buff_cell:
							break
						# start the first run
						if state == BEGIN:
							screen.move(x, y)
						else:
							screen.skip(x-cursor_x)
						state = RUNNING
					
					if state == RUNNING:
						if scr_cell != buff_cell:
							# continuing the same run
							screen.style(buff_style, last_style)
							last_style = buff_style
							screen.write(buff_char)
							break
						cursor_x = x
						state = POSTRUN
						extra = 0
						post_run = ""
						postpost_run = ""
					
					if state == POSTRUN:
						if buff_cell != scr_cell:
							screen.write(post_run)
							state = RUNNING
						elif extra >= 4:
							state = BETWEEN
							break
						elif buff_style == last_style:
							extra += 1
							post_run += buf_char
							break
						else:
							last_style = buf_style
							state = POSTPOSTRUN
					
					if state == POSTPOSTRUN:
						if buff_style != last_style:
							state = BETWEEN
							break
						if buff_cell != scr_cell:
							screen.write(post_run)
							screen.style(last_style)
							screen.write(postpost_run)
							state = RUNNING
						elif extra >= 4:
							state = BETWEEN
							break
						else:
							extra += 1
							postpost_run += buf_char
							break
		self._do_write()

def main():
	scr = Screen()
	
	signal.signal(signal.SIGWINCH, (lambda signum, frame: scr.update_size()))
	scr.clear()
	scr.move(0, 0)
	scr.style(Style(fg=Style.GREEN, bg=Style.BLACK))
	scr.write("DONE!!!!!!!!!!!!!!!!!!!!!")
	scr.style(Style(Style.BRIGHT_GREEN, Style.BRIGHT_MAGENTA))
	scr.move(2, 10)
	scr.write("......... WAIT! THERE'S MORE!!")
	scr.style(Style())
	scr.move(scr.width-2, scr.height+1)
	scr.write("01")
	
	pad = ScreenPad(64, 16)
	for x in range(16):
		for y in range(16):
			pad.write(x*4, y, "ab", Style(Style.COLORS[x], Style.COLORS[y]))
			pad.write(x*4+2, y, "c", Style(Style.COLORS[x], Style.COLORS[y], bold=True))
	#pad.write(10, 10, "hello world. This is Dog", (Attr.FG_BRIGHT_BLUE, Attr.BG_BLUE, Attr.BOLD))
	scr.draw_pad(pad, 0, 0)
	
	scr.move(0, 25)
	scr.style(Style())


if __name__ == "__main__":
	main()
