'''
Created on Jun 01, 2013

@author: Krzysztof Spisak-Spisacki
'''

import html

class HTMLRenderer(object):
    def __init__(self, screenspec):
        self.screenspec = screenspec

    def execute(self, fd):
        html.attach()
        retval = self.screenspec.to_html()
        html.detach()

        fd.write(retval)

        return fd