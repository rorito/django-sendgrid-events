from __future__ import absolute_import
import json

from django.core import serializers
from django.db import models
from django.utils import timezone

from jsonfield import JSONField
from celery import shared_task

from sendgrid_events.signals import batch_processed


class Event(models.Model):
    kind = models.CharField(max_length=75)
    email = models.CharField(max_length=150)
    data = JSONField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def process_batch(cls, data, json_compatible=False):
        events = []
        for event in json.loads(data):
            events.append(Event.objects.create(
                kind=event["event"],
                email=event["email"],
                data=event
            ))

        batch_processed.send(sender=Event, events=events)

        if json_compatible:
            return json.loads(serializers.serialize('json', events))

        return events


@shared_task
def process_batch(data, json_compatible=False):
    return Event.process_batch(data=data, json_compatible=json_compatible)
