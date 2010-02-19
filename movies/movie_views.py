from models import Movie
from django.template.loader import get_template 
from django.http import HttpResponse, Http404

def movie_view_page(request, movie_id):
	try: 
		movie = Movie.objects.get(id=movie_id) 
	except: 
		raise Http404('Requested movie not found.') 
	if request.is_ajax():
		template = get_template('render_movie.html')
	else:
		template = get_template('movie_page.html') 

	variables = RequestContext(request, { 	
		'movie' : movie,
	}) 

	output = template.render(variables) 
	return HttpResponse(output)
