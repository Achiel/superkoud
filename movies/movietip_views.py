from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from movies.forms import *
from movies.views import *
from django.shortcuts import render_to_response
from django.template.loader import get_template 
from django.http import HttpResponse, Http404
from movies.models import * 
from django.http import HttpResponseRedirect
from django.forms import ModelForm

@login_required
def delete_movietip(movietip_id):
	try: 
		movietip = Movietip.objects.get(id=movietip_id) 
	except: 
		raise Http404('Requested tip not found.')
	movietip.delete()
	
def movietip_view_page(request, movietipid):
	try: 
		movietip = Movietip.objects.get(id=movietipid) 
	except: 
		raise Http404('Requested tip not found.') 
	if request.is_ajax():
		template = get_template('render_tip.html')
	else:
		template = get_template('movietip_page.html') 
	wishform = MoviewishSaveForm({'movie' : movietip.movie})
	variables = RequestContextContext(request, { 	
		'movietip': movietip,
		'wishform': wishform,
	}) 

	output = template.render(variables) 
	return HttpResponse(output)

@login_required
def movietip_save_page(request):
	if request.method == 'GET': 
		movietipform = MovietipSaveForm() 
		moviewishform = MoviewishSaveForm()
		variables = RequestContext(request, { 
			'movietipform': movietipform, 
			'moviewishform' : moviewishform, 
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
			return HttpResponseRedirect('/user/%s' % request.user.username ) 
		else:
			render_error('Movie save page form not valid')

def movietips_page(request):
	if request.user is not None:
		movietips = Movietip.objects.exclude(user=request.user.id)
	else:
		movietips = Movietip.objects.all()[:10]
	template = get_template('movietips_page.html')
	variables = RequestContext(request, {
		'movietips' : movietips
	})
	return HttpResponse(template.render(variables))

@login_required
def movietips_my_page(request):
	movietips = Movietip.objects.filter(user=request.user.id)
	template = get_template('movietips_page.html')
	return HttpResponse(template.render(RequestContext(request, {
			'movietips' : movietips
		})))
