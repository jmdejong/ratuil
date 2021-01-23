


import curses

from .constants import INT_INFINITY
from .basescreen import BaseScreen
from .textstyle import TextStyle as Style
from .strwidth import charwidth
from .cursedpad import CursedPad
from .import inputs


key_mappings = {
	curses.KEY_UP: inputs.UP,
	curses.KEY_DOWN: inputs.DOWN,
	curses.KEY_LEFT: inputs.LEFT,
	curses.KEY_RIGHT: inputs.RIGHT,
	curses.KEY_BACKSPACE: inputs.BACKSPACE,
	curses.KEY_HOME: inputs.HOME,
	curses.KEY_END: inputs.END,
	curses.KEY_PPAGE: inputs.PAGEUP,
	curses.KEY_NPAGE: inputs.PAGEDOWN,
	curses.KEY_DC: inputs.DELETE,
	curses.KEY_IC: inputs.INSERT,
}

class Colours:
	
	def __init__(self):
		
		self.colours = min(curses.COLORS, 16)
		self.pairs = self.colours*self.colours

		curses.use_default_colors()
		for i in range(0, self.pairs):
			curses.init_pair(i, i%self.colours, i//self.colours)
	
	def get(self, fg=0, bg=0):
		if fg is None:
			fg = 0
		if bg is None:
			bg = 0
		if self.colours == 16:
			return curses.color_pair(fg + bg*self.colours)
		elif self.colours == 8:
			dfg = fg % 8
			dbg = bg % 8
			if bg == 8:
				dbg = 7
			if fg == 8:
				dfg = 7
			colour = curses.color_pair(dfg + dbg*self.colours)
			if fg >= 8 and bg < 8:
				colour |= curses.A_BOLD
			elif fg < 8 and bg >= 8:
				colour |= curses.A_DIM
			return colour
		else:
			return curses.color_pair(0)
	
	def attrs(self, style):
		if style is None:
			style = Style.default
		attributes = self.get(style.fg, style.bg);
		if style.attr[Style.BOLD]:
			attributes |= curses.A_BOLD
		if style.attr[Style.UNDERSCORE]:
			attributes |= curses.A_UNDERLINE
		if style.attr[Style.REVERSE]:
			attributes |= curses.A_REVERSE
		return attributes


class CursedScreen(BaseScreen):
	
	def __init__(self, **_kwargs):
		pass
	
	def initialize_terminal(self):
		# Initialize curses
		self.screen = curses.initscr()

		# Turn off echoing of keys, and enter cbreak mode,
		# where no buffering is performed on keyboard input
		curses.noecho()
		curses.cbreak()

		# In keypad mode, escape sequences for special keys
		# (like the cursor keys) will be interpreted and
		# a special value like curses.KEY_LEFT will be returned
		self.screen.keypad(1)
		
		try:
			# make the cursor invisible
			# store the previous cursor location
			self.cursor_visibility = curses.curs_set(0)
		except:
			# having the cursor displayed is annoying somewhat annoying,
			# but it's not terrible so safe to ignore
			pass

		# Start color, too.  Harmless if the terminal doesn't have
		# color; user can test with has_color() later on.  The try/catch
		# works around a minor bit of over-conscientiousness in the curses
		# module -- the error return from C start_color() is ignorable.
		try:
			curses.start_color()
		except:
			pass
		self.colours = Colours()
		
		self.width = 0
		self.height = 0
		#self.blink_bright_background = blink_bright_background # use the blink attribute for bright backgrounds
		#self.always_reset = always_reset or blink_bright_background # always reset if the style is different than the previous one
		self.update_size()
		self.screen.refresh()
	
	def finalize_terminal(self):
		self.screen.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin()
	
	def get_key(self):
		key = self.screen.getch()
		if key in key_mappings:
			return key_mappings[key]
		return inputs.name_char(key)
	
	def create_pad(self, width, height):
		return CursedPad(self.screen, self.colours, width, height)
	
	
	def update_size(self):
		curses.update_lines_cols()
		(y, x) = self.screen.getmaxyx()
		self.width = x
		self.height = y
	
	def _addstr(self, y, x, string, *args):
		if not self.screen:
			return
		try:
			self.screen.addstr(y, x, string, *args)
		except curses.error:
			# ncurses has a weird problem:
			# it always raises an error when drawing to the last character in the window
			# it draws first and then raises the error
			# therefore to draw in the last place of the window the last character needs to be ingored
			# other solutions might be possible, but are more hacky
			pass
		
	def write(self, x, y, text, style=None):
		self._addstr(y, x, text, self.colours.attrs(style))
	
	def clear(self):
		self.screen.clear();
	
	def reset(self):
		curses.endwin()
		self.screen.refresh()
		self.update_size()
	
	def draw_pad(self, pad, scr_x=0, scr_y=0, width=INT_INFINITY, height=INT_INFINITY, pad_x=0, pad_y=0):
		pad.pad.noutrefresh(pad_y, pad_x, scr_y, scr_x, scr_y + height-1, scr_x + width-1)
	
	def update(self):
		self.screen.refresh()

Screen = CursedScreen

