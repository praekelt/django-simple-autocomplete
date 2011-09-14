from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.test.client import RequestFactory
from django.test import TestCase
from django.conf import settings

from simple_autocomplete.widgets import AutoCompleteWidget

class DummyModel(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
models.register_models('simple_autocomplete', DummyModel)

class EditDummyForm(forms.ModelForm):
    class Meta:
        model = DummyModel

class TestCase(TestCase):

    def setUp(self):
        self.adam = User.objects.create_user('adam', 'adam@foo.com', 'password')
        self.eve = User.objects.create_user('eve', 'eve@foo.com', 'password')
        self.dummy = DummyModel()
        self.dummy.save()
        self.request = RequestFactory()
    
    def test_monkey(self):
        # Are we using the autocomplete widget?
        form = EditDummyForm(self.request, instance=self.dummy)
        self.failUnless(isinstance(form.fields['user'].widget, AutoCompleteWidget))
