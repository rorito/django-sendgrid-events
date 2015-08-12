======================
django-sendgrid-events
======================

.. image:: https://img.shields.io/travis/eldarion/django-sendgrid-events.svg
    :target: https://travis-ci.org/eldarion/django-sendgrid-events

.. image:: https://img.shields.io/coveralls/eldarion/django-sendgrid-events.svg
    :target: https://coveralls.io/r/eldarion/django-sendgrid-events

.. image:: https://img.shields.io/pypi/dm/django-sendgrid-events.svg
    :target:  https://pypi.python.org/pypi/django-sendgrid-events/

.. image:: https://img.shields.io/pypi/v/django-sendgrid-events.svg
    :target:  https://pypi.python.org/pypi/django-sendgrid-events/

.. image:: https://img.shields.io/badge/license-BSD-blue.svg
    :target:  https://pypi.python.org/pypi/django-sendgrid-events/


a simple app to provide and endpoind for and handle batch events from
SendGrid's Event API


Documentation
-------------

Documentation can be found online at http://django-sendgrid-events.rtfd.org.


How to Use with Celery
----------------------
1. In the root of your project, create a sendgrid_event_hooks.py file
https://gist.github.com/rorito/1f2add7742dcd3449021

2. In settings.py (or equivalent), add:
.. code-block:: python
    SENDGRID_EVENT_HANDLER = 'tribute.sendgrid_event_hooks.CustomEventHandler'

3. Wherever you have integrated django-sendgrid-events processing in your app (for example in your tasks.py), add the following:
.. code-block:: python
    from django.core.serializers import serialize
    from sendgrid_events.models import Event

    @shared_task
    def process_sendgrid_events(data):
        events = Event.process_batch(data=data)
        return json.loads(serialize('json', events))
        

Commercial Support
------------------

This app, and many others like it, have been built in support of many of Eldarion's
own sites, and sites of our clients. We would love to help you on your next project
so get in touch by dropping us a note at info@eldarion.com.
