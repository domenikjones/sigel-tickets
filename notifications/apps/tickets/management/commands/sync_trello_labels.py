import requests

from django.core.management import BaseCommand

from core.models import CoreSettings
from tickets.models import TrelloLabel


class Command(BaseCommand):
    def handle(self, *args, **options):
        core_settings = CoreSettings.objects.first()
        if not core_settings:
            print("CoreSettings not found, please configure it.")
            return

        # fetch existing labels from trello
        res = requests.get(
            f"https://api.trello.com/1/boards/{core_settings.trello_board_id}/labels",
            headers={"Accept": "application/json"},
            params={
                "key": core_settings.trello_api_key,
                "token": core_settings.trello_api_token,
            },
        )

        for label in res.json():
            label, created = TrelloLabel.objects.get_or_create(
                trello_label_id=label["id"],
                defaults={
                    "trello_label_name": label["name"],
                    "trello_label_color": label["color"],
                },
            )
            if created:
                print(f"Created new trello label: {label}")
