import pickle

from django.forms.widgets import Select, SelectMultiple
from django.utils.safestring import mark_safe
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse
from django.conf import settings

from simple_autocomplete.monkey import _simple_autocomplete_queryset_cache
from simple_autocomplete.utils import get_search_fieldname, \
    get_threshold_for_model


class AutoCompleteWidget(Select):
    input_type = 'autocomplete'
    url = None
    initial_display = None
    token = None
    model = None

    def __init__(self, url=None, initial_display=None, token=None,
        model=None, *args, **kwargs):
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
            dc, dc, query = pickle.loads(
                _simple_autocomplete_queryset_cache[self.token]
            )
            queryset = QuerySet(model=self.model, query=query)
            threshold = get_threshold_for_model(self.model)
            if threshold and (queryset.count() < threshold):
                # Render the normal select widget if size below threshold
                return super(AutoCompleteWidget, self).render(
                    name, value, attrs
                )
            else:
                url = reverse('simple_autocomplete:simple-autocomplete', args=[self.token])
                if value:
                    display = unicode(queryset.get(pk=value))

        html = u"""
    <script type="text/javascript">
    (function($) {

    $(document).ready(function() {

    $("#id_%(name)s_helper").autocomplete({
        source: function(request, response){
            $.ajax({
                url: "%(url)s",
                data: {q: request.term},
                success: function(data) {
                    if (data != 'CACHE_MISS')
                    {
                        response($.map(data, function(item) {
                            return {
                                label: item[1],
                                value: item[1],
                                real_value: item[0]
                            };
                        }));
                    }
                },
                dataType: "json"
            });
        },
        select: function(event, ui) { $('#id_%(name)s').val(ui.item.real_value); },
        minLength: 3
    });

    });

    })(django.jQuery);
    </script>

<input id="id_%(name)s_helper" type="text" value="%(display)s" />
<a href="#" title="Clear" onclick="django.jQuery('#id_%(name)s_helper').val(''); django.jQuery('#id_%(name)s_helper').focus(); django.jQuery('#id_%(name)s').val(''); return false;">x<small></small></a>
<input name="%(name)s" id="id_%(name)s" type="hidden" value="%(value)s" />""" % dict(name=name, url=url, display=display, value=value)
        return mark_safe(html)


class AutoCompleteMultipleWidget(SelectMultiple):
    input_type = 'autocomplete_multiple'
    url = None
    initial_display = None
    token = None
    model = None

    def __init__(self, url=None, initial_display=None, token=None,
        model=None, *args, **kwargs):
        """
        url: a custom URL that returns JSON with format [(value, label),(value,
        label),...].

        initial_display: if url is provided then initial_display is a
        dictionary containing the initial content of the autocomplete box, eg.
        {1:"John Smith", 2:"Sarah Connor"}. The key is the primary key of the
        referenced item.

        token: an identifier to retrieve a cached queryset. Used internally.

        model: the model that the queryset objects are instances of. Used
        internally.
        """
        self.url = url
        self.initial_display = initial_display
        self.token = token
        self.model = model
        super(AutoCompleteMultipleWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = []

        display = ''
        if self.url:
            url = self.url
            # todo: Display is not so simple in this case. Needs a lot of work.
            # Will probably have to be a dictionary.
            display = self.initial_display
        else:
            dc, dc, query = pickle.loads(
                _simple_autocomplete_queryset_cache[self.token]
            )
            queryset = QuerySet(model=self.model, query=query)
            threshold = get_threshold_for_model(self.model)
            if threshold and (queryset.count() < threshold):
                # Render the normal select widget if size below threshold
                return super(AutoCompleteMultipleWidget, self).render(
                    name, value, attrs
                )
            else:
                url = reverse('simple_autocomplete:simple-autocomplete', args=[self.token])

            html = u"""
    <script type="text/javascript">
    (function($) {

    $(document).ready(function() {

    $("#id_%s_helper").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "%s",
                data: {q: request.term},
                success: function(data) {
                    if (data != 'CACHE_MISS')
                    {
                        response($.map(data, function(item) {
                            return {
                                label: item[1],
                                value: item[1],
                                real_value: item[0]
                            };
                        }));
                    }
                },
                dataType: "json"
            });
        },
        select: function(event, ui) {
            var name = '%s';
            var parent = $('#id_' + name).parent();
            var target = $('div.autocomplete-placeholder', parent);
            target.append('<p><input name="' + name + '" value="' + ui.item.real_value + '" '
                + 'type="hidden" />' + ui.item.value
                + ' <a href="#" title="Remove" onclick="django.jQuery(this).parent().remove(); django.jQuery('+"'"+'#id_%s_helper'+"'"+').val(' + "''" + '); django.jQuery('+"'"+'#id_%s_helper'+"'"+').focus(); return false;">x<small></small></a></p>');
        },
        close: function(event, ui) {
            django.jQuery('#id_%s_helper').val('');
        },
        minLength: 3
    });

    });

    })(django.jQuery);
    </script>

<input id="id_%s_helper" type="text" value="" />
<input id="id_%s" type="hidden" value="" />
<div class="autocomplete-placeholder">""" % (name, url, name, name, name, name, name, name)

            # Create html for existing values
            for v in value:
                if v is None: continue
                display = unicode(queryset.get(pk=v))
                html += """<p><input name="%s" type="hidden" value="%s" />
%s <a href="#" title="Remove" onclick="django.jQuery(this).parent().remove(); django.jQuery('#id_%s_helper').val(''); django.jQuery('#id_%s_helper').focus(); return false;">x<small></small></a></p>""" % (name, v, display, name, name)

            html += "</div>"

            # Help with green plus icon alignment
            # todo: use css class
            html += """<div style="display: inline-block; width: 104px;">&nbsp;</div>"""

            return mark_safe(html)
