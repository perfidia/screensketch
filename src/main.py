#!/usr/bin.env python

import sys
import logging

from xml.dom.minidom import parseString

from screensketch.screenspec.reader import TextReader
from screensketch.screenspec.writer import TextWriter
from screensketch.screenspec.writer import XMLWriter
from screensketch.screenspec.rendering import HTMLRendering
from screensketch.screenspec.visualization import HTMLRenderer

FORMAT = '%(levelname)-7s %(message)s'


logging.basicConfig(format = FORMAT, level = logging.DEBUG)

#logging.disable(logging.DEBUG)

logger = logging.getLogger("root")

logger.info("START")

number = 2   # see data folder
frmt = "txt" # txt or xml

input_data = open("../samples/screenspec/example%02d.txt" % number).read()

retval = TextReader(input_data).execute()
#TextWriter(retval).execute(sys.stdout)
#XMLWriter(retval).execute(sys.stdout)

#print retval.children[0].children[1].identifier
#retval.children[0].children[1]._grid = [["a", "b"], ["c", "d"]]
#print retval.children[0].children[0].values

#f = open("tar.xml",'w');
#XMLWriter(retval).execute(f)
#f.close();

HTMLRenderer(retval).execute(sys.stdout)

logger.info("END")
