'''
Created on Dec 9, 2012

@author: Bartosz Alchimowicz
'''

import os
import unittest
from StringIO import StringIO
from screensketch.screenspec.reader import TextReader
from screensketch.screenspec.writer import TextWriter
from screensketch.screenspec.reader import XMLReader
from screensketch.screenspec.writer import XMLWriter

class Test(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		path = os.getcwd().split(os.sep)

		for d in reversed(path[:]):
			if d != 'tests':
				path.pop()
				continue

			break

		path.pop()

		path.append('samples')
		path.append('screenspec')

		cls.path = os.sep.join(path)

	def wrapper(self, filename):
		tmp_fd = StringIO()

		input_text = open(filename).read()
		input_model = TextReader(input_text).execute()

		XMLWriter(input_model).execute(tmp_fd)
		output_model = XMLReader(tmp_fd.getvalue()).execute()

		tmp_fd = StringIO()
		TextWriter(output_model).execute(tmp_fd)

		tmp0 = input_text.split('\n')
		tmp1 = tmp_fd.getvalue().split('\n')

		self.assertEqual(len(tmp0), len(tmp1))

		for i, j in zip(tmp0, tmp1):
			self.assertEqual(i, j)

	def testExample01(self):
		self.wrapper(self.path + "/example01.txt")

	def testExample02(self):
		self.wrapper(self.path + "/example02.txt")

	def testExample03(self):
		self.wrapper(self.path + "/example03.txt")

	def testExample04(self):
		self.wrapper(self.path + "/example04.txt")

if __name__ == "__main__":
	raise Exception("Run from project root directory")
	unittest.main()
