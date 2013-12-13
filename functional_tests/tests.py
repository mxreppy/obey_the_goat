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
			print( "sys argv is " + arg)
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.split('=')[1]
				return
		LiveServerTestCase.setUpClass()
		print( "setting cls.server_url")
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

class NewVisitorTest( FunctionalTest ):

	def test_can_start_a_list_and_retrieve_it_later(self): #4
		# Edith has heard about a cool new online to-do app. She goes
		# to check out its homepage
# 		self.browser.get('http://localhost:8000')
		self.browser.get( self.server_url) 

		# She notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title) #5
		
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn( 'To-Do', header_text )
		
		# She is invited to enter a todo item straightaway
		inputbox = self.browser.find_element_by_id( 'id_new-item')
		self.assertEqual( 
				inputbox.get_attribute('placeholder'),
				'Enter a to-do item'
		)
		
		# She types blah into textbox
		inputbox.send_keys( 'Buy peacock feathers')
		
		# when she hits enter, the page updates and lists the todo
		inputbox.send_keys( Keys.ENTER )
		
		# Check URL to see if we redirected to a /lists path
		edith_list_url = self.browser.current_url
		self.assertRegex( edith_list_url, '/lists/.+')
		
		self.check_for_row_in_table( '1: Buy peacock feathers' )
		
		# there is still a text box
		inputbox = self.browser.find_element_by_id( 'id_new-item')
		inputbox.send_keys( 'Use feathers to fly')
		inputbox.send_keys( Keys.ENTER )
		
		# the page updates and shows both elements
		self.check_for_row_in_table( '1: Buy peacock feathers' )
		self.check_for_row_in_table( '2: Use feathers to fly' )
		
		
		# Francis also visits (from a new browser), and sees his own data (not ediths)
		self.browser.quit()
		self.browser = webdriver.Firefox()
		
		self.browser.get( self.server_url )	
		page_text = self.browser.find_element_by_tag_name( 'body' ).text
		self.assertNotIn( 'Buy peacock feathers', page_text )
		self.assertNotIn( 'feathers to fly' , page_text )
		
		# Francis starts a new list
		inputbox = self.browser.find_element_by_id( 'id_new-item')
		inputbox.send_keys( 'buy milk')
		inputbox.send_keys( Keys.ENTER )
		
		# Francis gets a unique url
		francis_url = self.browser.current_url
		self.assertRegex( francis_url, '/lists/.+' )
		self.assertNotEqual( francis_url, edith_list_url )

		
class LayoutAndStylingTest( FunctionalTest ):

	def test_layout_and_styling( self ) :
		# Edith goes to the home page
		self.browser.get( self.server_url )
		self.browser.set_window_size( 1024, 768 )
		
		inputbox = self.browser.find_element_by_tag_name( 'input' )
		
		self.assertAlmostEqual( 
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=3
		)
		
		inputbox.send_keys( 'testing\n' )
		
		inputbox = self.browser.find_element_by_tag_name('input')
		
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width']/2,
			512,
			delta=3
		)
		
class ItemValidationTest( FunctionalTest ):

	@skip
	def test_cannot_add_empty_list_items(self):
		# Edith goes to the home page and hits enter on an empty box
		
		# see's friendly warning error
		
		# enters text
		
		# now works
		
		# tries an empty list item on the list view page
		
		# similar wrning
		
		# but works with data
		
		self.fail( 'write test' )
		
