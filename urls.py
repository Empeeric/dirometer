from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

sitemaps = {
}

urlpatterns = patterns('',
    (r'^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^admin$', 'django.views.generic.simple.redirect_to', {'url': 'admin/'}),
    (r'^admin/', include('urlsadmin')),
    (r'^api/', include('backend.urls')),
    (r'', include('frontend.urls')),
)
