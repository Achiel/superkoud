
def view_tip(request, tip):
	try: 
		movietip = Movietip.objects.get(id=movietipid) 
	except: 
		raise Http404('Requested tip not found.') 
	if request.is_ajax():
		template = get_template('render_tip.html')
	else:
		template = get_template('movietip_page.html') 
	wishform = MoviewishSaveForm({'movie' : movietip.movie})
	variables = RequestContext(request, { 	
		'movietip': movietip,
		'wishform': wishform,
	}) 

	output = template.render(variables) 
	return HttpResponse(output)
