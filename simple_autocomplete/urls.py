from django.conf.urls import patterns, url

urlpatterns = patterns(
    'simple_autocomplete.views',
    url(r'^(?P<token>[\w-]+)/$', 'get_json', name='simple-autocomplete'),
)
