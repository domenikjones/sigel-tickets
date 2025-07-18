from core.admin import CoreAdmin
from django.contrib import admin

from tickets.models import Ticket


@admin.register(Ticket)
class TicketAdmin(CoreAdmin):
    list_display = ("id", "ticket_no", "status", "client", "title")
    search_fields = ("ticket_no", "title", "description")
    list_filter = ("status",)
    date_hierarchy = "created_at"
    readonly_fields = (
        "ticket_no",
        "created_at",
        "updated_at",
        "trello_ticket_id",
        "trello_ticket_url",
        "slack_message_ts",
        "slack_channel_id",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    (
                        "draft",
                        "ticket_no",
                        "status",
                        "client",
                        ("created_at", "updated_at"),
                    )
                ),
            },
        ),
        ("Ticket", {"fields": ("module", "title", "description")}),
        (
            "Notifications",
            {
                "fields": (
                    ("trello_ticket_created", "trello_ticket_id", "trello_ticket_url"),
                    ("slack_notification_sent", "slack_message_ts"),
                )
            },
        ),
    )
