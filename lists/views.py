from django.shortcuts import render
from django.http import HttpResponse
# from django.shortcuts 

from lists.models import Item

# Create your views here.
def home_page( request ):

	if request.method == 'POST':
		new_text = request.POST['item_text']
		Item.objects.create( text=new_text )

	else:
		new_text = ''
			
	
	return render( request, 'home.html', {
		'new_item_text': new_text,
	})
