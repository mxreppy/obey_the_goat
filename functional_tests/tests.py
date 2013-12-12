from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import unittest
import time


class NewVisitorTest(LiveServerTestCase): #1

	def setUp(self): #2
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait( 3 )
	
	def tearDown(self): #3
		self.browser.quit()
		
	def check_for_row_in_table( self, row_text ):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name( 'tr' )
		
		self.assertIn( row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self): #4
		# Edith has heard about a cool new online to-do app. She goes
		# to check out its homepage
# 		self.browser.get('http://localhost:8000')
		self.browser.get( self.live_server_url) 

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
		
		self.browser.get( self.live_server_url )	
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

		
# 		self.fail('Finish the test!') #6

		# She is invited to enter a to-do item straight away
#		  [...rest of comments as before]

	def test_layout_and_styling( self ) :
		# Edith goes to the home page
		self.browser.get( self.live_server_url )
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
		
		

# if __name__ == '__main__': #7
# 	unittest.main(warnings='ignore') #8