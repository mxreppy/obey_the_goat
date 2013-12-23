from django import forms
from lists.models import Item

EMPTY_LIST_ERROR = "You can't have an empty list item"

# Example of simple form
# class ItemForm( forms.Form ):
# 	item_text = forms.CharField(
# 		widget=forms.fields.TextInput( attrs={
# 			'placeholder': 'Enter a to-do item',
# 			'class': 'form-control input-lg',
# 		}),
# 	)

# Example of model based form
class ItemForm( forms.models.ModelForm ): 
	class Meta:
		model = Item
		fields = ('text', )
		widgets= {
			'text': forms.fields.TextInput( attrs={
				'placeholder': 'Enter a to-do item',
				'class': 'form-control input-lg',
			}),
		}
	
	def save( self, for_list ): 
		self.instance.list = for_list
		return super().save()
		
		
	def __init__( self, *args, **kwargs ): 
		super().__init__( *args, **kwargs ) 
# 		empty_error = EMPTY_LIST_ERROR 
		self.fields['text'].error_messages['required'] = EMPTY_LIST_ERROR
		
	
		