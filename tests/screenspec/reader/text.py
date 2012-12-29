'''
Created on Dec 9, 2012

@author: Bartosz Alchimowicz
'''

import unittest
import StringIO
from screensketch.screenspec.reader import TextReader
from screensketch.screenspec.writer import TextWriter

class Test(unittest.TestCase):
	def wrapper(self, filename):
		tmp_fd = StringIO.StringIO()

		input = open(filename).read()
		output = TextReader(input).execute()

		tmp0 = input.split('\n')

		TextWriter(output).execute(tmp_fd)
		tmp1 = tmp_fd.getvalue().split('\n')

		self.assertEqual(len(tmp0), len(tmp1))

		for idx, val in enumerate(tmp0):
			self.assertEqual(val, tmp1[idx])

	def testExample01(self):
		self.wrapper("data/screenspec/example01.txt")

	def testExample02(self):
		self.wrapper("data/screenspec/example02.txt")

	def testExample03(self):
		self.wrapper("data/screenspec/example03.txt")

if __name__ == "__main__":
	raise Exception("Run from project root directory")
	unittest.main()
