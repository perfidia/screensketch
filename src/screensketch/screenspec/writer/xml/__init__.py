'''
Created on Dec 29, 2012

@author: Bartosz Alchimowicz
'''

import reflection

class XMLWriter(object):
	def __init__(self, screenspec):
		self.screenspec = screenspec

	def execute(self, fd):
		reflection.attach()
		retval = self.screenspec.to_xml()
		reflection.detach()

		fd.write(retval)

		return fd
