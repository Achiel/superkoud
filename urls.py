from django.conf.urls.defaults import * 
from movies.views import * 
import os.path
static_media = os.path.join( 
  os.path.dirname(__file__), 'static_media' 
)

urlpatterns = patterns('', 
	(r'^$', main_page), 
	(r'^user/(\w+)/$', user_page), 
	(r'^login/$', 'django.contrib.auth.views.login'), 
	(r'^logout/$', 'django.contrib.auth.views.logout'),
	(r'^register/$', register),
	(r'^tip/create/$', movietip_save_page),
	(r'^tip/(\w)$', movietip_view_page),
	(r'^admin/', ('django.contrib.admin.urls')), 
	(r'^tip/view/(\w)$', movietip_view_page),
	(r'^converttowish/$', moviewish_save_page),
	(r'^wish/save/(\w)$', moviewish_save_page),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', 
	    { 'document_root': static_media }),
)