from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from unittest import skip

import unittest
import time
import sys

class FunctionalTest(LiveServerTestCase): #1

	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
# 			print( "sys argv is " + arg)
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.split('=')[1]
				print( "overrided server url: %s " % ( cls.server_url, ) )
				return
		LiveServerTestCase.setUpClass()
# 		print( "setting cls.server_url")
		cls.server_url = cls.live_server_url
		
	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			LiveServerTestCase.tearDownClass()
	
	def setUp(self): #2
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait( 3 )
	
	def tearDown(self): #3
		self.browser.quit()
		
	def check_for_row_in_table( self, row_text ):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name( 'tr' )
		
		self.assertIn( row_text, [row.text for row in rows])
		
	def get_item_inputbox( self ):
		return self.browser.find_element_by_id( 'id_text' )
