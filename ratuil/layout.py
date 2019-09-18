
import os.path

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
from .widgets.switchbox import SwitchBox

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
	"bar": Bar,
	"switchbox": SwitchBox
}



class Layout:
	
	def __init__(self, tree, basepath=""):
		
		self.tree = tree
		self.id_elements = {}
		self.changed = True
		self.target = None
		self.layout = self.build_layout(self.tree)
		self._target_size = None
		
	def build_layout(self, etree):
		children = [self.build_layout(child) for child in etree]
		widget = widgets[etree.tag].from_xml(children, etree)
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
	
	@classmethod
	def from_xml_str(cls, string, basepath=""):
		return cls(ET.fromstring(string), basepath)
	
	@classmethod
	def from_xml_file(cls, fname, basepath=None):
		if basepath is None:
			basepath = os.path.dirname(fname)
		return cls(ET.parse(fname).getroot(), basepath)
	
