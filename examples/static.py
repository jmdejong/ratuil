#!/usr/bin/env -S python3

from ratuil.layout import Layout
from ratuil.screen import Screen

layoutstring = """<?xml version="1.0"?>
<hbox>
	<vbox width="20" align="right">
		<bar id="health" height="2" full-char="+" empty-char="-" full-style="fg:7; bg:2" empty-style="fg:7; bg: 1;" total="10" filled="8"></bar>
		<switchbox id="menus" selected="equipment" height="50%">
			<border key="inventory">
				<listing id="inventory">
					milk
					eggs
					bread
				</listing>
			</border>
			<border char="#" key="equipment">
				<listing id="equipment">
					cotton underwear
					cotton shirt
					jeans
					friendship bracelet
				</listing>
			</border>
		</switchbox>
		<border char=" ">
			<textbox id="info">
This is a great place to show some information.
Textbox lines are wrapped!
			</textbox>
		</border>
	</vbox>
	<fill width="1" align="right" style="fg:12;bg:4">
		@
	</fill>
	<vbox>
		<hbox align="bottom" height="1">
			<charbox width="2">&gt;</charbox>
			<textinput id="input"></textinput>
		</hbox>
		<log id="messages" align="bottom" height="20%%">
			Welcome to [game]
		</log>
		<border>
			<overlay>
				<field id="field" char-size="2"></field>
				<border offset-x="2" align="right" width="13" offset-y="1" height="3" style="reverse">
					<charbox>hello world</charbox>
				</border>
			</overlay>
		</border>
	</vbox>
</hbox>
"""

def main():
	
	layout = Layout.from_xml_str(layoutstring)
	
	screen = Screen()
	screen.clear()
	layout.set_target(screen)
	layout.update()
	screen.update()
	screen.finalize()
	print()


if __name__ == "__main__":
	main()
