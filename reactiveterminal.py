#!/usr/bin/env -S python3 -u


from bufferedscreen import BufferedScreen
from window import Window

from widgets.textbox import TextBox
from widgets.charbox import CharBox
from widgets.hbox import HBox

import xml.etree.ElementTree as ET


def build_textbox(etree):
	return TextBox(etree.text)

def build_charbox(etree):
	return CharBox(etree.text)

def build_hbox(etree):
	children = []
	separators = []
	for childnode in etree:
		children.append(build_tree(childnode))
		separators.append(int(childnode.attrib.get("width")))
	return HBox(children, separators)

widgets = {
	"textbox": build_textbox,
	"charbox": build_charbox,
	"hbox": build_hbox
}

def build_tree(etree):
	return widgets[etree.tag](etree)

def main():
	
	scr = BufferedScreen()
	scr.clear()
	
	window = Window(scr)
	
	tree = build_tree(ET.parse("layout.xml").getroot())

	tree.resize(scr)
	
	tree.update()
	
	scr.update()
	
	


if __name__ == "__main__":
	main()
