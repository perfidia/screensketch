import re
import sys
import string
import ply.lex as lex

tokens = (
	'SCREEN',
	'BUTTON',
	'LINK',
	'IMAGE',
	'STATIC_TEXT',
	'DYNAMIC_TEXT',
	'EDIT_BOX',
	'CHECK_BOX',
	'RADIO_BUTTON',
	'TEXT_AREA',
	'PASSWORD',
	'CUSTOM',

	'COMBO_BOX',
	'LIST_BOX',
	'RADIO_BUTTONS',
	'CHECK_BOXES',

	'SIMPLE',
	'LIST',
	'TABLE',

	'BRACKET_ROUND_L',
	'BRACKET_ROUND_R',
	'SPACE',
	'TAB',
	'COLON',
	'ENDL',
	'PIPE',
	'OTHER',
	'DIGIT',

	'IDENTIFIER',
)

############################
#          Header          #
############################

def t_SCREEN(t):
	r'SCREEN'
	return t

############################
# Semi-Compound Components #
############################

def t_COMBO_BOX(t):
	r'COMBO_BOX'
	return t

def t_LIST_BOX(t):
	r'LIST_BOX'
	return t

def t_RADIO_BUTTONS(t):
	r'RADIO_BUTTONS'
	return t

def t_CHECK_BOXES(t):
	r'CHECK_BOXES'
	return t

############################
#     Basic Components     #
############################

def t_BUTTON(t):
	r'BUTTON'
	return t

def t_LINK(t):
	r'LINK'
	return t

def t_IMAGE(t):
	r'IMAGE'
	return t

def t_STATIC_TEXT(t):
	r'STATIC_TEXT'
	return t

def t_DYNAMIC_TEXT(t):
	r'DYNAMIC_TEXT'
	return t

def t_EDIT_BOX(t):
	r'EDIT_BOX'
	return t

def t_CHECK_BOX(t):
	r'CHECK_BOX'
	return t

def t_RADIO_BUTTON(t):
	r'RADIO_BUTTON'
	return t

def t_TEXT_AREA(t):
	r'TEXT_AREA'
	return t

def t_PASSWORD(t):
	r'PASSWORD'
	return t

def t_CUSTOM(t):
	r'CUSTOM'
	return t

############################
#    Compound Components   #
############################

def t_SIMPLE(t):
	r'SIMPLE'
	return t

def t_LIST(t):
	r'LIST'
	return t

def t_TABLE(t):
	r'TABLE'
	return t

############################
#          Other           #
############################

t_SPACE           = r'\ '
t_TAB             = r'\t'

t_BRACKET_ROUND_L = r'\('
t_BRACKET_ROUND_R = r'\)'
t_COLON           = r':'
t_ENDL            = r'\n+'
t_IDENTIFIER      = r'[A-Za-z][A-Za-z0-9_]*'
t_DIGIT           = r'[0-9]'
t_PIPE            = r'\|'
t_OTHER           = r'[-?><=]'

def t_error(t):
	print "LEX error: '%s'" % t.value
	sys.exit(1)
	# t.lexer.skip(1)

lexer = lex.lex()

############

if __name__ == "__main__":
	filename = '../../../../data/screenspec/example01.txt'
#	filename = '../../../../data/screenspec/example02.txt'
#	filename = '../../../../data/screenspec/example03.txt'

	data = open(filename, "r").read()

	lexer.input(data)
	lexer.linepos = 0

	print ">>"

	while True:
		tok = lexer.token()
		if not tok: break      # No more input

		if tok.type == 'WHITESPACE':
			value = ""
			for i in tok.value:
				value += {
					'\t': '\\t'
				}.get(i, i)

			value = ">" + value + "<"
		elif tok.type == 'ENDL':
			value = '\\n'
		else:
			value = tok.value

		print "%-20s %s" % (tok.type, value)

	print "<<"
