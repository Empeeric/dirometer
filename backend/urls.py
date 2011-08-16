from django.conf.urls.defaults import *

urlpatterns = patterns('backend.views',
    url(r'^addReport', 'addReport', name='addReport'),
    url(r'^check', 'makeQuery', name='addReport'),
    url(r'^addmobile', 'update_mobile', name='update_mobile'),
    url(r'^sync', 'get_sync_data', name='sync'),
)
