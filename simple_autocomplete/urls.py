from django.conf.urls import url

from simple_autocomplete.views import get_json


urlpatterns = [
    url(r'^(?P<token>[\w-]+)/$', get_json, name='simple-autocomplete')
]
