from django.db.models.fields import FieldDoesNotExist, CharField
from django.conf import settings


def get_search_fieldname(model):
    # If model has 'search_field' settings use that. Otherwise, if
    # model has field 'title' then use that, else use the first
    # CharField on model.
    fieldname = get_setting("%s.%s" % (model._meta.app_label, model.__name__.lower()), \
        'search_field', '')
    if fieldname:
        try:
            # Django 1.11 deprecates get_field_by_name
            if hasattr(model._meta, 'get_field_by_name'):
                model._meta.get_field_by_name(fieldname)
            else:
                model._meta.get_field(fieldname)
        except FieldDoesNotExist:
            raise RuntimeError("Field '%s.%s' does not exist" % (model._meta.app_label, \
                model.__name__.lower()))
    else:
        try:
            # Django 1.11 deprecates get_field_by_name
            if hasattr(model._meta, 'get_field_by_name'):
                model._meta.get_field_by_name('title')
            else:
                model._meta.get_field('title')
            fieldname = 'title'
        except FieldDoesNotExist:
            for field in model._meta.fields:
                if isinstance(field, CharField):
                    fieldname = field.name
                    break
    if not fieldname:
        raise RuntimeError("Cannot determine fieldname")
    return fieldname


def get_threshold_for_model(model):
    key = '%s.%s' % (model._meta.app_label, model._meta.model_name)
    return getattr(settings, 'SIMPLE_AUTOCOMPLETE', {}).get(
        key, {}).get('threshold', None
    )


def get_setting(app_label_model, key, default):
    return getattr(settings, 'SIMPLE_AUTOCOMPLETE', {}).get(app_label_model, {}).get(key, default)
