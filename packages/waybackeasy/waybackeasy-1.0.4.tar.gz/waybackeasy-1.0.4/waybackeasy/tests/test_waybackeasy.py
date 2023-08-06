# writing some tests
import unittest
from ..waybackeasy import *

class Tests(unittest.TestCase):
	""" some basic testing of waybackeasy get function """
	
	# checking normal retrieval from WB-machine	
	def test_get_func(self):		
		for each in ["https://news.ycombinator.com", "news.ycombinator.com", "https://news.ycombinator.com/"]:
			result = get(each, "27.05.2016")
			if "INTERNET ARCHIVE ON" in result:
				wbmachine_check = True
			self.assertTrue(wbmachine_check)

	# checking appropriate Error rendering
	def test_url_format_errors(self):
		self.assertRaises(FormatError, get, "ttttt", "27.05.2016")

	def test_date_format_errors(self):
		self.assertRaises(FormatError, get, "https://news.ycombinator.com", "2705.20166")

"""
way to run test:
cd into first waybackeasy directory, that which includes setup.py etc.
then run: python -m unittest waybackeasy.tests.test_waybackeasy
-- this is due to Python's weiredness with importing modules from sibling/parent directories. odd.
"""
