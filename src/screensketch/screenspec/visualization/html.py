'''
Created on May 18, 2013

@author: Krzysztof Spisak-Spisacki
'''

from types import MethodType
from lxml import etree as ET
import screensketch.screenspec.model as orginal


def ScreenSpec_att_to_html(self):
	htmlNode = ET.Element('html')
	bodyNode = ET.SubElement(htmlNode, 'body')

	for c in self.children:
		c.to_html(bodyNode)

	output = StringIO.StringIO()
	ET.ElementTree(node).write(output, pretty_print=True, encoding='UTF-8')

	return output.getvalue()

def Screen_att_to_html(self, parent):
	tableNode = ET.SubElement(parent, 'table')
	tableNode.set('id', self.find('name').text)
	tableBody = ET.SubElement(tableNode, 'tbody')
	
	for c in self.find('children').children:
		c.to_html(tableBody)

	return tableNode

def Component_att_to_html(self, parent):
	tr = ET.SubElement(parent, 'tr')
	tr.set('colspan', '2')
	tr.set('id', self.find('identifier').text)
	tr.set('class', 'merged')
	td = ET.SubElement(tr, 'td')
	
	htmlElement = __createHtmlElement(td, 
						self.get('type'), 
						self.find('values'), 
						self.find('identifier').text)

def ComoundComponent_att_to_html(self, parent):
	pass

def StaticValue_att_to_html(self, parent):
	pass

def StaticValueContainer_att_to_html(self, parent):
	pass

def __createHtmlElement(self, parent, type, values, id):
	elm = None
	if ('BUTTON' == type):
		elm = ET.SubElement(parent, 'input')
		elm.set('type', 'button')
		elm.set('value', values.find('value').text)
	elif ('LINK' == type):
		elm = ET.SubElement(parent, 'a')
		elm.set('href', 'link')
		elm.text = values.find('value').text
		ET.SubElement(parent, 'br')
	elif ('STATIC_TEXT' == type):
		elm = ET.SubElement(parent, 'span')
		elm.text = values.find('value').text
	elif ('RADIO_BUTTONS' == type):		
		for c in values.findAll('value'):			
			elm = ET.SubElement(parent, 'input')
			elm.set('type', 'radio')
			elm.set('name', id)
			elm.set('value', c.text)
			if c.get('selected') == 'True':
				elm.set('checked', '')
			ET.SubElement(parent, 'br')
	elif ('CHECK_BOXES' == type):
		for c in values.findAll('value'):			
			elm = ET.SubElement(parent, 'input')
			elm.set('type', 'checkbox')
			elm.set('name', id)
			elm.set('value', c.text)
			if c.get('selected') == 'True':
				elm.set('checked', '')
			ET.SubElement(parent, 'br')
	elif ('COMBO_BOX' == type):
		elm = ET.SubElement(parent, 'select')
		for c in values.findAll('value'):			
			option = ET.SubElement(elm, 'option')
			option.set('value', c.text)
			option.text = c.text
	elif ('LIST_BOX' == type):
		elm = ET.SubElement(parent, 'select')
		elm.set('multiple', 'multiple')
		for c in values.findAll('value'):			
			option = ET.SubElement(elm, 'option')
			option.set('value', c.text)
			option.text = c.text
	elif ('EDIT_BOX' == type):
		elm = ET.SubElement(parent, 'input')
		elm.set('type', 'text')
		elm.set('value', values.find('value').text)
	elif ('TEXT_AREA' == type):
		elm = ET.SubElement(parent, 'textarea')
		elm.text = values.find('value').text
		
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
