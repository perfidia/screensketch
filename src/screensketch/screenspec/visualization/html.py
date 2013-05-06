from types import MethodType
import screensketch.screenspec.model as orginal

def ScreenSpec_att_to_html(self):
	pass

def Screen_att_to_html(self, parent):
	pass

def Component_att_to_html(self, parent):
	pass

def ComoundComponent_att_to_html(self, parent):
	pass

def StaticValue_att_to_html(self, parent):
	pass

def StaticValueContainer_att_to_html(self, parent):
	pass

attachments = {
	orginal.ScreenSpec:           ScreenSpec_att_to_html,
	orginal.Screen:               Screen_att_to_html,
	orginal.Component:            Component_att_to_html,
	orginal.ComoundComponent:     ComoundComponent_att_to_html,
	orginal.StaticValue:          StaticValue_att_to_html,
	orginal.Button:               StaticValueContainer_att_to_html,
	orginal.Link:                 StaticValueContainer_att_to_html,
	orginal.StaticText:           StaticValueContainer_att_to_html,
	orginal.EditBox:              StaticValueContainer_att_to_html,
	orginal.TextArea:             StaticValueContainer_att_to_html,
	orginal.ComboBox:             StaticValueContainer_att_to_html,
	orginal.ListBox:              StaticValueContainer_att_to_html,
	orginal.RadioButtons:         StaticValueContainer_att_to_html,
	orginal.CheckBoxes:   	      StaticValueContainer_att_to_html,
}

def attach():
	for clazz in attachments:
		method = attachments[clazz]
		clazz.to_html = MethodType(method, None, clazz)

def detach():
	for clazz in attachments:
		del clazz.to_html
