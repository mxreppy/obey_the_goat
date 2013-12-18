from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.shortcuts 

from lists.forms import ItemForm
from lists.models import Item, List

# Create your views here.
def home_page( request ):

	return render( 
		request, 
		'home.html', 
		{'form': ItemForm() } 
	)
	
	
def view_list( request, list_id ):

	itemlist = List.objects.get( id=list_id )
	form = ItemForm()

	if request.method == 'POST': 
		form = ItemForm( data=request.POST ) 
		if form.is_valid(): 			
			Item.objects.create( text=request.POST['text'], list=itemlist )
			return redirect( itemlist )
	
	return render( request, 'list.html', 
		{ 'list': itemlist, 'form': form } 
	)


def new_list( request ):
	form = ItemForm( data=request.POST )
	if( form.is_valid()): 
		itemlist = List.objects.create()
		Item.objects.create( text=request.POST['text'] , list=itemlist)
		# even better with the model defining get_absolute_url
		return redirect( itemlist )
	else:
		return render( request, 'home.html', {"form": form } )
	
