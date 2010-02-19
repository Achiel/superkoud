from django.http import HttpResponse, Http404
from django.template.loader import get_template 
#from django.contrib.auth.forms import UserCreationForm
from forms import SKUserCreationForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from movietip_views import *
from moviewish_views import *
from movie_views import *

from movies.models import * 
from movies.forms import *
from django.contrib.auth.models import User 
from utils.shpaml_loader import load_template_source

def delete_moviewish(moviewish_id):
	try: 
		moviewish = Moviewish.objects.get(id=moviewish_id) 
	except: 
		raise Http404('Requested wish not found.')
	moviewish.delete()

def main_page(request): 
  template = load_template_source('main.html')
  variables = RequestContext(request, { 
    'head_title': 'Superkoud ', 
    'page_title': 'brrrr', 
    'page_body': 'Helping movie addicts, one tip at a time',
    'tipform' : MovietipSaveForm(), 
    'movietips' : Movietip.objects.all()[:10],
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
  followform = FollowForm(initial={'followusername':username})
  variables = RequestContext(request, { 
    'username': username, 
    'movietips': movietips,
    'followform' : followform 
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
	variables = RequestContext(request, {
		'users' : users
	})
	return HttpResponse(template.render(variables))

def register(request):
	if request.method == 'POST':
		form = SKUserCreationForm(request.POST)
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
		form = SKUserCreationForm()
		return render_to_response("registration/register.html", {
			'form': form,
			})

def render_error(error):
	template = get_template('error_page.html')
	variables = RequestContext(request, { 
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
	return HttpResponse(get_template('moviewishes_page.html').render(RequestContext(request, {
			'moviewishes' : moviewishes
		})))

def moviewish_view_page(request, moviewish_id):
	if request.method == 'GET':
		try: 
			moviewish = Moviewish.objects.get(id=moviewish_id) 
		except: 
			raise Http404('Requested wish not found.') 
		template = get_template('moviewish_page.html') 
		tipform = MoviewishSaveForm({'movie' : moviewish.movie})
		variables = RequestContext(request, { 	
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
	convert_form = MoviewishConvertForm(request.POST)
	if convert_form.is_valid():
		title = form.cleaned_data['movie']
		movietip, created = Movietip.objects.get_or_create(
			movie = convert_form.cleaned_data['movie']
		)
		print title
	return HttpResponseRedirect('/wish/')
				
# converts a wish to a tip
@login_required
def movietip_convert_page2(request, moviewish_id):
	if request.method == 'POST':
		convert_form = MoviewishConvertForm(request.POST)
		if convert_form.is_valid():
			title = form.cleaned_data['movie']
			movietip, created = Movietip.objects.get_or_create(
				movie = form.cleaned_data['movie']
			)
			movietip.save()
	return HttpResponseRedirect('/tip/')

@login_required
def follow_user(request):
	if request.method == 'POST':
		form = FollowForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['followusername']
			user = User.objects.get(username=username)
			myprofile = UserProfile.objects.get(user=request.user.id)
			myprofile.following.add(user)
			myprofile.save()	
		else:
			return render_error("Form not valid")
	return HttpResponseRedirect('/')

@login_required
def view_following(request):
	following = request.user.get_profile().following.all()
	print following
	print "foep"
	template = get_template('following_page.html')
	variables = RequestContext(request, {
		'users': following
	})

	output = template.render(variables)	
	return HttpResponse(output)
