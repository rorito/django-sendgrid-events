from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from sendgrid_events.models import Event, process_batch


@require_POST
@csrf_exempt
def handle_batch_post(request):
    background_process = False
    if hasattr(settings, 'SENDGRID_BACKGROUND_PROCESSING'):
        background_process = settings.SENDGRID_BACKGROUND_PROCESSING

    queue = None
    if hasattr(settings, 'SENDGRID_BACKGROUND_QUEUE'):
        queue = settings.SENDGRID_BACKGROUND_QUEUE

    if background_process:
        if queue:
            process_batch.apply_async(
                kwargs={'data': request.body},
                queue=queue
            )
        else:
            process_batch.apply_async(kwargs={'data': request.body})

    else:
        Event.process_batch(data=request.body)
    return HttpResponse()
