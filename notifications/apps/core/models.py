from django.db import models


class CoreModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class CoreSettings(CoreModel):
    trello_api_key = models.CharField("Trello API key", max_length=255, null=True, blank=True)
    trello_api_token = models.CharField("Trello API token", max_length=255, null=True, blank=True)
    trello_board_id = models.CharField("Trello board ID", max_length=255, null=True, blank=True)
    trello_list_id = models.CharField("Trello list ID", max_length=255, null=True, blank=True)

    slack_token = models.CharField("Slack token", max_length=255, null=True, blank=True)
    slack_channel_id = models.CharField("Slack channel", max_length=255, null=True, blank=True)

    def __str__(self):
        return "Core Settings"

    class Meta:
        app_label = "core"
        verbose_name = "Settings"
        verbose_name_plural = "Settings"
