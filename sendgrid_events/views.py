from django.conf import settings
from django.http import HttpResponse
from django.utils.module_loading import import_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .handlers import AbstractEventHandler, DefaultEventHandler


@require_POST
@csrf_exempt
def handle_batch_post(request):
    background_process = False

    EventHandler = DefaultEventHandler
    if hasattr(settings, 'SENDGRID_EVENT_HANDLER'):
        CustomHandler = import_string(settings.SENDGRID_EVENT_HANDLER)

        if issubclass(CustomHandler, AbstractEventHandler):
            EventHandler = CustomHandler

    handler = EventHandler()
    handler.process_events(request.body)

    return HttpResponse()
