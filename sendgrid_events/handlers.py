from .models import Event


class AbstractEventHandler(object):
    def process_events(self, data):
        raise NotImplementedError(
            'Event handler has to implement method `handle_event`'
        )


class DefaultEventHandler(AbstractEventHandler):
    def process_events(self, data):
        return Event.process_batch(data=data)
