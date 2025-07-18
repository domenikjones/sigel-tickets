import requests

from django.core.management import BaseCommand

from core.models import CoreSettings
from tickets.models import TrelloLabel, Ticket
from tickets.trello import trello_add_label


class Command(BaseCommand):
    def handle(self, *args, **options):
        core_settings = CoreSettings.objects.first()
        if not core_settings:
            print("CoreSettings not found, please configure it.")
            return

        ticket = Ticket.objects.first()
        trello_add_label(ticket=ticket, core_settings=core_settings)
