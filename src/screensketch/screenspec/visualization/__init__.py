'''
Created on Jun 01, 2013

@author: Krzysztof Spisak-Spisacki
'''

import html
import xml.etree.ElementTree as xml
import lxml.etree as etree

class HTMLRenderer(object):
    def __init__(self, screenspec):
        self.screenspec = screenspec

    def execute(self, fd):
        html.attach()
        retval = self.screenspec.to_html()
        html.detach()

        tree = etree.fromstring(xml.tostring(retval, encoding='utf8', method='xml'))
         
        fd.write(etree.tostring(tree, pretty_print=True))

        return fd