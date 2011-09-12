Django Simple Autocomplete
==========================
**App enabling the use of jQuery UI autocomplete widget for ModelChoiceFields with minimal configuration required.**

.. contents:: Contents
    :depth: 5

Installation
------------

#. Install or add ``django-simple-autocomplete`` to your Python path.

#. Add ``simple_autocomplete`` to your ``INSTALLED_APPS`` setting.

#. Add (r'^simple-autocomplete/', include('simple_autocomplete.urls')) to urlpatterns.

#. Ensure jQuery core, jQuery UI Javascript and jQuery UI CSS is loaded by your templates.

Usage
-----

Django by default renders a select widget (a.k.a. combobox or dropdown) for
foreign key fields. You can change the widget to an autocomplete widget by
adding the model to the SIMPLE_AUTOCOMPLETE_MODELS tuple in your settings file.
For instance, to use the autocomplete widget when selecting a user do::
    
    SIMPLE_AUTOCOMPLETE_MODELS = ('auth.user',)

The product attempts to use a field ``title`` for filtering and display in
the list. If the model has no field ``title`` then the first CharField is
used. Eg. for the user model the field ``username`` is used.

The widget can be used implicitly in a form. The declaration of
``ModelChoiceField`` is all that is required::

    class MyForm(forms.Form):
        user = forms.ModelChoiceField(queryset=User.objects.all(), initial=3)

The widget can be used explicitly in a form. In such a case you must provide an 
URL which returns results as JSON with format [(value, label), (value, label),...]. 
The ``initial`` and ``initial_display`` parameters are only required if there is 
a starting value::

    from simple_autocomplete.widgets import AutoCompleteWidget

    class MyForm(forms.Form):
        user = forms.ModelChoiceField(
            queryset=User.objects.all(),         
            initial=3,
            widget=AutoCompleteWidget(
                url='/custom-json-query', 
                initial_display='John Smith'
            )
        )

The ability to specify an URL for the widget enables you to hook up to other 
more advanced autocomplete query engines if you wish.

