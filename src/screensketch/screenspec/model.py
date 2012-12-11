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

	def to_text(self, indent = -1):
		return "\n".join([c.to_text(indent + 1) for c in self.children])

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

	def to_text(self, indent = 0):
		indention = "\t" * indent
		retval = "%sSCREEN %s:\n" % (indention, self.name)

		retval += "".join([c.to_text(indent + 1) for c in self.children])

		return retval

############################
#        Component         #
############################

class Component(object):
	def __init__(self, identifier, name):
		assert identifier is not None

		self.identifier = identifier
		self.name = name

	def to_text(self, indent):
		indention = "\t" * indent

		if self.name is not None:
			return "%s%s(%s)\n" % (indention, self.identifier, self.name)

		return "%s%s\n" % (indention, self.identifier)

class ComoundComponent(Component):
	def __init__(self, identifier, name):
		Component.__init__(self, identifier, name)
		self.children = []

	def append(self, child):
		assert isinstance(child, Component)

		self.children.append(child)

		return self

	def to_text(self, indent):
		indention = "\t" * indent

		retval = "%s%s(%s):\n" % (indention, self.identifier, self.name)
		retval += "".join([c.to_text(indent + 1) for c in self.children])

		return retval

class StaticValue(object):
	def __init__(self):
		self._static_values = None

	def _set_static_values(self, values):
		raise Exception("Please overwrite")

	def _get_static_values(self):
		return "|".join(self._static_values)

	def to_text(self, indent):
		indention = "\t" * indent

		retval = "%s%s(%s)" % (indention, self.identifier, self.name)

		if self._static_values is not None:
			retval += ": " + self._get_static_values() + "\n"
		elif isinstance(self, ComoundComponent) and len(self.children) > 0:
			retval += ":\n" + "".join([c.to_text(indent + 1) for c in self.children])
		else:
			retval += "\n"

		return retval

############################
#     Basic Components     #
############################

class Entity(Component):
	def __init__(self, identifier):
		Component.__init__(self, identifier, None)

class Button(Component, StaticValue):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "BUTTON")
		StaticValue.__init__(self)

	def _set_static_values(self, values):
		if len(values) != 1:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValue._get_static_values, _set_static_values)

	def to_text(self, indent):
		return StaticValue.to_text(self, indent)

class Link(Component, StaticValue):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "LINK")
		StaticValue.__init__(self)

	def _set_static_values(self, values):
		if len(values) != 1:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValue._get_static_values, _set_static_values)

	def to_text(self, indent):
		return StaticValue.to_text(self, indent)

class Image(Component):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "IMAGE")

class StaticText(Component, StaticValue):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "STATIC_TEXT")
		StaticValue.__init__(self)

	def _set_static_values(self, values):
		if len(values) != 1:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValue._get_static_values, _set_static_values)

	def to_text(self, indent):
		return StaticValue.to_text(self, indent)

class DynamicText(Component):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "DYNAMIC_TEXT")

class EditBox(Component, StaticValue):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "EDIT_BOX")
		StaticValue.__init__(self)

	def _set_static_values(self, values):
		if len(values) != 1:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValue._get_static_values, _set_static_values)

	def to_text(self, indent):
		return StaticValue.to_text(self, indent)

class CheckBox(Component):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "CHECK_BOX")

class RadioButton(Component):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "RADIO_BUTTON")

class TextArea(Component, StaticValue):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "TEXT_AREA")
		StaticValue.__init__(self)

	def _set_static_values(self, values):
		if len(values) == 0:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValue._get_static_values, _set_static_values)

	def to_text(self, indent):
		return StaticValue.to_text(self, indent)

class Password(Component):
	def __init__(self, identifier):
		Component.__init__(self, identifier, "PASSWORD")

class Custom(Component):
	def __init__(self, identifier):
		assert False and "Modify screenspec.parser to add custom components"

############################
# Semi-Compound Components #
############################

class ComboBox(ComoundComponent, StaticValue):
	def __init__(self, identifier):
		ComoundComponent.__init__(self, identifier, "COMBO_BOX")
		StaticValue.__init__(self)

	def _set_static_values(self, values):
		if len(values) == 0:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValue._get_static_values, _set_static_values)

	def to_text(self, indent):
		return StaticValue.to_text(self, indent)

class ListBox(ComoundComponent, StaticValue):
	def __init__(self, identifier):
		ComoundComponent.__init__(self, identifier, "LIST_BOX")
		StaticValue.__init__(self)

	def _set_static_values(self, values):
		if len(values) == 0:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValue._get_static_values, _set_static_values)

	def to_text(self, indent):
		return StaticValue.to_text(self, indent)

class RadioButtons(ComoundComponent, StaticValue):
	def __init__(self, identifier):
		ComoundComponent.__init__(self, identifier, "RADIO_BUTTONS")
		StaticValue.__init__(self)

	def _set_static_values(self, values):
		if len(values) == 0:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValue._get_static_values, _set_static_values)

	def to_text(self, indent):
		return StaticValue.to_text(self, indent)

class CheckBoxes(ComoundComponent, StaticValue):
	def __init__(self, identifier):
		ComoundComponent.__init__(self, identifier, "CHECK_BOXES")
		StaticValue.__init__(self)

	def _set_static_values(self, values):
		if len(values) == 0:
			raise Exception("Wrong number of static values")

		self._static_values = values

	static_values = property(StaticValue._get_static_values, _set_static_values)

	def to_text(self, indent):
		return StaticValue.to_text(self, indent)

############################
#    Compound Components   #
############################

class Simple(ComoundComponent):
	def __init__(self, identifier):
		ComoundComponent.__init__(self, identifier, "SIMPLE")

class List(ComoundComponent):
	def __init__(self, identifier):
		ComoundComponent.__init__(self, identifier, "LIST")

class Table(ComoundComponent):
	def __init__(self, identifier):
		ComoundComponent.__init__(self, identifier, "TABLE")
