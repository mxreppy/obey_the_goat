from django.shortcuts import render
from django.http import HttpResponse
# from django.shortcuts 

from lists.models import Item

# Create your views here.
def home_page( request ):

# 	if request.method == 'POST':
# 		return HttpResponse(request.POST['item_text'])
# 	return render( request, 'home.html' )
	
	item = Item()
	
	item.text = request.POST.get( 'item_text', '' )
	item.save()
	
	return render( request, 'home.html', {
		'new_item_text': item.text,
	})
