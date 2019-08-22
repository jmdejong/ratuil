#!/usr/bin/env -S python3 -u

#import sys
#import shutil
#import io
import signal



from screen import Screen
from bufferedscreen import BufferedScreen
from constants import INT_INFINITY
from pad import Pad
from style import Style




def main():
	#scr = Screen()
	
	#signal.signal(signal.SIGWINCH, (lambda signum, frame: scr.update_size()))
	#scr.clear()
	#scr.move(0, 0)
	#scr.style(Style(fg=Style.GREEN, bg=Style.BLACK))
	#scr.write("DONE!!!!!!!!!!!!!!!!!!!!!")
	#scr.style(Style(Style.BRIGHT_GREEN, Style.BRIGHT_MAGENTA))
	#scr.move(2, 10)
	#scr.write("......... WAIT! THERE'S MORE!!")
	#scr.style(Style.default)
	#scr.move(scr.width-2, scr.height+1)
	#scr.write("01")
	
	raw_screen = Screen()
	
	scr = BufferedScreen()
	scr.clear()
	signal.signal(signal.SIGWINCH, (lambda signum, frame: scr.reset()))
	
	pad = Pad(64, 16)
	for x in range(16):
		for y in range(16):
			pad.write(x*4, y, "ab", Style(Style.COLORS[x], Style.COLORS[y]))
			pad.write(x*4+2, y, "c", Style(Style.COLORS[x], Style.COLORS[y], bold=True))
	#pad.write(10, 10, "hello world. This is Dog", (Attr.FG_BRIGHT_BLUE, Attr.BG_BLUE, Attr.BOLD))
	scr.draw_pad(pad, 0, 0)
	
	pad.write(28, 3, "hello world", Style(Style.RED, Style.BRIGHT_BLUE))
	
	raw_screen.style(Style.default)
	raw_screen.write("\n\n")
	#raw_screen.write(str(scr.on_screen.data))
	raw_screen.write("\n\n")
	
	scr.draw_pad_optimized(pad)
	
	raw_screen.move(0, 25)
	raw_screen.style(Style.default)


if __name__ == "__main__":
	main()
