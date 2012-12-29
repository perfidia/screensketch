# -*- coding: utf-8 -*-

from lex import tokens
from screensketch.screenspec.model import *

import ply.yacc as yacc
import sys
import inspect
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# indention
ind_list = []
ind_length = None
ind_counter = None

######################################################
# statement
######################################################

def p_spec(p):
	'''spec : screen
	        | spec screen
	'''

	logger.debug(">>> " + inspect.stack()[0][3])

	if isinstance(p[1], ScreenSpec):
		p[1].append(p[2])
		p[0] = p[1]
	else:
		p[0] = ScreenSpec().append(p[1])

	assert p[0] != None

	logger.debug("<<< " + inspect.stack()[0][3])

def p_screen(p):
	'''screen : header component_list
	'''

	logger.debug(">>> " + inspect.stack()[0][3])

	p[0] = p[1]

	assert p[0] != None

	logger.debug("<<< " + inspect.stack()[0][3])

def p_header(p):
	'''header : SCREEN SPACE IDENTIFIER COLON ENDL
	'''

	global ind_list
	global ind_counter

	logger.debug(">>> " + inspect.stack()[0][3])

	retval = Screen(p[3])

	# restore all globals to default
	ind_list = [retval]
	ind_counter = 0

	p[0] = retval

	assert p[0] != None

	logger.debug("<<< " + inspect.stack()[0][3])

def p_component_list(p):
	'''component_list : component_item
	                  | component_list component_item
	'''

	logger.debug(">>> " + inspect.stack()[0][3])

	p[0] = "FALLTHROUGHT"

	assert p[0] != None

	logger.debug("<<< " + inspect.stack()[0][3])

def p_component_item(p):
	'''component_item : whitespace IDENTIFIER ENDL
	                  | whitespace IDENTIFIER BRACKET_ROUND_L component_type BRACKET_ROUND_R ENDL
	                  | whitespace IDENTIFIER BRACKET_ROUND_L component_type BRACKET_ROUND_R COLON ENDL
	                  | whitespace IDENTIFIER BRACKET_ROUND_L component_type BRACKET_ROUND_R COLON SPACE static_values ENDL
	'''

	# This function contains most of the logic

	global ind_list
	global ind_length
	global ind_counter

	logger.debug(">>> " + inspect.stack()[0][3])

	# set indention for further checking
	if ind_length == None:
		ind_length = len(p[1])

	ind_current = len(p[1])/ind_length

	# create instance of of component_type
	if len(p) == 4:
		retval = Entity(p[2])
	else:
		retval = p[4](p[2])

	# perform some checking of input file
	#this checking should include also parent...
	#if len(p) == 7 and isinstance(retval, ComoundComponent):
	#	raise Exception("Syntax error: lack of ':' in:" + str(p.slice))

	if ind_counter > ind_current:
		diff = ind_counter - ind_current
		ind_list = ind_list[:-diff]
	elif ind_counter < ind_current:
		diff = ind_current - ind_counter

		if diff != 1:
			raise Exception("Syntax error: wrong indention in:" + str(p.slice))

	# set static_values
	if len(p) == 10:
		retval.static_values = p[8]

	# add item to a parent
	ind_list[-1].append(retval)

	# update list with parents
	if isinstance(retval, ComoundComponent) and len(p) != 10:
		ind_list.append(retval)

	# set new indention
	ind_counter = ind_current

	p[0] = "FALLTHROUGHT"

	assert p[0] != None

	logger.debug("<<< " + inspect.stack()[0][3])

def p_component_type(p):
	'''component_type : basic_type
	                  | semi_compound_type
	                  | compound_type
	'''

	logger.debug(">>> " + inspect.stack()[0][3])

	p[0] = p[1]

	assert p[0] != None

	logger.debug("<<< " + inspect.stack()[0][3])

