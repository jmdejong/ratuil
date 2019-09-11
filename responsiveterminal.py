#!/usr/bin/env -S python3 -u


from bufferedscreen import BufferedScreen
from screen import Screen
from layout import Layout


import shutil


def main():
	
	scr = BufferedScreen()
	scr.clear()
	
	
	with open("layout.xml") as f:
		layouttext = f.read()
	
	layout = Layout(layouttext)
	
	layout.resize(scr)
	layout.update(force=True)
	
	
	scr.update()
	
	raw = Screen()
	size = shutil.get_terminal_size()
	raw.move(0, size.lines-1)
	


if __name__ == "__main__":
	main()
