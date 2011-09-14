import pickle

from django.forms.widgets import Widget
from django.utils.safestring import mark_safe
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse

from simple_autocomplete.monkey import _simple_autocomplete_queryset_cache
from simple_autocomplete.utils import get_search_fieldname

class AutoCompleteWidget(Widget):
    input_type = 'autocomplete'
    url = None
    initial_display = None
    token = None
    model = None

    def __init__(self, url=None, initial_display=None, token=None, model=None, *args, **kwargs):
        """
        url: a custom URL that returns JSON with format [(value, label),(value,
        label),...].  

        initial_display: if url is provided then initial_display is the initial
        content of the autocomplete box, eg. "John Smith".

        token: an identifier to retrieve a cached queryset. Used internally.

        model: the model that the queryset objects are instances of. Used
        internally.
        """
        self.url = url
        self.initial_display = initial_display
        self.token = token
        self.model = model
        super(AutoCompleteWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
      
        display = ''
        if self.url:
            url = self.url
            display = self.initial_display

        else:
            fieldname = get_search_fieldname(self.model)
            url = reverse('simple-autocomplete', args=[self.token])
            if value:            
                dc, dc, query = pickle.loads(_simple_autocomplete_queryset_cache[self.token])
                queryset = QuerySet(model=self.model, query=query)
                display = getattr(queryset.get(pk=value), fieldname)

        html = """
    <script type="text/javascript">
    $(document).ready(function(){

    $("#id_%s_helper").autocomplete({
        source: function(request, response){
            $.ajax({
                url: "%s",
                data: {q: request.term},
                success: function(data) {
                    if (data != 'CACHE_MISS')                    
                        response($.map(data, function(item) {
                            return {
                                label: item[1],
                                value: item[1],
                                real_value: item[0]
                            };
                        }));
                },
                dataType: "json"
            });
        },
        select: function(event, ui) { $('#id_%s').val(ui.item.real_value); },
        minLength: 3
    });

    });
    </script>

<input id="id_%s_helper" type="text" value="%s" />
<input name="%s" id="id_%s" type="hidden" value="%s" />""" % (name, url, name, name, display, name, name, value)
        return mark_safe(html)

    def value_from_datadict(self, data, files, name):
        return data.get(name, None)
