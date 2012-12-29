'''
Created on Dec 29, 2012

@author: Bartosz Alchimowicz
'''

from types import MethodType
import screensketch.screenspec.model as orginal

def ScreenSpec_att_to_text(self, indent = -1):
		return "\n".join([c.to_text(indent + 1) for c in self.children])

def Screen_att_to_text(self, indent = 0):
		indention = "\t" * indent
		retval = "%sSCREEN %s:\n" % (indention, self.name)

		retval += "".join([c.to_text(indent + 1) for c in self.children])

		return retval

def Component_att_to_text(self, indent):
		indention = "\t" * indent

		if self.name is not None:
			return "%s%s(%s)\n" % (indention, self.identifier, self.name)

		return "%s%s\n" % (indention, self.identifier)

def ComoundComponent_att_to_text(self, indent):
		indention = "\t" * indent

		retval = "%s%s(%s):\n" % (indention, self.identifier, self.name)
		retval += "".join([c.to_text(indent + 1) for c in self.children])

		return retval

def StaticValue_att_to_text(self, indent):
		indention = "\t" * indent

		retval = "%s%s(%s)" % (indention, self.identifier, self.name)

		if self._static_values is not None:
			retval += ": " + "|".join([i.value if i.selected == False else "=%s" % i.value for i in self._get_static_values()]) + "\n"
		elif isinstance(self, orginal.ComoundComponent) and len(self.children) > 0:
			retval += ":\n" + "".join([c.to_text(indent + 1) for c in self.children])
		else:
			retval += "\n"

		return retval

#def Button_att_to_text(self, indent):
#		return orginal.StaticValue.to_text(self, indent)
#
#def Link_att_to_text(self, indent):
#		return orginal.StaticValue.to_text(self, indent)
#
#def StaticText_att_to_text(self, indent):
#		return orginal.StaticValue.to_text(self, indent)
#
#def EditBox_att_to_text(self, indent):
#		return orginal.StaticValue.to_text(self, indent)
#
#def TextArea_att_to_text(self, indent):
#		return orginal.StaticValue.to_text(self, indent)
#
#def ComboBox_att_to_text(self, indent):
#		return orginal.StaticValue.to_text(self, indent)
#
#def ListBox_att_to_text(self, indent):
#		return orginal.StaticValue.to_text(self, indent)
#
#def RadioButtons_att_to_text(self, indent):
#		return orginal.StaticValue.to_text(self, indent)
#
#def CheckBoxes_att_to_text(self, indent):
#		return orginal.StaticValue.to_text(self, indent)

attachments = {
	orginal.ScreenSpec:       ScreenSpec_att_to_text,
	orginal.Screen:           Screen_att_to_text,
	orginal.Component:        Component_att_to_text,
	orginal.ComoundComponent: ComoundComponent_att_to_text,
	orginal.StaticValue:      StaticValue_att_to_text,
	orginal.Button:           StaticValue_att_to_text,
	orginal.Link:             StaticValue_att_to_text,
	orginal.StaticText:       StaticValue_att_to_text,
	orginal.EditBox:          StaticValue_att_to_text,
	orginal.TextArea:         StaticValue_att_to_text,
	orginal.ComboBox:         StaticValue_att_to_text,
	orginal.ListBox:          StaticValue_att_to_text,
	orginal.RadioButtons:     StaticValue_att_to_text,
	orginal.CheckBoxes:   	  StaticValue_att_to_text,
}

def attach():
	for clazz in attachments:
		method = attachments[clazz]
		clazz.to_text = MethodType(method, None, clazz)

def detach():
	for clazz in attachments:
		del clazz.to_text
