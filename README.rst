Django Rrweb
============

`Django Rrweb <http://www.grantjenks.com/docs/django-rrweb/>`__ is an Apache2
licensed Django application that records and replays sessions in web browsers.


Features
--------

- Record sessions in web browsers
- Replay sessions in web browsers
- Tested on Python 3.7, 3.8, 3.9, 3.10
- Tested on Django 3.2 LTS and Django 4.0

.. image:: https://github.com/grantjenks/django-rrweb/workflows/integration/badge.svg
   :target: https://github.com/grantjenks/django-rrweb/actions?query=workflow%3Aintegration

.. image:: https://github.com/grantjenks/django-rrweb/workflows/release/badge.svg
   :target: https://github.com/grantjenks/django-rrweb/actions?query=workflow%3Arelease


Quickstart
----------

Installing Django Rrweb is simple with `pip
<http://www.pip-installer.org/>`_::

    $ pip install django-rrweb

Changes to `settings.py` like:

.. code::

   INSTALLED_APPS += ['django.contrib.humanize', 'django_rrweb']

And

.. code::

   MIDDLEWARE += ['django_rrweb.middleware.session_key_middleware']

Changes to `urls.py` like:

.. code::

   urlpatterns += [path('rrweb/', include('django_rrweb.urls'))]

The Django "admin" is also required for replaying and deleting sessions.

Then migrate the database like:

.. code::

   $ python manage.py migrate


Reference and Indices
---------------------

* `Django Rrweb Documentation`_
* `Django Rrweb at PyPI`_
* `Django Rrweb at GitHub`_
* `Django Rrweb Issue Tracker`_

.. _`Django Rrweb Documentation`: http://www.grantjenks.com/docs/django-rrweb/
.. _`Django Rrweb at PyPI`: https://pypi.python.org/pypi/django-rrweb/
.. _`Django Rrweb at GitHub`: https://github.com/grantjenks/django-rrweb
.. _`Django Rrweb Issue Tracker`: https://github.com/grantjenks/django-rrweb/issues


Django Rrweb License
--------------------

Copyright 2022 Grant Jenks

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
