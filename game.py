#!/usr/bin/env -S python3 -u


from ratuil.bufferedscreen import BufferedScreen
from ratuil.screen import Screen
from ratuil.layout import Layout
from ratuil.textstyle import TextStyle
from ratuil.pad import Pad
from ratuil.inputs import get_key


import shutil
import random
import signal
import tty
import sys
import termios


sprites = {
	"floor": ("＿", TextStyle(3)),
	"wall": ("Ｘ", TextStyle(7,8)),
	"coin": ("ｃ", TextStyle(11)),
	"player": ("}{", TextStyle(12))#"＠", TextStyle(12))
}
#sprites = {
	#"floor": ("_", TextStyle(3)),
	#"wall": ("x", TextStyle(7,8)),
	#"coin": ("c", TextStyle(11)),
	#"player": ("@", TextStyle(12))
#}

generated_objects = {
	"floor": 75,
	"wall": 20,
	"coin": 5
}

objectweights = list(zip(*generated_objects.items()))

class Field:
	
	def __init__(self, width, height):
		self.cells = {}
		self.width = width
		self.height = height
		self._generate()
		self.player = Player(self.width // 2, self.height // 2)
	
	def _generate(self):
		for x in range(self.width):
			for y in range(self.height):
				if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
					obj = "wall"
				elif x == self.width // 2 and y == self.height // 2:
					obj = "floor"
				else:
					obj, = random.choices(*objectweights)
					#print(obj)
				self.cells[(x, y)] = obj
	
	def get(self, x, y):
		if x == self.player.x and y == self.player.y:
			return "player"
		return self.cells.get((x, y))
	
	def set(self, x, y, val):
		self.cells[(x, y)] = val
	
	def update(self, key):
		self.player.update(self, key)


class Player:
	
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
		self.inventory = ["sword", "food", "axe"]
		self.inventory_selector = 0
		self.switch_selector = 0
	
	
	def update(self, field, key):
		new_x = self.x + (key == "d") - (key == "a")
		new_y = self.y + (key == "s") - (key == "w")
		if field.get(new_x, new_y) != "wall":
			self.x = new_x
			self.y = new_y
		self.inventory_selector += (key == "+") - (key == "-")
		self.inventory_selector %= len(self.inventory)
		
		self.switch_selector += (key == "*")
		self.switch_selector %= 2


def draw(layout, field):
	player = field.player
	out = layout.get("field")
	out.set_size(field.width, field.height)
	for x in range(field.width):
		for y in range(field.height):
			out.change_cell(x, y, *sprites[field.get(x, y)])
	out.set_center(player.x, player.y)
	
	inv = layout.get("inventory")
	inv.set_items(player.inventory)
	inv.select(player.inventory_selector)
	switch = layout.get("menus")
	switch.select(player.switch_selector)
	layout.update()
	

def main():
	scr = BufferedScreen()
	scr.clear()
	
	layout = Layout.from_xml_file("game.xml")
	
	layout.set_target(scr)
	layout.update(force=True)
	
	signal.signal(signal.SIGWINCH, (lambda signum, frame: scr.reset()))
	
	
	layout.get("input").set_text("hello", 5)
	
	field = Field(200, 40)
	while True:
		draw(layout, field)
		if hasattr(scr, "update"):
			scr.update()
		inp = get_key(do_interrupt=True)
		#if inp == "^C":
			#break
		layout.get("messages").add_message(str(ord(inp[0])) + ": " + inp)
		field.update(inp)


if __name__ == "__main__":
	fd = sys.stdin.fileno()
	oldterm = termios.tcgetattr(fd)
	exitreason = None
	try:
		tty.setraw(sys.stdin)
		Screen.default.hide_cursor()
		main()
	except KeyboardInterrupt:
		exitreason = "^C caught, goodbye"
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, oldterm)
		Screen.default.finalize()
	if exitreason:
		Screen.default.move(0, Screen.default.height-2)
		print(exitreason)
