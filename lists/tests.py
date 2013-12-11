from django.core.urlresolvers import resolve

from django.test import TestCase
from django.template.loader import render_to_string

from django.http import HttpRequest

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
		
		self.assertRedirects( response, '/lists/the-only-list-in-theworld/')
			
	
class ListAndItemModelTest( TestCase ):
	def test_saving_and_retrieving_items( self):
	
		list_ = List()
		list_.save()
		
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		first_item.save()
		
		second_item = Item()
		second_item.text = 'Item the seconduo' 
		second_item.list = list_
		second_item.save()
		
		
		saved_lists = List.objects.all()
		self.assertEqual( saved_lists.count(), 1 )
		self.assertEqual( saved_lists[0], list_ )
		
		
		saved_items = Item.objects.all()
		self.assertEqual( saved_items.count(), 2 )
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		
		self.assertEqual( first_saved_item.text, 'The first (ever) list item' )
		self.assertEqual( first_saved_item.list, list_ )
		
		self.assertEqual( second_saved_item.text, 'Item the seconduo' )
		self.assertEqual( second_saved_item.list, list_ )
		
		
class ListViewTest( TestCase ):
	def test_displays_all_items( self ):
		list_ = List.objects.create()
		
		Item.objects.create( text='itemmmmm 1' , list=list_)
		Item.objects.create( text='itemmmm 2'  , list=list_)

		response = self.client.get( '/lists/the-only-list-in-theworld/' )
		
		self.assertContains( response, 'itemmmmm 1')
		self.assertContains( response, 'itemmmm 2' )
# 		self.assertContains( response, )

	def test_uses_list_template( self ) :
		response = self.client.get( '/lists/the-only-list-in-theworld/' )
		self.assertTemplateUsed( response, 'list.html' )
			