from django.http import HttpResponse, Http404
from django.template import Context 
from django.template.loader import get_template 
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from movies.models import * 
from movies.forms import *

def main_page(request): 
  template = get_template('main_page.html') 
  variables = Context({ 
    'head_title': 'Django ', 
    'page_title': 'Welcome to Djangomarks', 
    'page_body': 'Where you can store and shaaAAAre marks!',
    'user': request.user,
  }) 
  output = template.render(variables) 
  return HttpResponse(output)

from django.contrib.auth.models import User 
def user_page(request, username): 
  try: 
    user = User.objects.get(username=username) 
  except: 
    raise Http404('Requested user not found.') 
  movietips = user.movietip_set.all() 
  auth = request.user.is_authenticated()
  template = get_template('user_page.html') 
  variables = Context({ 
    'username': username, 
    'movietips': movietips,
    'auth' : auth,
  }) 
  output = template.render(variables) 
  return HttpResponse(output)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {
        'form': form,
    })

def render_error(error):
	template = get_template('error_page.html')
	variables = Context({ 
	    'head_title': 'Superkoud ', 
	    'page_title': 'Error', 
	    'page_body': error,
	  }) 
	output = template.render(variables) 
	return HttpResponse(output)
	
def movietip_view_page(request, movietipid):
	try: 
		movietip = Movietip.objects.get(id=movietipid) 
	except: 
		raise Http404('Requested tip not found.') 
	# movietips = user.movietip_set.all() 
	template = get_template('movietip_page.html') 
	wishform = MoviewishSaveForm({'movie' : movietip.movie})
	username = request.user.username
	variables = Context({ 	
		'username': username, 
		'movietip': movietip,
		'wishform': wishform,
	}) 

	output = template.render(variables) 
	return HttpResponse(output)
	
def movietip_save_page(request):
	if request.method == 'GET': 
		form = MovietipSaveForm() 
		variables = RequestContext(request, { 
			'form': form 
		}) 
		return render_to_response('movietip_save.html', variables)
	else:
		form = MovietipSaveForm(request.POST) 
		if form.is_valid(): 
			movie, created = Movie.objects.get_or_create( 
				title = form.cleaned_data['movie']
			) 
			movietip, created2 = Movietip.objects.get_or_create(
				movie = movie,
				user = request.user,
			)
			movietip.description = form.cleaned_data['description'] 
			movietip.save() 
			return HttpResponseRedirect('/user/%s/' % request.user.username ) 
		else:
			render_error('Movie save page form not valid')

def moviewish_view_page(request, moviewish_id):
	try: 
		moviewish = Moviewish.objects.get(id=moviewish_id) 
	except: 
		raise Http404('Requested wish not found.') 

	template = get_template('moviewish_page.html') 
	username = request.user.username
	variables = Context({ 	
		'username': username, 
		'moviewish': moviewish,
		'movie' : moviewish.movie,
	}) 

	output = template.render(variables) 
	return HttpResponse(output)
	
def moviewish_save_page(request):
	if request.method == 'POST':
		form = MoviewishSaveForm(request.POST)
		if form.is_valid():
			movie, createdmovie = Movie.objects.get_or_create( 
				title = form.cleaned_data['movie']
			)
			moviewish, createdwish = Moviewish.objects.get_or_create(
				user = request.user,
				movie = movie
			)
			moviewish.save()
			return HttpResponseRedirect('/wish/%s/' % moviewish.id)
		else:
			render_error('Moviewish save page form not valid')
	else:
		render_error('Moviewish save page does not support \'GET\'')