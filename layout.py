

from widgets.textbox import TextBox
from widgets.charbox import CharBox
from widgets.hbox import HBox
from widgets.vbox import VBox
from widgets.listing import Listing
from widgets.border import Border

import xml.etree.ElementTree as ET

widgets = {
	"textbox": TextBox,
	"charbox": CharBox,
	"hbox": HBox,
	"vbox": VBox,
	"listing": Listing,
	"border": Border
}



class Layout:
	
	def __init__(self, xmllayout):
		
		self.tree = ET.fromstring(xmllayout)
		self.layout = self.build_layout(self.tree)
		self.id_elements = {}
		
	def build_layout(self, etree):
		children = [self.build_layout(child) for child in etree]
		widget = widgets[etree.tag](children, etree)
		if "id" in etree.attrib:
			self.id_elements[etree.attrib["id"]] = widget
		return widget
	
	def resize(self, target):
		self.layout.resize(target)
	
	def update(self, force=False):
		self.layout.update(force)
	
