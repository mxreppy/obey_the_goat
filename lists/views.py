from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.shortcuts 

from lists.models import Item, List

# Create your views here.
def home_page( request ):

	return render( request, 'home.html' )
	
	
def view_list( request, list_id ):

	itemlist = List.objects.get( id=list_id)
	items = Item.objects.filter( list=itemlist )
	
	return render( request, 'list.html', {
		'items': items
	})

def new_list( request ):
	itemlist = List.objects.create()
	Item.objects.create( text=request.POST['item_text'] , list=itemlist)
	return redirect( '/lists/%d/' % (itemlist.id, ) )