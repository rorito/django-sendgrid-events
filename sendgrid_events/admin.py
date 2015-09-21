from django.contrib import admin
from django.utils.html import format_html
from post_office.models import Email

from .models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ["kind", "email", "created_at", "post_office_email"]
    list_filter = ["created_at", "kind"]
    search_fields = ["email", "data"]

    def post_office_email(self, obj):
        try:
            # Search the email_uuid field from event
            email_uuid = obj.data["email_uuid"]
            # Search the Emails with that uuid
            pks = Email.objects.filter(headers__contains=email_uuid).values_list("pk", flat=True)
        except KeyError as err:
            # The event does not have an email_uuid field
            pks = []

        value = ""
        if len(pks) > 0:
            for pk in pks:
                value += format_html('<strong><a href="/admin/post_office/email/{0}/">{0}</a></strong> ', pk)
        else:
            value = "Email object related by email_uuid not found"
        return value

    post_office_email.allow_tags = True


admin.site.register(Event, EventAdmin)
