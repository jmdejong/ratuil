#!/usr/bin/env -S python3 -u


from bufferedscreen import BufferedScreen
from screen import Screen
from layout import Layout
from style import Style


import shutil
import random
import signal
import tty
import sys
import termios


sprites = {
	"floor": ("＿", Style(3)),
	"wall": ("Ｘ", Style(7,8)),
	"coin": ("ｃ", Style(11)),
	"player": ("＠", Style(12))
}
#sprites = {
	#"floor": ("_", Style(3)),
	#"wall": ("x", Style(7,8)),
	#"coin": ("c", Style(11)),
	#"player": ("@", Style(12))
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
	
	
	def update(self, field, key):
		new_x = self.x + (key == "d") - (key == "a")
		new_y = self.y + (key == "s") - (key == "w")
		if field.get(new_x, new_y) != "wall":
			self.x = new_x
			self.y = new_y
		self.inventory_selector += (key == "+") - (key == "-")
		self.inventory_selector %= len(self.inventory)


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
	layout.update()
	

def main():
	scr = Screen()
	scr.clear()
	
	with open("game.xml") as f:
		layouttext = f.read()
	
	layout = Layout(layouttext)
	
	layout.set_target(scr)
	layout.update(force=True)
	
	signal.signal(signal.SIGWINCH, (lambda signum, frame: scr.reset()))
	
	tty.setcbreak(sys.stdin)
	
	
	Screen.default.hide_cursor()
	
	field = Field(150, 40)
	while True:
		draw(layout, field)
		if hasattr(scr, "update"):
			scr.update()
		field.update(sys.stdin.read(1))


if __name__ == "__main__":
	fd = sys.stdin.fileno()
	oldterm = termios.tcgetattr(fd)
	exitreason = None
	try:
		main()
	except KeyboardInterrupt:
		exitreason = "^C caught, goodbye"
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, oldterm)
		Screen.default.finalize()
	if exitreason:
		Screen.default.move(0, Screen.default.height-2)
		print(exitreason)
