'''
Created on Dec 9, 2012

@author: Bartosz Alchimowicz
'''

import unittest
from screensketch.screenspec.reader import Reader

class Test(unittest.TestCase):
	def wrapper(self, filename):
		input = open(filename).read()
		output = Reader(input).execute()

		tmp0 = input.split('\n')
		tmp1 = output.to_text().split('\n')

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
