Changelog
=========

0.3.3
-----
#. Tests failing for Django 1.5. Pin to 1.4.x until that is fixed.
#. Handle case where an item that is referenced by a multiselect has been deleted from the database.

0.3.2
-----
#. Allow `search_field` to be specified per model, in case the defaults don't suffice.

0.3.1
-----
#. Fix unicode bug.

0.3
---
#. `max_items` setting specifies maximum number of items to display in autocomplete dropdown.
#. `duplicate_format_function` setting allows appending of a custom string if more than one item in the autocomplete dropdown has the same string value. 

0.2
---
#. Clear autoselect helper in some cases for cleaner UI.
#. Use object string representation for display and not lookup fieldname.

0.1
---
#. Add autocomplete widget for multiple selections
#. Threshold setting to determine when to show autocomplete widget instead of normal widget

0.0.1
-----
#. Initial release.

