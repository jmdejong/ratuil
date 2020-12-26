#!/usr/bin/env -S python3

#from ratuil.bufferedscreen import Screen
#from ratuil.ansiscreen import Screen
from ratuil.cursedscreen import Screen
from ratuil.layout import Layout
from ratuil.inputs import get_key
import time

layoutstring = """\
<?xml version="1.0"?>
<hbox>
	<vbox width="20" align="right">
		<bar id="health" height="1" full-char="+" empty-char="-" full-style="fg:7; bg:2" empty-style="fg:7; bg: 1;" total="10" filled="8"></bar>
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
			<textbox id="info" wrap="words">
This is a great place to show some information.
Textbox lines can be wrapped!
			</textbox>
		</border>
	</vbox>
	<fill width="1" align="right" style="fg:12;bg:4">
		@
	</fill>
	<vbox>
		<hbox align="bottom" height="1">
			<textbox width="2">&gt;</textbox>
			<textinput id="input"></textinput>
		</hbox>
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
	target = Screen()
	try:
		target.initialize_terminal()
		target.clear()
		layout = Layout.from_xml_str(target, layoutstring)
		layout.update()
		target.update()
		get_key()
	finally:
		target.finalize_terminal()
	print()


if __name__ == "__main__":
	main()
