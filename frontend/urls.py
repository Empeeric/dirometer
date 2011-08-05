from django.conf.urls.defaults import *

urlpatterns = patterns('frontend.views',
    url(r'^$', 'home', name='home'),
         url(r'^all', 'showAll', name='showAll'),
)
