from django.shortcuts import render
# from django.http import HttpResponse
# from django.shortcuts 

# Create your views here.
def home_page( request ):
	return render( request, 'home.html' )
# 	return HttpResponse( '<html><title>To-Do lists</title></html>')
	
# home_page = None
