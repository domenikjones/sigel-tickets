from typing import Dict, List, Tuple, Union

import requests
from django.conf import settings
from django.urls import reverse

from core.models import CoreSettings
from tickets.constants import SLACK_STATUS_REACTION
from tickets.models import Ticket


def slack_update_message(ticket: Ticket, core_settings: CoreSettings):
    """
    Update the Slack message for a given ticket.

    Removing old reactions, adding a new status-specific reaction,
    and updating the message content.

    Args:
        ticket (Ticket): The ticket object containing Slack-related information and status.
        core_settings (CoreSettings): The core settings provide API credentials for trello.
    """
    slack_remove_message_reaction(ticket=ticket, core_settings=core_settings)
    slack_update_message_reaction(ticket=ticket, core_settings=core_settings)
    slack_update_message_status(ticket=ticket, core_settings=core_settings)


def slack_create_message(ticket: Ticket, core_settings: CoreSettings) -> Tuple[str, str]:
    """
    Post a new ticket message to Slack and add a status-specific reaction.

    Args:
        ticket (Ticket): The ticket object containing details to be posted.
        core_settings (CoreSettings): The core settings provide API credentials for trello.

    Returns:
        Tuple[str, str]: A tuple containing the Slack message timestamp and channel ID.
    """
    try:
        data = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={
                "Authorization": f"Bearer {core_settings.slack_token}",
                "Content-Type": "application/json; charset=utf-8",
            },
            json={
                "channel": core_settings.slack_channel_id,
                "blocks": slack_message_blocks(ticket=ticket),
            },
        ).json()
        slack_update_message_reaction(ticket=ticket, core_settings=core_settings)
    except requests.exceptions.RequestException as e:
        # todo: do something about it, for example send an email
        print(e)
        return "", ""

    return data.get("ts"), data.get("channel")


def slack_update_message_status(ticket: Ticket, core_settings: CoreSettings):
    """
    Update the Slack message for a given ticket with the latest block content.

    Args:
        ticket (Ticket): The ticket object containing Slack channel ID, message timestamp, and ticket details.
        core_settings (CoreSettings): The core settings provide API credentials for trello.
    """
    requests.post(
        "https://slack.com/api/chat.update",
        headers={
            "Authorization": f"Bearer {core_settings.slack_token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        json={
            "channel": ticket.slack_channel_id,
            "ts": ticket.slack_message_ts,
            "blocks": slack_message_blocks(ticket=ticket),
        },
    )


def slack_update_message_reaction(ticket: Ticket, core_settings: CoreSettings):
    """
    Add a status-specific reaction to a Slack message associated with the given ticket.

    Args:
        ticket (Ticket): The ticket object containing Slack channel ID, message timestamp, and status.
        core_settings (CoreSettings): The core settings provide API credentials for trello.
    """
    requests.post(
        "https://slack.com/api/reactions.add",
        headers={
            "Authorization": f"Bearer {core_settings.slack_token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        json={
            "channel": ticket.slack_channel_id,
            "timestamp": ticket.slack_message_ts,
            "name": SLACK_STATUS_REACTION[ticket.status],
        },
    )


def slack_remove_message_reaction(ticket: Ticket, core_settings: CoreSettings):
    """
    Remove all reactions from a Slack message associated with the given ticket.

    Args:
        ticket (Ticket): The ticket object containing Slack channel ID and message timestamp.
        core_settings (CoreSettings): The core settings provide API credentials for trello.
    """
    data = requests.get(
        "https://slack.com/api/reactions.get",
        headers={
            "Authorization": f"Bearer {core_settings.slack_token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        params={
            "channel": ticket.slack_channel_id,
            "timestamp": ticket.slack_message_ts,
        },
    ).json()

    for reaction in data.get("message", {}).get("reactions", []):
        emoji_name = reaction["name"]

        requests.post(
            "https://slack.com/api/reactions.remove",
            headers={
                "Authorization": f"Bearer {core_settings.slack_token}",
                "Content-Type": "application/json; charset=utf-8",
            },
            json={
                "channel": ticket.slack_channel_id,
                "timestamp": ticket.slack_message_ts,
                "name": emoji_name,
            },
        )


def slack_message_blocks(ticket: Ticket) -> List[Dict[str, Union[str, dict]]]:
    """
    Generate Slack message blocks for a given ticket, including a link to the Django admin page and client information.

    Args:
        ticket (Ticket): The ticket object to generate Slack blocks for.

    Returns:
        List[Dict[str, Union[str, dict]]]: A list of Slack block elements formatted as dictionaries.
    """
    django_admin_path = reverse("admin:tickets_ticket_change", args=[ticket.pk])
    django_admin_url = f"{settings.BASE_URL}{django_admin_path}"
    client_id = ticket.client.pk if ticket.client else "N/A"
    client_name = ticket.client.name if ticket.client else "N/A"

    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"SM - 🪲 Ticket #{ticket.ticket_no}",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Admin: {django_admin_url}",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{ticket.title}*\n"
                f"Modul: {ticket.module}\n"
                f"Kunde: {client_name}\n"
                f"Kunden ID: {client_id} - "
                f"Shard: {ticket.pk} - "
                f"JTL-Version: {ticket.pk}",
            },
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"Trello: {ticket.trello_ticket_url}"},
        },
        {
            "block_id": "status",
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Status: {ticket.get_status_display()}*"},
        },
    ]
