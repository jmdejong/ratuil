
import os.path

from .screenelement import ScreenElement

from .widgets.textbox import TextBox
from .widgets.hbox import HBox
from .widgets.vbox import VBox
from .widgets.listing import Listing
from .widgets.border import Border
from .widgets.log import Log
from .widgets.textinput import TextInput
from .widgets.field import Field
from .widgets.bar import Bar
from .widgets.switchbox import SwitchBox
from .widgets.box import Box
from .widgets.fill import Fill
from .widgets.empty import Empty
from .widgets.overlay import Overlay

import xml.etree.ElementTree as ET

widgets = {
	"textbox": TextBox,
	"hbox": HBox,
	"vbox": VBox,
	"listing": Listing,
	"border": Border,
	"log": Log,
	"textinput": TextInput,
	"field": Field,
	"bar": Bar,
	"switchbox": SwitchBox,
	"box": Box,
	"fill": Fill,
	"empty": Empty,
	"overlay": Overlay
}

class Layout:
	
	def __init__(self, backend, tree, basepath=""):
		
		self.backend = backend
		self.tree = tree
		self.id_elements = {}
		self.changed = True
		self.target = None
		self.layout = self.build_layout(self.tree)
		self._target_size = None
		
	def build_layout(self, etree):
		children = [self.build_layout(child) for child in etree]
		widget = widgets[etree.tag].from_xml(children, etree.attrib, etree.text)
		widget.set_backend(self.backend)
		se = ScreenElement(widget, etree.attrib)
		if se.id is not None:
			self.id_elements[se.id] = se
		return se
	
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
		return self.id_elements.get(id).widget
	
	@classmethod
	def from_xml_str(cls, backend, string, basepath=""):
		return cls(backend, ET.fromstring(string), basepath)
	
	@classmethod
	def from_xml_file(cls, backend, fname, basepath=None):
		if basepath is None:
			basepath = os.path.dirname(fname)
		return cls(backend, ET.parse(fname).getroot(), basepath)
	
