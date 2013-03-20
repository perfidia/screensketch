'''
Created on Apr 28, 2011

@author: Bartosz Alchimowicz
'''

############################
#        Collection        #
############################

class ScreenSpec(object):
	def __init__(self):
		self.children = []

	def append(self, screen):
		assert isinstance(screen, Screen)

		self.children.append(screen)

		return self

############################
#          Header          #
############################

class Screen(object):
	def __init__(self, name):
		assert isinstance(name, basestring)

		self.name = name
		self.children = []

	def append(self, child):
		assert isinstance(child, Component)

		self.children.append(child)

		return self

############################
#        Component         #
############################

class Component(object):
	def __init__(self, identifier, name):
		assert identifier is not None

		self.identifier = identifier
		self.name = name

class ComoundComponent(Component):
	def __init__(self, identifier, name):
		Component.__init__(self, identifier, name)
		self.children = []

	def append(self, child):
		assert isinstance(child, Component)

		self.children.append(child)

		return self

class StaticValueContainer(object):
	def __init__(self):
		self._static_values = None

	def _set_static_values(self, values):
		raise Exception("Please overwrite")

	def _get_static_values(self):
		return self._static_values

class ComoundValuesContainer(object):
	def __init__(self):
		self._grid = None # 2d lisl

############################
#     Basic Components     #
############################

class Entity(Component):
	def __init__(self, identifier):
		Component.__init__(self, identifier, None)

class Button(Component, StaticValueContainer):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "BUTTON")
		StaticValueContainer.__init__(self)

	def _set_static_values(self, values):
		if len(values) != 1:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValueContainer._get_static_values, _set_static_values)

class Link(Component, StaticValueContainer):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "LINK")
		StaticValueContainer.__init__(self)

	def _set_static_values(self, values):
		if len(values) != 1:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValueContainer._get_static_values, _set_static_values)

class Image(Component):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "IMAGE")

class StaticText(Component, StaticValueContainer):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "STATIC_TEXT")
		StaticValueContainer.__init__(self)

	def _set_static_values(self, values):
		if len(values) != 1:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValueContainer._get_static_values, _set_static_values)

class DynamicText(Component):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "DYNAMIC_TEXT")

class EditBox(Component, StaticValueContainer):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "EDIT_BOX")
		StaticValueContainer.__init__(self)

	def _set_static_values(self, values):
		if len(values) != 1:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValueContainer._get_static_values, _set_static_values)

class CheckBox(Component):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "CHECK_BOX")

class RadioButton(Component):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "RADIO_BUTTON")

class TextArea(Component, StaticValueContainer):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "TEXT_AREA")
		StaticValueContainer.__init__(self)

	def _set_static_values(self, values):
		if len(values) == 0:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValueContainer._get_static_values, _set_static_values)

class Password(Component):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "PASSWORD")

class Custom(Component):
	def __init__(self, identifier):
		assert False and "Modify screenspec.parser to add custom components"

############################
# Semi-Compound Components #
############################

class ComboBox(ComoundComponent, StaticValueContainer):
	def __init__(self, identifier):
		ComoundComponent.__init__(self, identifier, "COMBO_BOX")
		StaticValueContainer.__init__(self)

	def _set_static_values(self, values):
		if len(values) == 0:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValueContainer._get_static_values, _set_static_values)

class ListBox(ComoundComponent, StaticValueContainer):
	def __init__(self, identifier):
		ComoundComponent.__init__(self, identifier, "LIST_BOX")
		StaticValueContainer.__init__(self)

	def _set_static_values(self, values):
		if len(values) == 0:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValueContainer._get_static_values, _set_static_values)

class RadioButtons(ComoundComponent, StaticValueContainer):
	def __init__(self, identifier):
		ComoundComponent.__init__(self, identifier, "RADIO_BUTTONS")
		StaticValueContainer.__init__(self)

	def _set_static_values(self, values):
		if len(values) == 0:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValueContainer._get_static_values, _set_static_values)

class CheckBoxes(ComoundComponent, StaticValueContainer):
	def __init__(self, identifier):
		ComoundComponent.__init__(self, identifier, "CHECK_BOXES")
		StaticValueContainer.__init__(self)

	def _set_static_values(self, values):
		if len(values) == 0:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValueContainer._get_static_values, _set_static_values)

############################
#    Compound Components   #
############################

class Simple(ComoundComponent, ComoundValuesContainer):
	def __init__(self, identifier):
		ComoundComponent.__init__(self, identifier, "SIMPLE")
		ComoundValuesContainer.__init__(self)

class List(ComoundComponent, ComoundValuesContainer):
	def __init__(self, identifier):
		ComoundComponent.__init__(self, identifier, "LIST")
		ComoundValuesContainer.__init__(self)

class Table(ComoundComponent, ComoundValuesContainer):
	def __init__(self, identifier):
		ComoundComponent.__init__(self, identifier, "TABLE")
		ComoundValuesContainer.__init__(self)

############################
#       StaticValues       #
############################

class StaticValue(object):
	def __init__(self, value, selected = False):
		assert value != None

		self.value = value
		self.selected = selected
