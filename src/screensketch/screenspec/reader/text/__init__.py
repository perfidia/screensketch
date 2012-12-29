import ply
import lex, yacc
import logging
import re
from screensketch.screenspec.model import *

logger = logging.getLogger()

class TextReader(object):
	def __init__(self, input_data):
		self.input_data = input_data

		self.debug_logger = self.__getLogger()

		#self.__lex =  ply.lex.lex(module = lex, reflags = re.UNICODE)
		self.__yacc = ply.yacc.yacc(module = yacc, debug = True, debuglog = self.debug_logger)

	def __getLogger(self):
		debug_logger = logging.getLogger("debug_parser")

		debug_logger.propagate = False

		fileHandler = logging.FileHandler('parselog.txt', mode = 'w', encoding = None, delay = False)
		formatter = logging.Formatter('%(filename)10s:%(lineno)4d:%(message)s')
		fileHandler.setFormatter(formatter)
		debug_logger.addHandler(fileHandler)

		return debug_logger

	###########################################################################
	# execute
	###########################################################################

	def execute(self):
		logger.info(">>> " + __package__)

		retval = self.__yacc.parse(self.input_data, debug = self.debug_logger)

		logger.info("<<< " + __package__)

		return retval
