
from .boxstyle import BoxStyle
from .widgets.textbox import TextBox
from .widgets.charbox import CharBox
from .widgets.hbox import HBox
from .widgets.vbox import VBox
from .widgets.listing import Listing
from .widgets.border import Border
from .widgets.log import Log
from .widgets.textinput import TextInput
from .widgets.field import Field
from .widgets.bar import Bar

import xml.etree.ElementTree as ET

widgets = {
	"textbox": TextBox,
	"charbox": CharBox,
	"hbox": HBox,
	"vbox": VBox,
	"listing": Listing,
	"border": Border,
	"log": Log,
	"textinput": TextInput,
	"field": Field,
	"bar": Bar
}



class Layout:
	
	def __init__(self, xmllayout):
		
		self.tree = ET.fromstring(xmllayout)
		self.id_elements = {}
		self.changed = True
		self.target = None
		self.layout = self.build_layout(self.tree)
		self._target_size = None
		
	def build_layout(self, etree):
		children = [self.build_layout(child) for child in etree]
		widget = widgets[etree.tag](children, etree)
		widget.set_box_style(BoxStyle.from_attrs(etree.attrib))
		if "id" in etree.attrib:
			self.id_elements[etree.attrib["id"]] = widget
		return widget
	
	def set_target(self, target):
		self.target = target
		self.resize()
	
	def resize(self):
		self.layout.resize(self.target)
		self._target_size = (self.target.width, self.target.height)
		self.changed = True
	
	def update(self, force=False):
		if self._target_size != (self.target.width, self.target.height):
			self.resize()
		if self.changed:
			force = True
			self.changed = False
		self.layout.update(force)
	
	def get(self, id):
		return self.id_elements.get(id)
	
