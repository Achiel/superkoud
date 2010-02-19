from django.conf.urls.defaults import * 
from movies.views import * 
from movies.movietip_views import *
import os.path
static_media = os.path.join( 
  os.path.dirname(__file__), 'static_media' 
)


urlpatterns = patterns('', 
	(r'^$', main_page), 
	(r'^admin/', ('django.contrib.admin.urls')), 
	
	(r'^user/(\w+)$', user_page), 
	(r'^user/$', users_page),
	
	(r'^login/$', 'django.contrib.auth.views.login'), 
	(r'^logout/$', 'django.contrib.auth.views.logout'),
	(r'^register/$', register),

	(r'^follow/$', follow_user),
	(r'^following/$', view_following),

	(r'^movie/(\w+)$', movie_view_page),
	
	(r'^tip/$', movietips_page),
	(r'^savetip/$', movietip_save_page),
	(r'^tip/(\w+)/$', movietip_view_page),
	(r'^tip/view/(\w+)$', movietip_view_page),
	
	(r'^mytips/$', movietips_my_page),
	(r'^converttotip/$', movietip_convert_page),
	#(r'^converttotip/(\w+)$', movietip_convert_page),

	
	(r'^wish/$', moviewishes_page),
	(r'^wish/save/(\w+)$', moviewish_convert_page),
	(r'^wish/(\w+)$', moviewish_view_page),
	(r'^savewish/$', moviewish_save_page),
	
	(r'^converttowish/$', moviewish_save_page),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', 
	    { 'document_root': static_media }),
	
)
