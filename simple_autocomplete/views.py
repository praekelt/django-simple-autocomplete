from django.utils import simplejson
from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.db.models import get_model
from django.core.cache import cache

from simple_autocomplete.utils import get_search_fieldname


def get_json(request, token):
    """Return matching results as JSON"""
    result = []
    searchtext = request.GET['q']
    if len(searchtext) >= 3:
        tu = cache.get(token, None)
        if tu is not None:
            app_label, model_name, query = tu
            model = get_model(app_label, model_name)
            queryset = QuerySet(model=model, query=query)
            fieldname = get_search_fieldname(model)
            di = {'%s__istartswith' % fieldname: searchtext}
            items = queryset.filter(**di).order_by(fieldname)[:10]
            for item in items:
                result.append((item.id, str(item)))
        else:
            result = 'CACHE_MISS'
    return HttpResponse(simplejson.dumps(result))
