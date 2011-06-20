from django.conf.urls.defaults import *
import os.path
from dungeon.views import *
from django.views.generic.simple import direct_to_template

site_media = os.path.join(
    os.path.dirname(__file__), 'site_media'
)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    
    (r'^$', main_page),
    
    # session management
    (r'^login/$', 'django.contrib.auth.views.login'), 
    (r'^logout/$', logout_page),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        { 'document_root': site_media }),
    (r'^register/$', register_page),
    (r'^register/success/$', direct_to_template,
        { 'template': 'registration/register_success.html' }),
        
    # player management
    (r'^players/create/$', create_player),
    (r'^players/(\w+)/(\w+)/$', player),
    (r'^play/(\w+)/(\w+)/$', play),
    
    # Example:
    # (r'^helvetica/', include('helvetica.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
