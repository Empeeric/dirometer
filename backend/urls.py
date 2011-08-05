from django.conf.urls.defaults import *

urlpatterns = patterns('backend.views',
    url(r'^addReport', 'addReport', name='addReport'),
     url(r'^check', 'makeQuery', name='addReport'),
)
