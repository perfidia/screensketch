'''
Created on May 18, 2013

@author: Krzysztof Spisak-Spisacki
'''

from types import MethodType
import StringIO
import xml.etree.ElementTree as xml
import screensketch.screenspec.model as orginal


def ScreenSpec_att_to_html(self):
	htmlNode = xml.Element('html')
	bodyNode = xml.Element('body')
	htmlNode.append(bodyNode)

	for c in self.children:
		c.to_html(bodyNode)

	return htmlNode

def Screen_att_to_html(self, parent):
	tableNode = xml.Element('table')
	parent.append(tableNode)
	
	tableNode.set('id', self.name)
	tableBody = xml.Element('tbody')
	tableNode.append(tableBody)
	
	for c in self.children:
		c.to_html(tableBody)

	return tableNode

def Component_att_to_html(self, parent):
	tr = xml.Element('tr')
	parent.append(tr)
	tr.set('id', self.identifier)
	
	return tr

def ComoundComponent_att_to_html(self, parent):
	for c in self.children:
		c.to_html(parent)

def StaticValue_att_to_html(self, parent):
	pass

def StaticValueContainer_att_to_html(self, parent):
	tr = xml.Element('tr')
	parent.append(tr)
	tr.set('id', self.identifier)
	td = xml.Element('td')
	tr.append(td)
	
	elm = None
	if (isinstance(self, orginal.Button)):
		tr.set('colspan', '2')
		tr.set('class', 'merged')
		elm = xml.Element('input')
		elm.set('type', 'button')
		elm.set('value', self.static_values[0])
	elif (isinstance(self, orginal.Link)):
		tr.set('colspan', '2')
		tr.set('class', 'merged')
		elm = xml.Element('a')
		elm.set('href', 'link')
		elm.text = self.static_values[0]
		td.append(xml.Element('br'))
	elif (isinstance(self, orginal.StaticText)):
		tr.set('colspan', '2')
		tr.set('class', 'merged')
		elm = xml.Element('span')
		elm.text = self.static_values[0]
	elif (isinstance(self, orginal.RadioButtons)):
		td.text = 'radio_buttons'
		innerTd = xml.Element('td')
		tr.append(innerTd)
		for c in self.static_values:
			option = xml.Element('input')
			option.set('type', 'radio')
			option.set('name', self.name)
			option.set('selected', c.selected)
			option.set('value', c.value)
			innerTd.append(option)
			innerTd.append(xml.Element('br'))
	elif (isinstance(self, orginal.CheckBoxes)):
		td.text = 'check_boxes'
		innerTd = xml.Element('td')
		tr.append(innerTd)
		for c in self.static_values:
			option = xml.Element('input')
			option.set('type', 'checkbox')
			option.set('name', self.name)
			option.set('selected', c.selected)
			option.set('value', c.value)
			innerTd.append(option)
			innerTd.append(xml.Element('br'))
	elif (isinstance(self, orginal.ComboBox)):
		td.text = 'combo_box'
		innerTd = xml.Element('td')
		tr.append(innerTd)
		select = xml.Element('select')
		innerTd.append(select)
		if self.static_values != None:
			for c in self.static_values:
				option = xml.Element('option')
				option.set('value', c.value)
				select.append(option)
	elif (isinstance(self, orginal.EditBox)):
		td.text = 'edit_box'
		elm = xml.Element('input')
		elm.set('type', 'button')
		elm.set('value', self.static_values[0])
	elif (isinstance(self, orginal.TextArea)):
		td.text = 'text_area'
		innerTd = xml.Element('td')
		tr.append(innerTd)
		elm = xml.Element('textarea')
		innerTd.append(elm)
		for c in self.static_values:
			elm.tail = c.value
	elif (isinstance(self, orginal.ListBox)):
		td.text = 'list_box'
		innerTd = xml.Element('td')
		tr.append(innerTd)
		elm = xml.Element('select')
		innerTd.append(elm)
		for c in self.static_values:
			option = xml.Element('option')
			option.set('value', c.value)
			option.text = c.value
			elm.append(option)
	return elm
	

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