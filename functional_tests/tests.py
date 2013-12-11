from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import unittest
import time


class NewVisitorTest(unittest.TestCase): #1

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
		self.browser.get('http://localhost:8000')

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
		
		self.check_for_row_in_table( '1: Buy peacock feathers' )
		
		# there is still a text box
		inputbox = self.browser.find_element_by_id( 'id_new-item')
		inputbox.send_keys( 'Use feathers to fly')
		inputbox.send_keys( Keys.ENTER )
		
		# the page updates and shows both elements
		self.check_for_row_in_table( '1: Buy peacock feathers' )
		self.check_for_row_in_table( '2: Use feathers to fly' )
		
		self.fail('Finish the test!') #6

		# She is invited to enter a to-do item straight away
#		  [...rest of comments as before]

if __name__ == '__main__': #7
	unittest.main(warnings='ignore') #8