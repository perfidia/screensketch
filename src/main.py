#!/usr/bin.env python

import logging

from screensketch.screenspec.reader import TextReader

FORMAT = '%(levelname)-7s %(message)s'


logging.basicConfig(format = FORMAT, level = logging.DEBUG)

#logging.disable(logging.DEBUG)

logger = logging.getLogger("root")

logger.info("START")

input_data = open("../data/screenspec/example01.txt").read()
#input_data = open("../data/screenspec/example02.txt").read()
#input_data = open("../data/screenspec/example03.txt").read()

retval = TextReader(input_data).execute()

print retval.to_text(),

logger.info("END")
