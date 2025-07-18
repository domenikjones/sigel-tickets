from core.admin import CoreAdmin
from django.contrib import admin

from tickets.models import Ticket, TrelloLabel


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
        (
            "Ticket",
            {
                "fields": (
                    "module",
                    "title",
                    "description",
                    "last_joblog_log",
                    "last_joblog_message",
                    "last_joblog_stacktrace",
                )
            },
        ),
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


@admin.register(TrelloLabel)
class TrelloLabelAdmin(CoreAdmin):
    list_display = ("module", "trello_label_id", "trello_label_name", "trello_label_color")
