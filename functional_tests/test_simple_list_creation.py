from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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

	