def p_static_values(p):
	'''static_values : static_value
	                 | static_values PIPE static_value
	'''

	selected = False

	if len(p) == 2:
		if p[1][0] == '=':
			value = p[1][1:]
			selected = True
		else:
			value = p[1]

		p[0] = [StaticValue(value, selected)]
	else:
		if p[3][0] == '=':
			value = p[3][1:]
			selected = True
		else:
			value = p[3]

		p[1].append(StaticValue(value, selected))
		p[0] = p[1]

	assert p[0] != None

def p_static_value(p):
	'''static_value : IDENTIFIER
	                | BRACKET_ROUND_L
	                | BRACKET_ROUND_R
	                | COLON
	                | DIGIT
	                | OTHER
	                | static_value IDENTIFIER
	                | static_value BRACKET_ROUND_L
	                | static_value BRACKET_ROUND_R
	                | static_value COLON
	                | static_value DIGIT
	                | static_value OTHER
	                | static_value SPACE IDENTIFIER
	                | static_value SPACE BRACKET_ROUND_L
	                | static_value SPACE BRACKET_ROUND_R
	                | static_value SPACE COLON
	                | static_value SPACE DIGIT
	                | static_value SPACE OTHER
	'''

	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 3:
		p[0] = p[1] + p[2]
	else:
		p[0] = p[1] + p[2] + p[3]

	assert p[0] != None

def p_basic_type(p):
	'''basic_type : BUTTON
	              | LINK
				  | IMAGE
				  | STATIC_TEXT
				  | DYNAMIC_TEXT
				  | EDIT_BOX
				  | CHECK_BOX
				  | RADIO_BUTTON
				  | TEXT_AREA
				  | PASSWORD
				  | CUSTOM
	'''

	p[0] = {
		'BUTTON': Button,
		'LINK': Link,
		'IMAGE': Image,
		'STATIC_TEXT': StaticText,
		'DYNAMIC_TEXT': DynamicText,
		'EDIT_BOX': EditBox,
		'CHECK_BOX': CheckBox,
		'RADIO_BUTTON': RadioButton,
		'TEXT_AREA': TextArea,
		'PASSWORD': Password,
		'CUSTOM': Custom,
	}.get(p[1])

	assert p[0] != None

def p_semi_compound_type(p):
	'''semi_compound_type : COMBO_BOX
						  | LIST_BOX
						  | RADIO_BUTTONS
						  | CHECK_BOXES
	'''

	p[0] = {
		'COMBO_BOX': ComboBox,
		'LIST_BOX': ListBox,
		'RADIO_BUTTONS': RadioButtons,
		'CHECK_BOXES': CheckBoxes,
	}.get(p[1])

	assert p[0] != None

def p_compound_type(p):
	'''compound_type : SIMPLE
	                 | LIST
				     | TABLE
	'''

	p[0] = {
		'SIMPLE': Simple,
		'LIST': List,
		'TABLE': Table,
	}.get(p[1])

	assert p[0] != None

def p_whitespace(p):
	'''whitespace : SPACE
	              | TAB
	              | whitespace SPACE
	              | whitespace TAB
	'''

	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = p[1] + p[2]

	assert p[0] != None

# Error rule for syntax errors
def p_error(p):
	logger.error("YACC error: " + str(p))
	raise Exception("Syntax error")
	sys.exit(1)

######################################################

if __name__ == "__main__":
	filename = '../../../../data/screenspec/example01.txt'
#	filename = '../../../../data/screenspec/example02.txt'
#	filename = '../../../../data/screenspec/example03.txt'

	data = open(filename, "r").read()

	#log = logging.getLogger("parser")
	log = logging.getLogger()
	#handler = logging.StreamHandler()
	handler = logging.FileHandler('parselog.txt', mode = 'w', encoding = None, delay = False)
	formatter = logging.Formatter('%(filename)10s:%(lineno)4d:%(message)s')
	handler.setFormatter(formatter)
	log.addHandler(handler)

	parser = yacc.yacc(debug = True, debuglog = log)
	result = parser.parse(data, debug = log)

	print result.to_text()

	print "-"*10
