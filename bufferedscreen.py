

import sys
import io

from constants import INT_INFINITY
from screen import Screen
from pad import Pad




class BufferedScreen:
	
	def __init__(self, out=sys.stdout):
		self.out = out
		self.screen = Screen(io.StringIO())
		self.on_screen = Pad(self.screen.width, self.screen.height)
	
	def clear(self):
		self.on_screen = Pad(self.screen.width, self.screen.height)
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
		self._do_write()
	
	def draw_pad(self, *args, **kwargs):
		self.on_screen.draw_pad(*args, **kwargs)
		self.screen.draw_pad(*args, **kwargs)
		self._do_write()
		
	
	def draw_pad_optimized(self, src, dest_x=0, dest_y=0, width=INT_INFINITY, height=INT_INFINITY, src_x=0, src_y=0):
		# Optimizes on the amount of characters to write to the terminal, which is more crucial in applications running over a network connection (like ssh)
		# This will only draw the changed characters
		width = min(self.screen.width - dest_x, src.width - src_x)
		height = min(self.screen.height - dest_y, src.height - src_y)
		
		BEGIN = "BEGIN" # before anything on the line has been done
		RUNNING = "RUNNING" # while changing current characters
		POSTRUN = "POSTRUN" # after changing some characters. Unsure whether to jump to next place or just continue
		POSTPOSTRUN = "POSTPOSTRUN" # same, but now the style has been changed
		BETWEEN = "BETWEEN" # run finished, but not worth to continue. Looking for the next changes
		last_style = None
		for y in range(height):
			#runs = []
			#current_run = None
			running = False
			last_run = None
			post_run = ""
			postpost_run = ""
			post_style = None
			extra = 0
			
			state = BEGIN
			#last_style = None
			#cursor_x = None
			for x, (scr_cell, buff_cell) in enumerate(zip(
					self.on_screen.get_line(dest_x, dest_y + y, width),
					src.get_line(src_x, src_y + y, width))):
				if scr_cell is None:
					scr_cell = (None, None)
				scr_style, scr_char = scr_cell
				if buff_cell is None:
					if state == BEGIN:
						continue
					if state == RUNNING:
						cursor_x = x
					state = BETWEEN
					continue
				buff_style, buff_char = buff_cell
				while True:
				
					if  state == BEGIN or state == BETWEEN:
						if scr_cell == buff_cell:
							break
						# start the first run
						if state == BEGIN:
							self.screen.move(dest_x + x, dest_y + y)
						else:
							self.screen.skip(x-cursor_x)
						state = RUNNING
					
					if state == RUNNING:
						if scr_cell != buff_cell:
							# continuing the same run
							self.screen.style(buff_style, last_style)
							last_style = buff_style
							self.screen.write(buff_char)
							break
						cursor_x = x
						state = POSTRUN
						extra = 0
						post_run = ""
						postpost_run = ""
					
					if state == POSTRUN:
						if buff_cell != scr_cell:
							self.screen.write(post_run)
							state = RUNNING
						elif extra >= 4:
							state = BETWEEN
							break
						elif buff_style == last_style:
							extra += 1
							post_run += buff_char
							break
						else:
							before_last_style = last_style
							last_style = buff_style
							state = POSTPOSTRUN
					
					if state == POSTPOSTRUN:
						if buff_style != last_style:
							state = BETWEEN
							break
						if buff_cell != scr_cell:
							self.screen.write(post_run)
							self.screen.style(last_style, before_last_style)
							self.screen.write(postpost_run)
							state = RUNNING
						elif extra >= 4:
							state = BETWEEN
							break
						else:
							extra += 1
							postpost_run += buff_char
							break
		self.on_screen.draw_pad(src, dest_x, dest_y, width, height, src_x, src_y)
		self._do_write()
