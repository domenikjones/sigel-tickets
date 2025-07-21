from typing import Tuple

import requests

from core.models import CoreSettings
from tickets.models import Ticket, TrelloLabel


def trello_create_ticket(ticket: Ticket, core_settings: CoreSettings) -> Tuple[str, str]:
    """
    Create a new Trello card in the specified Trello list using the given ticket information.

    Args:
        ticket (Ticket): The ticket object containing title and description to create the Trello card.
        core_settings (CoreSettings): The core settings provide API credentials for trello.

    Returns:
        Tuple[str, str]: A tuple containing the Trello card ID and URL. Returns empty strings if an exception occurs.
    """
    try:
        data = requests.post(
            url="https://api.trello.com/1/cards",
            headers={"Accept": "application/json"},
            params={
                "idList": core_settings.trello_list_id,
                "key": core_settings.trello_api_key,
                "token": core_settings.trello_api_token,
                "name": f"{ticket.title} | Ticket #{ticket.pk} | Module: {ticket.module}",
                "desc": ticket.description,
            },
        ).json()
    except requests.exceptions.RequestException as e:
        # todo: do something about it, for example send an email
        print("trello exception", e)
        return "", ""

    return data.get("id"), data.get("url")


def trello_add_label(ticket: Ticket, core_settings: CoreSettings):
    """Adds a Trello label to a card based on the ticket's module.

    This function fetches the appropriate Trello label for the given
    ticket's module and attaches it to the Trello card via the Trello API.
    If no label is found for the module, the function returns early
    without making any API request.

    Args:
        ticket (Ticket): The ticket object containing module and Trello card ID information.
        core_settings (CoreSettings): Settings object that includes Trello API credentials.

    Returns:
        None
    """
    trello_label = TrelloLabel.objects.filter(module=ticket.module).first()

    if not trello_label:
        return

    requests.post(
        url=f"https://api.trello.com/1/cards/{ticket.trello_ticket_id}/idLabels",
        headers={"Accept": "application/json"},
        params={
            "key": core_settings.trello_api_key,
            "token": core_settings.trello_api_token,
            "value": trello_label.trello_label_id,
        },
    )
