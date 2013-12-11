from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.shortcuts 

from lists.models import Item

# Create your views here.
def home_page( request ):

	if request.method == 'POST':
		new_text = request.POST['item_text']
		Item.objects.create( text=new_text )
		return redirect('/')
	
	items = Item.objects.all()
	
	return render( request, 'home.html', {
		'items': items
	})
