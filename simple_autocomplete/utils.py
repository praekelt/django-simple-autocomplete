from django.db.models.fields import FieldDoesNotExist, CharField

def get_search_fieldname(model):
    # If model has field 'title' then use that, else use the first 
    # CharField on model.
    fieldname = ''
    try:
        model._meta.get_field_by_name('title')
        fieldname = 'title'
    except FieldDoesNotExist:
        for field in model._meta.fields:
            if isinstance(field, CharField):
                fieldname = field.name
                break                
    if not fieldname:
        raise RuntimeError, "Cannot determine fieldname"
    return fieldname
