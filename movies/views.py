from django.http import HttpResponse, Http404
from django.template import Context 
from django.template.loader import get_template 
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from general import *
from movietip_views import *
from tag_views import *
from moviewish_views import *
from movie_views import *
from tag_views import *

from movies.models import * 
from movies.forms import *
from django.contrib.auth.models import User 

def delete_moviewish(moviewish_id):
	try: 
		moviewish = Moviewish.objects.get(id=moviewish_id) 
	except: 
		raise Http404('Requested wish not found.')
	moviewish.delete()

def main_page(request): 
  template = get_template('main_page.html') 
  variables = Context({ 
    'head_title': 'Superkoud ', 
    'page_title': 'brrrr', 
    'page_body': 'Helping movie addicts, one tip at a time',
    'username': get_username(request),
  }) 
  output = template.render(variables) 
  return HttpResponse(output)


def user_page(request, username): 
  try: 
    user = User.objects.get(username=username) 
  except: 
    raise Http404('Requested user not found.') 
  movietips = user.movietip_set.all() 
  template = get_template('user_page.html') 
  variables = Context({ 
    'username': username, 
    'movietips': movietips,
  }) 
  output = template.render(variables) 
  return HttpResponse(output)

@login_required
def edit_profile(req):
	user = request.user
	if request.method == 'POST':
		form = ProfileEditForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/")
	else:
		form = ProfileEditForm()
		return render_to_response("user/profile.html", {
				'form' : form,
			})

def users_page(request):
	users = User.objects.all()
	template = get_template('users_page.html')
	variables = Context({
		'username' : get_username(request),
		'users' : users
	})
	return HttpResponse(template.render(variables))

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			request.session['username'] = new_user.username
			return HttpResponseRedirect("/")
		else:
			return render_to_response("registration/register.html", {
					'form': form,
					'message' : "form isn't valid",
				})
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

@login_required
def moviewishes_page(request):
	moviewishes = Moviewish.objects.filter(user=request.user.id)
	for wish in moviewishes:
		wish.form = MoviewishConvertForm({'movie' : wish.movie})
	return HttpResponse(get_template('moviewishes_page.html').render(Context({
			'username' : get_username(request),
			'moviewishes' : moviewishes
		})))

def moviewish_view_page(request, moviewish_id):
	if request.method == 'GET':
		try: 
			moviewish = Moviewish.objects.get(id=moviewish_id) 
		except: 
			raise Http404('Requested wish not found.') 
		template = get_template('moviewish_page.html') 
		username = get_username(request)
		tipform = MoviewishSaveForm({'movie' : moviewish.movie})
		variables = Context({ 	
			'username': username, 
			'moviewish': moviewish,
			'movie' : moviewish.movie,
		}) 

		output = template.render(variables) 
		return HttpResponse(output)
	elif request.method == 'DELETE':
		render_error('DELETE FOUND')
	else: #POST, handle as delete
		return "flapflap"
		# delete_moviewish(moviewish_id)
		return HttpResponseRedirect('/wish/')
		
@login_required
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
			return HttpResponseRedirect('/wish/%s' % moviewish.id)
		else:
			return render_error('Moviewish save page form not valid')
	else:
		return render_error('Moviewish save page does not support \'GET\'')
		
@login_required
def moviewish_convert_page(request):
	if request.method == 'POST':
		form = MoviewishConvertForm(request.POST)
		if form.is_valid():
			movie, createdmovie = Movie.objects.get_or_create( 
				title = form.cleaned_data['movie']
			)
			moviewish, createdwish = Moviewish.objects.get_or_create(
				user = request.user,
				movie = movie
			)
			moviewish.save()
			return HttpResponseRedirect('/wish/')
		else:
			return render_error('Moviewish save page form not valid')
	else:
		return render_error('Moviewish save page does not support \'GET\'')

# converts a wish to a tip
@login_required
def movietip_convert_page(request):
	convert_form = MoviewishConvertForum(request)
	if convert_form.is_valid():
		title = form.cleaned_data['movie']
		movietip, created = Movietip.objects.get_or_create(
			movie = form.cleaned_data['movie']
		)
	print title
				
# converts a wish to a tip
@login_required
def movietip_convert_page(request, moviewish_id):
	if request.method == 'POST':
		# try:
		# 			moviewish = Moviewish.objects.get(id=moviewish_id, user=request.user)
		# 		except:
		# 			raise Http404('Wish not found')
		convert_form = MoviewishConvertForm(request)
		if convert_form.is_valid():
			title = form.cleaned_data['movie']
			movietip, created = Movietip.objects.get_or_create(
				movie = form.cleaned_data['movie']
			)
			movietip.save()
	return HttpResponseRedirect('/tip/')
