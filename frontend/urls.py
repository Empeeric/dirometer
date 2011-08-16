from django.conf.urls.defaults import *

urlpatterns = patterns('frontend.views',
    url(r'^widget', 'widget', name='widget'),
    url(r'^$', 'home', name='home'),
)
