#from ??? import DjangoRendering
import reading

class HTMLRendering(object):
	def __init__(self, screenspec):
		self.screenspec = screenspec

	def execute(self):
		reading.mainFunction()

	
