from django.conf.urls.defaults import *
from django.http import HttpResponse

handler500 = 'djangotoolbox.errorviews.server_error'

sitemaps = {
}

urlpatterns = patterns('',
    (r'^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^admin$', 'django.views.generic.simple.redirect_to', {'url': 'admin/'}),
    (r'^admin/', include('urlsadmin')),
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /api/*", mimetype="text/plain")),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/img/favicon.ico'}),
    (r'^api/', include('backend.urls')),
    (r'', include('frontend.urls')),
)
