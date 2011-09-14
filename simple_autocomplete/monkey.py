import pickle
import hashlib

from django.forms.models import ModelChoiceField
from django.conf import settings
from django.forms.fields import Field

_simple_autocomplete_queryset_cache = {}

from simple_autocomplete.widgets import AutoCompleteWidget

def ModelChoiceField__init__(self, queryset, empty_label=u"---------", cache_choices=False,
             required=True, widget=None, label=None, initial=None,
             help_text=None, to_field_name=None, *args, **kwargs):
    if required and (initial is not None):
        self.empty_label = None
    else:
        self.empty_label = empty_label
    self.cache_choices = cache_choices

    # Monkey starts here
    # Do not apply patch to subclasses like ModelMultipleChoiceField
    if self.__class__ ==  ModelChoiceField:
        key = '%s.%s' % (queryset.model._meta.app_label, queryset.model._meta.module_name)
        if key in getattr(settings, 'SIMPLE_AUTOCOMPLETE_MODELS', []):
            pickled = pickle.dumps((
                queryset.model._meta.app_label, 
                queryset.model._meta.module_name, 
                queryset.query
            ))
            token = hashlib.md5(pickled).hexdigest()
            _simple_autocomplete_queryset_cache[token] = pickled
            widget = AutoCompleteWidget(token=token, model=queryset.model)
    # Monkey ends here        

    # Call Field instead of ChoiceField __init__() because we don't need
    # ChoiceField.__init__().
    Field.__init__(self, required, widget, label, initial, help_text,
                   *args, **kwargs)

    self.queryset = queryset
    self.choice_cache = None
    self.to_field_name = to_field_name

ModelChoiceField.__init__ = ModelChoiceField__init__
