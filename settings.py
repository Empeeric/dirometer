# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import *

import os

# Activate django-dbindexer for the default database
DATABASES['native'] = DATABASES['default']
DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
AUTOLOAD_SITECONF = 'indexes'

SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

INSTALLED_APPS = (
#    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'djangotoolbox',
    'frontend',
    'backend',
    'autoload',
    'dbindexer',

    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
)

MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
    'autoload.middleware.AutoloadMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

ADMIN_MEDIA_PREFIX = '/media/admin/'
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

ROOT_URLCONF = 'urls'

GOOGLE_MAPS_API_KEY="ABQIAAAAnc7jlR_9nQgBjuMDVxFJUhQFwM1dKL5IwzzppoLBjK1Y6n9veBQltxojKtcjzAG1jdsp6kqw0B9GCQ"

WAZE_API="0687a712-ca4d-4116-953d-faf15bbd86e0"

GEOCODE_URL="http://geocoding.cloudmade.com/95739caddbc446dd933b9f391daf9842/geocoding/v2/find.js?query=street:%(street)s;city:%(city)s;house:%(house)s;country:israel"

CHECK_LIST=[
    ( 'Q1' , 'Is the place big?' , True ) ,
    ( 'Q2' , 'Does it have a roof?' , True) ,
    ( 'Q3' , 'Can you see the moon on a bright night?', True) ,
    ( 'Q4' ,  'How good is it?'  , False )
]

MAX_MARKERS=300
MAX_NEAR_ITEMS = 150