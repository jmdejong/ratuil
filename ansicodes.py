#!/usr/bin/env -S python3 -u

#import sys
#import shutil
#import io
import signal



from .screen import Screen
from .bufferedscreen import BufferedScreen
from .constants import INT_INFINITY
from .pad import Pad
from .style import Style
from .window import Window
from .widgets.textbox import TextBox
from .widgets.charbox import CharBox
from .widgets.hbox import HBox




def main():
	
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
	scr.draw_pad_direct(pad, 0, 0)
	
	pad.write(28, 3, "hello world", Style(Style.RED, Style.BRIGHT_BLUE))
	
	raw_screen.style(Style.default)
	raw_screen.addstr("\n\n")
	#raw_screen.addstr(str(scr.on_screen.data))
	raw_screen.addstr("\n\n")
	
	scr.draw_pad(pad)
	scr.update()
	
	
	text1 = TextBox()
	text1.set_text("lorum ipsum dolor \nsit amet\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1\nbye")
	
	text2 = CharBox()
	text2.set_text("It is a truth, universally accepted bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb2\ndone")
	
	box = HBox([text1, text2], [32])
	
	
	win = Window(scr, 10, 10)
	box.resize(win)
	#text.resize(win)
	
	box.update()
	scr.update()
	
	raw_screen.move(0, 25)
	raw_screen.style(Style.default)


if __name__ == "__main__":
	main()
