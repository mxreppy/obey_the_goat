from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

	
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
		
