from typing import Tuple

import requests

from tickets.constants import TRELLO_API_KEY, TRELLO_API_TOKEN, TRELLO_DEFAULT_LIST_ID
from tickets.models import Ticket


def trello_create_ticket(ticket: Ticket, trello_list_id: str = TRELLO_DEFAULT_LIST_ID) -> Tuple[str, str]:
    """
    Create a new Trello card in the specified Trello list using the given ticket information.

    Args:
        ticket (Ticket): The ticket object containing title and description to create the Trello card.
        trello_list_id (str, optional): The ID of the Trello list where the card will be created.
        Defaults to TRELLO_DEFAULT_LIST_ID.

    Returns:
        Tuple[str, str]: A tuple containing the Trello card ID and URL. Returns empty strings if an exception occurs.
    """
    try:
        data = requests.post(
            url="https://api.trello.com/1/cards",
            headers={"Accept": "application/json"},
            params={
                "idList": trello_list_id,
                "key": TRELLO_API_KEY,
                "token": TRELLO_API_TOKEN,
                "name": ticket.title,
                "desc": ticket.description,
            },
        ).json()
    except requests.exceptions.RequestException as e:
        # todo: do something about it, for example send an email
        print("trello exception", e)
        return "", ""

    return data.get("id"), data.get("url")
