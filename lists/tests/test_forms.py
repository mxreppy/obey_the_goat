from django.test import TestCase

from lists.forms import EMPTY_LIST_ERROR, ItemForm
from lists.models import Item, List


class ItemFormTest( TestCase ):

	def test_form_renders_item_text_input( self ): 
		form = ItemForm()
		
		self.assertIn( 'placeholder="Enter a to-do item"', form.as_p() )
		self.assertIn( 'class="form-control input-lg"', form.as_p() )
		
# 		self.fail( form.as_p() )

	def test_from_validation_for_blank_items( self ): 
		form = ItemForm( data={'text':''} )
		self.assertFalse( form.is_valid() )
		self.assertEqual( form.errors['text'], [EMPTY_LIST_ERROR] )
		
# 		form.save()
	def test_form_save_handles_saving_to_a_list( self ):
	
		itemlist = List.objects.create()
		
		form = ItemForm( data={'text': 'do me' } )
		new_item = form.save( for_list = itemlist )
		
		self.assertEqual( new_item, Item.objects.all()[0] )
		self.assertEqual( new_item.text, 'do me' )
		self.assertEqual( new_item.list, itemlist )
		