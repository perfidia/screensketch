'''
Created on Dec 29, 2012

@author: Bartosz Alchimowicz
'''

import StringIO
from types import MethodType
from lxml import etree as ET
import screensketch.screenspec.model as orginal

def ScreenSpec_att_to_xml(self):
	node = ET.Element("screen-spec")

	for c in self.children:
		c.to_xml(node)

	tree = ET.ElementTree(node)
	output = StringIO.StringIO()
	tree.write(output, pretty_print=True, encoding="UTF-8")

	retval = output.getvalue()

	return retval

def Screen_att_to_xml(self, parent):
	node = ET.SubElement(parent, "screen")

	name = ET.SubElement(node, "name")
	name.text = self.name

	children = ET.SubElement(node, "children")

	for c in self.children:
		c.to_xml(children)

	return node

def Component_att_to_xml(self, parent):
	node = ET.SubElement(parent, "component")

	if self.name:
		node.set("type", self.name)

	identifier = ET.SubElement(node, "identifier")
	identifier.text = self.identifier

	return node

def ComoundComponent_att_to_xml(self, parent):
	node = ET.SubElement(parent, "component")
	node.set("type", self.name)

	identifier = ET.SubElement(node, "identifier")
	identifier.text = self.identifier

	children = ET.SubElement(node, "children")

	for c in self.children:
		c.to_xml(children)

	if isinstance(self, orginal.ComoundValuesContainer) and self._grid: # and len(self._grid) > 0
		grid = ET.SubElement(node, "values")

		for row in self._grid:
			tr = ET.SubElement(grid, "tr")

			for col in row:
				td = ET.SubElement(tr, "td")
				td.text = col

	return node

def StaticValue_att_to_xml(self, parent):
	node = ET.SubElement(parent, "value")
	node.text = self.value

	if self.selected == True:
		node.set("selected", "True")

	return node

def StaticValueContainer_att_to_xml(self, parent):
	node = ET.SubElement(parent, "component")
	node.set("type", self.name)

	identifier = ET.SubElement(node, "identifier")
	identifier.text = self.identifier

	if self._static_values is not None:
		static_values = ET.SubElement(node, "values")

		svs = self._get_static_values()

		for i in svs:
			i.to_xml(static_values)
	elif isinstance(self, orginal.ComoundComponent) and len(self.children) > 0:
		children = ET.SubElement(node, "children")

		for c in self.children:
			c.to_xml(children)
	else:
		pass

	return node

attachments = {
	orginal.ScreenSpec:           ScreenSpec_att_to_xml,
	orginal.Screen:               Screen_att_to_xml,
	orginal.Component:            Component_att_to_xml,
	orginal.ComoundComponent:     ComoundComponent_att_to_xml,
	orginal.StaticValue:          StaticValue_att_to_xml,
#	orginal.StaticValueContainer: StaticValueContainer_att_to_xml,
	orginal.Button:               StaticValueContainer_att_to_xml,
	orginal.Link:                 StaticValueContainer_att_to_xml,
	orginal.StaticText:           StaticValueContainer_att_to_xml,
	orginal.EditBox:              StaticValueContainer_att_to_xml,
	orginal.TextArea:             StaticValueContainer_att_to_xml,
	orginal.ComboBox:             StaticValueContainer_att_to_xml,
	orginal.ListBox:              StaticValueContainer_att_to_xml,
	orginal.RadioButtons:         StaticValueContainer_att_to_xml,
	orginal.CheckBoxes:   	      StaticValueContainer_att_to_xml,
}

def attach():
	for clazz in attachments:
		method = attachments[clazz]
		clazz.to_xml = MethodType(method, None, clazz)

def detach():
	for clazz in attachments:
		del clazz.to_xml
