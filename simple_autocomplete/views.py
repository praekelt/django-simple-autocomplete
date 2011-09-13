import simplejson
import pickle

from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType

from simple_autocomplete.monkey import _simple_autocomplete_queryset_cache
from simple_autocomplete.utils import get_search_fieldname

def get_json(request, token):
    """Return matching results as JSON"""
    result = []
    searchtext = request.GET['q']
    if len(searchtext) >= 3:
        pickled =_simple_autocomplete_queryset_cache.get(token, None)
        if pickled is not None:
            ctid, query = pickle.loads(pickled)
            model = ContentType.objects.get(id=ctid).model_class()
            queryset = QuerySet(model=model, query=query)
            fieldname = get_search_fieldname(model)
            di = {'%s__istartswith' % fieldname:searchtext}
            items = queryset.filter(**di).order_by(fieldname)[:10]
            for item in items:
                result.append((item.id, getattr(item, fieldname)))
        else:
            result = 'CACHE_MISS'
        print result            
    return HttpResponse(simplejson.dumps(result))
