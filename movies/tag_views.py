from models import Tag
from general import *
from django.template.loader import get_template 
from django.template import Context 
from django.http import HttpResponse, Http404

def view_tag_page(request, tag_name):
	try: 
		tag = Tag.objects.get(name=tag_name) 
	except: 
		raise Http404('Requested tag not found.') 
	if request.is_ajax():
		template = get_template('render_tag.html')
	else:
		template = get_template('tag_page.html') 
	username = get_username(request)

	variables = Context({ 	
		'username': username, 
		'movietips': tag.movietips,
		'tag' : tag,
	}) 

	output = template.render(variables) 
	return HttpResponse(output)
