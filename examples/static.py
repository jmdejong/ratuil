#!/usr/bin/env -S python3

from ratuil.layout import Layout
from ratuil.screen import Screen

layoutstring = """<?xml version="1.0"?>
<hbox>
	<vbox width="20" align="right">
		<bar id="health" height="2" full-char="+" empty-char="-" full-style="fg:7; bg:2" empty-style="fg:7; bg: 1;" total="10" filled="8"></bar>
		<switchbox id="menus">
			<border>
				<listing id="inventory">
					milk
					eggs
					bread
				</listing>
			</border>
			<border char="#">
				<listing id="equipment">
					cotton underwear
					cotton shirt
					jeans
					friendship bracelet
				</listing>
			</border>
		</switchbox>
	</vbox>
	<fill width="2" align="right" style="fg:12;bg:4">
		[]
	</fill>
	<vbox>
		<textinput id="input" align="bottom" height="1">hello</textinput>
		<log id="messages" align="bottom" height="20%%">
			Welcome to [game]
		</log>
		<border>
			<overlay>
				<field id="field" char-size="2"></field>
				<border offset-x="2" align="right" width="13" offset-y="1" height="3" style="reverse">
					<textbox>hello world</textbox>
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
