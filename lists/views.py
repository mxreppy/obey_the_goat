from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.shortcuts 

from lists.models import Item, List

# Create your views here.
def home_page( request ):

	return render( request, 'home.html' )
	
	
def view_list( request, list_id ):

	itemlist = List.objects.get( id=list_id )
	error = None
	
	if request.method == 'POST': 
		try: 
			Item.objects.create( text=request.POST['item_text'], list=itemlist )
			return redirect( itemlist )
		except ValidationError:
			error = "You can't have an empty list item" 

	return render( 
		request, 
		'list.html', 
		{ 'list': itemlist, 'error': error } 
	)

def new_list( request ):
	itemlist = List.objects.create()
	
	try: 
		Item.objects.create( text=request.POST['item_text'] , list=itemlist)
	except ValidationError:
		error_text = "You can't have an empty list item" 
		return render( request, 'home.html', {'error': error_text } )
		
	# bad -- url is hardcoded
# 	return redirect( '/lists/%d/' % (itemlist.id, ) )
	
	# better use view name
# 	return redirect( 'view_list', itemlist.id )
	# even better with the model defining get_absolute_url
	return redirect( itemlist )
	
# def add_item( request, list_id ) :
# 
# 	itemlist = List.objects.get( id=list_id )
# 	Item.objects.create( text=request.POST['item_text'], list=itemlist )
# 	
# 	return redirect( '/lists/%d/' % (itemlist.id,) )
# 	