#!/usr/bin.env python

import sys
import logging

from screensketch.screenspec.reader import TextReader
from screensketch.screenspec.writer import TextWriter
from screensketch.screenspec.writer import XMLWriter
from screensketch.screenspec.rendering import HTMLRendering

FORMAT = '%(levelname)-7s %(message)s'


logging.basicConfig(format = FORMAT, level = logging.DEBUG)

#logging.disable(logging.DEBUG)

logger = logging.getLogger("root")

logger.info("START")

input_data = open("../data/screenspec/example01.txt").read()
#input_data = open("../data/screenspec/example02.txt").read()
#input_data = open("../data/screenspec/example03.txt").read()
#input_data = open("../data/screenspec/example04.txt").read()

retval = TextReader(input_data).execute()

#TextWriter(retval).execute(sys.stdout)

print retval.children[0].children[1].identifier
retval.children[0].children[1]._grid = [["a", "b"], ["c", "d"]]
#print retval.children[0].children[0].values

f = open("tar.xml",'w');
XMLWriter(retval).execute(f)
f.close();

HTMLRendering(retval).execute()



logger.info("END")
