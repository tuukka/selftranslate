
from django.conf.urls.defaults import *

urlpatterns = patterns('selftranslate.views',
    (r'^reload$', 'view_reload'),
    (r'^(?P<language>[^/]*)$', 'view_languages'),
    (r'^(?P<language>[^/]*)/$', 'view_editor'),
    (r'^(?P<language>[^/]*)/unit$', 'view_unit'),
    (r'^(?P<language>[^/]*)/catalog$', 'view_catalog'),
)
