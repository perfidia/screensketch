'''
Created on Dec 9, 2012

@author: Bartosz Alchimowicz
'''

import os
import unittest
from StringIO import StringIO
from screensketch.screenspec.reader import TextReader
from screensketch.screenspec.writer import TextWriter

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

		input = open(filename).read()
		output = TextReader(input).execute()

		tmp0 = input.split('\n')

		TextWriter(output).execute(tmp_fd)
		tmp1 = tmp_fd.getvalue().split('\n')

		self.assertEqual(len(tmp0), len(tmp1))

		for idx, val in enumerate(tmp0):
			self.assertEqual(val, tmp1[idx])

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
