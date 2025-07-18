from ckeditor.fields import RichTextField
from clients.models import Client
from core.models import CoreModel
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import TextField

from tickets.constants import TICKET_STATUS_CHOICES, TICKET_STATUS_OPEN

User = get_user_model()


class Ticket(CoreModel):
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL, related_name="tickets")

    draft = models.BooleanField(default=True)
    ticket_no = models.CharField("Ticket No.", max_length=45, null=False, blank=False, default="")
    title = models.CharField("Title", max_length=100, null=False, blank=False)
    description = RichTextField("Description", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="ticket_authors")
    assignee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="tickets_assignees"
    )
    module = models.CharField("Module", max_length=100, null=True, blank=True)
    status = models.CharField("Status", max_length=100, choices=TICKET_STATUS_CHOICES, default=TICKET_STATUS_OPEN)
    last_joblog_log = TextField("Last Job Log", null=True, blank=True)
    last_joblog_message = TextField("Last Job Log Message", null=True, blank=True)
    last_joblog_stacktrace = TextField("Last Job Log Stacktrace", null=True, blank=True)

    trello_ticket_created = models.BooleanField("Trello Ticket Created", default=False)
    trello_ticket_id = models.CharField("Trello Ticket ID", max_length=45, null=True, blank=True)
    trello_ticket_url = models.URLField("Trello Ticket URL", null=True, blank=True)
    slack_notification_sent = models.BooleanField("Slack Notification Sent", default=False)
    slack_message_ts = models.CharField("Slack Message TS", max_length=45, null=True, blank=True)
    slack_channel_id = models.CharField("Slack Channel ID", max_length=45, null=True, blank=True)

    class Meta:
        app_label = "tickets"
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Ticket No. {self.ticket_no}"

    def save(self, *args, **kwargs):
        """
        Override the ticket model's save method to handle Trello and Slack notifications based on the ticket state.

        Saves the model instance. Then sends a Trello ticket creation request if not already created,
        sends a Slack notification if not already sent, or updates the Slack message if it already exists.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        # todo: local imports - need to resolve circular import
        from tickets.slack import slack_create_ticket, slack_update_ticket
        from tickets.trello import trello_create_ticket

        # handle ticket notifications before saving the model instance
        if not self.draft and not self.trello_ticket_created:
            try:
                ticket_id, ticket_url = trello_create_ticket(ticket=self)
                self.trello_ticket_id = ticket_id
                self.trello_ticket_url = ticket_url
                self.trello_ticket_created = True
            except Exception as e:
                # todo: do something about failing tickets
                print(e)

        if not self.draft and not self.slack_notification_sent:
            try:
                message_ts, channel_id = slack_create_ticket(ticket=self)
                self.slack_message_ts = message_ts
                self.slack_channel_id = channel_id
                self.slack_notification_sent = True
            except Exception as e:
                # todo: do something about failing messages
                print(e)

        if self.slack_message_ts and self.slack_channel_id:
            slack_update_ticket(ticket=self)

        # save the ticket model instance
        super(Ticket, self).save(*args, **kwargs)
