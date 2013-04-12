'''
Created on Apr 12, 2013

@author: Bartosz Alchimowicz
'''

from lxml import etree
from StringIO import StringIO
from screensketch.screenspec import model

class XMLReader(object):
	def __init__(self, input_data):
		self.input_data = input_data
		self.retval = None;

	def __parseComponent(self, node, parent):
		items = node.items()

		if len(items) > 1:
			raise ValueError('Incorrect data in component node')

		name = None

		if len(items) == 1:
			name = items[0][1]

		clazz = {
			'EDIT_BOX': model.EditBox,
			'BUTTON': model.Button,
			'CHECK_BOX': model.CheckBox,
			'CHECK_BOXES': model.CheckBoxes,
			'COMBO_BOX': model.ComboBox,
			'DYNAMIC_TEXT': model.DynamicText,
			'EDIT_BOX': model.EditBox,
			'IMAGE': model.Image,
			'LINK': model.Link,
			'LIST': model.List,
			'LIST_BOX': model.ListBox,
			'PASSWORD': model.Password,
			'RADIO_BUTTON': model.RadioButton,
			'RADIO_BUTTONS': model.RadioButtons,
			'SIMPLE': model.Simple,
			'STATIC_TEXT': model.StaticText,
			'TABLE': model.Table,
			'TEXT_AREA': model.TextArea,
		}.get(name, model.Entity)

		if clazz is None:
			raise ValueError('%s is an unsupported type of component' % name)

		children = []
		values = []

		for n in node.getchildren():
			if n.tag == 'identifier':
				identifier = n.text
			elif n.tag == 'children':
				children = self.__parseChildren(n, parent)
			elif n.tag == 'values':
				values = self.__parseValues(n, parent)
			else:
				raise ValueError('%s is an unsupported node in component tag' % n.tag)

		component = clazz(identifier)

		for child in children:
			component.append(child)

		if values:
			component._set_static_values(values)

		return component

	def __parseValues(self, node, parent):
		# tag name checked in __parseComponent

		children = []

		for n in node.getchildren():
			if n.tag == 'value':
				selected = False

				items = n.items()

				if len(items) == 1 and len(items[0]) == 2:
					selected = items[0][1]

				children.append(model.StaticValue(n.text, selected))
			else:
				raise ValueError('%s is an unsupported node in values tag' % n.tag)

		return children

	def __parseChildren(self, node, parent):
		# tag name checked in __parseScreen

		children = []

		for n in node.getchildren():
			children.append(self.__parseComponent(n, parent))

		return children

	def __parseScreen(self, node, parent):
		if node.tag != 'screen':
			raise ValueError('Tag screen-spec not found')

		children = []

		for n in node.getchildren():
			if n.tag == 'name':
				name = n.text
			elif n.tag == 'children':
				children = self.__parseChildren(n, parent)
			else:
				raise ValueError('Unknown node in screen tag found')

		parent.append(model.Screen(name, children))

	def __parseScreenSpec(self, node):
		if node.tag != 'screen-spec':
			raise ValueError('Tag screen-spec not found')

		self.retval = model.ScreenSpec()

		for n in node.getchildren():
			self.__parseScreen(n, self.retval)

	def execute(self):
		root = etree.fromstring(self.input_data)

		self.__parseScreenSpec(root)

		return self.retval
