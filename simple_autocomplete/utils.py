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
            model._meta.get_field_by_name(fieldname)
        except FieldDoesNotExist:
            raise RuntimeError("Field '%s.%s' does not exist" % (model._meta.app_label, \
                model.__name__.lower()))
    else:
        try:
            model._meta.get_field_by_name('title')
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
    key = '%s.%s' % (model._meta.app_label, model._meta.module_name)
    return getattr(settings, 'SIMPLE_AUTOCOMPLETE', {}).get(
        key, {}).get('threshold', None
    )


def get_setting(app_label_model, key, default):
    return getattr(settings, 'SIMPLE_AUTOCOMPLETE', {}).get(app_label_model, {}).get(key, default)
