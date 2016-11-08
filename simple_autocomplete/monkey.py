import pickle
import hashlib

from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.conf import settings
from django.forms.fields import Field

_simple_autocomplete_queryset_cache = {}

from simple_autocomplete.widgets import AutoCompleteWidget, \
    AutoCompleteMultipleWidget


def ModelChoiceField__init__(self, queryset, empty_label="---------",
        required=True, widget=None, label=None, initial=None,
        help_text='', to_field_name=None, limit_choices_to=None,
        *args, **kwargs
    ):

    if required and (initial is not None):
        self.empty_label = None
    else:
        self.empty_label = empty_label

    # Monkey starts here
    if (widget is None) and self.__class__ in (ModelChoiceField, ModelMultipleChoiceField):
        meta = queryset.model._meta
        key = '%s.%s' % (meta.app_label, meta.model_name)
        # Handle both legacy settings SIMPLE_AUTOCOMPLETE_MODELS and new
        # setting SIMPLE_AUTOCOMPLETE.
        models = getattr(
            settings, 'SIMPLE_AUTOCOMPLETE_MODELS',
            getattr(settings, 'SIMPLE_AUTOCOMPLETE', {}).keys()
        )
        if key in models:
            pickled = pickle.dumps((
                queryset.model._meta.app_label,
                queryset.model._meta.model_name,
                queryset.query
            ))
            token = hashlib.md5(pickled).hexdigest()
            _simple_autocomplete_queryset_cache[token] = pickled
            if self.__class__ == ModelChoiceField:
                widget = AutoCompleteWidget(token=token, model=queryset.model)
            else:
                widget = AutoCompleteMultipleWidget(
                    token=token, model=queryset.model
                )
    # Monkey ends here

    # Call Field instead of ChoiceField __init__() because we don't need
    # ChoiceField.__init__().
    Field.__init__(self, required, widget, label, initial, help_text,
        *args, **kwargs)
    self.queryset = queryset
    self.limit_choices_to = limit_choices_to   # limit the queryset later.
    self.to_field_name = to_field_name

ModelChoiceField.__init__ = ModelChoiceField__init__


# Preserve sort order of multiple choice values
def clean_decorator(func):
    def new(self, value):
        qs = func(self, value)
        li = [o for o in qs]
        li.sort(
            lambda a, b: cmp(value.index(str(a.pk)), value.index(str(b.pk)))
        )
        return li
    return new

ModelMultipleChoiceField.clean = clean_decorator(ModelMultipleChoiceField.clean)
