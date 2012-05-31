import simplejson
import hashlib

from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.test import TestCase
from django.conf import settings
from django.test.client import Client as BaseClient, FakePayload, \
    RequestFactory
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import reverse
from django.core.cache import cache

from simple_autocomplete.widgets import AutoCompleteWidget


class DummyModel(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
models.register_models('simple_autocomplete', DummyModel)


class EditDummyForm(forms.ModelForm):
    class Meta:
        model = DummyModel


class Client(BaseClient):
    """Bug in django/test/client.py omits wsgi.input"""

    def _base_environ(self, **request):
        result = super(Client, self)._base_environ(**request)
        result['HTTP_USER_AGENT'] = 'Django Unittest'
        result['HTTP_REFERER'] = 'dummy'
        result['wsgi.input'] = FakePayload('')
        return result


class TestCase(TestCase):

    def setUp(self):
        self.adam = User.objects.create_user(
            'adam', 'adam@foo.com', 'password'
        )
        self.eve = User.objects.create_user('eve', 'eve@foo.com', 'password')
        self.dummy = DummyModel()
        self.dummy.save()
        self.request = RequestFactory()
        self.client = Client()

    def test_monkey(self):
        # Are we using the autocomplete widget?
        form = EditDummyForm(self.request, instance=self.dummy)
        self.failUnless(
            isinstance(form.fields['user'].widget, AutoCompleteWidget)
        )

    def test_json(self):
        # Find our token in cache. Need to drop to low level API. Can't rely
        # on items() since values are encoded.
        for key in cache._cache.keys():
            # Use low level API knowledge to get token
            token = key[3:]
            tu = cache.get(token, (None, None, None))
            app_label, model_name, dc = tu
            if (app_label == 'auth') and (model_name == 'user'):
                break

        url = reverse('simple-autocomplete', args=[token])
        response = self.client.get(url, {'q': 'ada'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, """[[1, "adam"]]""")
