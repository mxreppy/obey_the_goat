from django.core.urlresolvers import resolve

from django.test import TestCase
from django.template.loader import render_to_string

from django.http import HttpRequest
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List

# Create your tests here.
class SmokeTest(TestCase):

	def test_root_url_resolves_to_homepageview( self):
		found = resolve('/')
		self.assertEqual( found.func, home_page)
		
	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page( request) 
		expected_html = render_to_string( 'home.html' )
		self.assertEqual( response.content.decode(), expected_html )
	
class NewListTest( TestCase ): 
		
	def test_saving_a_POST_request(self):
		self.client.post( 
			'/lists/new',
			data={'item_text': 'A new list item' } 
		)
				
		self.assertEqual( Item.objects.all().count(), 1)
		new_item = Item.objects.all()[0]
		self.assertEqual( new_item.text, 'A new list item' )
			
	def test_redirects_after_POST_request(self):
		response = self.client.post( 
			'/lists/new',
			data={'item_text': 'A new list item' } 
		)
		
		new_list = List.objects.all()[0]
		self.assertRedirects( response, '/lists/%d/' % (new_list.id,) )
			
	def test_validation_errors_sent_back_to_home_page( self ):
		response = self.client.post( '/lists/new', data={'item_text': '' } )
		self.assertEqual( Item.objects.all().count(), 0 )
		self.assertTemplateUsed( response, 'home.html' )
		expected_error = escape( "You can't have an empty list item" )
# 		print( response.content.decode() )
		self.assertContains( response, expected_error )
	
	
		
class ListViewTest( TestCase ):

	def test_displays_only_correct_items( self ):
		correct_list = List.objects.create()
		
		Item.objects.create( text='itemmmmm 1' , list=correct_list)
		Item.objects.create( text='itemmmm 2'  , list=correct_list)

		other_list = List.objects.create()
		
		Item.objects.create( text='yucky 1' , list=other_list)
		Item.objects.create( text='yucky 2'  , list=other_list)

		response = self.client.get( '/lists/%d/' % (correct_list.id,) )
		
		self.assertContains( response, 'itemmmmm 1')
		self.assertContains( response, 'itemmmm 2' )
		self.assertNotContains( response, 'yucky 1' )
		self.assertNotContains( response, 'yucky 2' )
		
# 		self.assertContains( response, )

	def test_uses_list_template( self ) :
	
		itemlist = List.objects.create()
		
		response = self.client.get( '/lists/%d/' % (itemlist.id,) )
		self.assertTemplateUsed( response, 'list.html' )
		
	def test_passes_correct_list_to_template( self ):
		other_list = List.objects.create()
		current_list = List.objects.create()
		
		response = self.client.get( '/lists/%d/' % (current_list.id,))
		
		self.assertEqual( response.context['list'], current_list )
		
class NewItemTest( TestCase ) :

	def test_can_save_a_POST_request_to_an_existing_list( self ): 
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		self.client.post( 
			'/lists/%d/new_item' % (correct_list.id, ),
			data={'item_text' : 'A new item for an existing list' } 
		)
		
		self.assertEqual( Item.objects.all().count(), 1 )
		new_item = Item.objects.all()[0]
		self.assertEqual( new_item.text, 'A new item for an existing list' ) 
		self.assertEqual( new_item.list, correct_list )		
		
	def test_redirects_to_list_view( self ):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		response = self.client.post( 
			'/lists/%d/new_item' % (correct_list.id, ),
			data={'item_text' : 'A new item for an existing list' } 
		)
		
		self.assertRedirects( response, '/lists/%d/' % (correct_list.id, ) )
		