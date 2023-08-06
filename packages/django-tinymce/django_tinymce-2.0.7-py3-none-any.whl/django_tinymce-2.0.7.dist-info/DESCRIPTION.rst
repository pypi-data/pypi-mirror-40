django-tinymce
==============

**django-tinymce** is a Django application that contains a widget to render a form field as a TinyMCE editor.

Quickstart
==========

Install django-tinymce:

.. code-block::

    $ pip install django-tinymce

Add tinymce to INSTALLED_APPS in settings.py for your project:

.. code-block::

    INSTALLED_APPS = (
        ...
        'tinymce',
    )

Add tinymce.urls to urls.py for your project:

.. code-block::

    urlpatterns = patterns('',
        ...
        (r'^tinymce/', include('tinymce.urls')),
    )

In your code:

.. code-block::

    from django.db import models
    from tinymce.models import HTMLField

    class MyModel(models.Model):
        ...
        content = HTMLField()

**django-tinymce** uses staticfiles so everything should work as expected, different use cases (like using widget instead of HTMLField) and other stuff is available in documentation.

Documentation
=============

http://django-tinymce.readthedocs.org/

Support and updates
===================

You can contact me directly at aljosa.mohorovic@gmail.com, track
updates at https://twitter.com/maljosa or use github issues.  Be
persistent and bug me, I often find myself lost in time so ping me if
you're still waiting for me to answer.

License
=======

Originally written by Joost Cassee.

This program is licensed under the MIT License (see LICENSE.txt)


Changelog
#########

This document describes changes between each past release.

2.0.7 (2019-01-15)
==================

- Fix AppRegistryNotReady exception. (#132)


2.0.6 (2015-11-12)
==================

- Make sure jQuery is loaded both in the admin and for non-admin forms. (#141)


2.0.5 (2015-09-09)
==================

- Use static finders for development mode. (#131)


2.0.4 (2015-08-07)
==================

- Fix non-admin jQuery.


2.0.3 (2015-08-06)
==================

- Handle non-admin jQuery. (#108)


2.0.2 (2015-07-26)
==================

- Add Python3 support.


2.0.1 (2015-07-24)
==================

- Fix missing CHANGELOG.


2.0.0 (2015-07-23)
==================

* Starts supporting Django 1.8


