from clients.models import Client
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from tickets.constants import TICKET_STATUS_OPEN
from tickets.models import Ticket

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Create initial data in database."""
        print("Setting up admin user..")
        admin, created = User.objects.get_or_create(
            username="admin",
            email="info@domain.com",
            defaults={
                "is_active": True,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        print("Admin user was created, setting default password='AdminAdmin'")
        if created:
            admin.set_password("AdminAdmin")
            admin.save()

        print("Setting up testing client..")
        client, _ = Client.objects.get_or_create(name="Best Client", defaults={})

        print("Setting up testing ticket..")
        ticket, _ = Ticket.objects.get_or_create(
            ticket_no="64853",
            defaults={
                "draft": True,
                "status": TICKET_STATUS_OPEN,
                "client_id": client.pk,
                "title": "Mollie Zahlungen werden nicht verarbeitet.",
                "description": "<p>Wir haben aktuell das Problem, das keine Mollie Zahlungen zu unseren Bestellungen "
                "zugeordnet werden.</p><p>Das geht wohl schon eine ganze weile so. Wir haben lange nicht "
                "reingeschaut aber irgendwie macht das ja so keinen SInn.</p>",
                "module": "sellermatch",
                "last_joblog_log": "",
                "last_joblog_message": "Source Sync Metadata started...\n"
                "    Sync ok.\n"
                "        Manufacturers (+0/-0)\n"
                "        Shipping      (+0/-0)\n"
                "        Markets       (+0/-0)\n"
                "        Users         (+0/-0)",
                "last_joblog_stacktrace": "",
            },
        )
