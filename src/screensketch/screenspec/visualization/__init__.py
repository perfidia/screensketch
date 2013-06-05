'''
Created on Jun 01, 2013

@author: Krzysztof Spisak-Spisacki
'''

import html
import xml.etree.ElementTree as xml

class HTMLRenderer(object):
    def __init__(self, screenspec):
        self.screenspec = screenspec

    def execute(self, fd):
        html.attach()
        retval = self.screenspec.to_html()
        html.detach()

        fd.write(xml.tostring(retval))

        return fd