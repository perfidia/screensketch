#!/usr/bin.env python

import sys
import logging

from screensketch.screenspec.reader import TextReader
from screensketch.screenspec.writer import TextWriter


FORMAT = '%(levelname)-7s %(message)s'


logging.basicConfig(format = FORMAT, level = logging.DEBUG)

#logging.disable(logging.DEBUG)

logger = logging.getLogger("root")

logger.info("START")

input_data = open("../data/screenspec/example01.txt").read()
#input_data = open("../data/screenspec/example02.txt").read()
#input_data = open("../data/screenspec/example03.txt").read()

retval = TextReader(input_data).execute()
TextWriter(retval).execute(sys.stdout)

logger.info("END")
