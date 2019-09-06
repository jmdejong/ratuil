#!/usr/bin/env -S python3 -u


from bufferedscreen import BufferedScreen
from screen import Screen
from window import Window
from layout import Layout


import shutil





def main():
	
	scr = BufferedScreen()
	scr.clear()
	
	#window = Window(scr)
	
	with open("layout.xml") as f:
		layouttext = f.read()
	
	layout = Layout(layouttext)
	
	layout.resize(scr)
	layout.update(force=True)
	
	#tree = build_layout(ET.parse("layout.xml").getroot())

	#tree.resize(scr)
	
	#tree.update()
	
	scr.update()
	
	raw = Screen()
	size = shutil.get_terminal_size()
	#raw.write(0,0,"********")
	#raw.write(size.columns-1, size.lines-1, "*")
	raw.move(0, size.lines-1)
	


if __name__ == "__main__":
	main()
