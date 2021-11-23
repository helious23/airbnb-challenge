from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):
    help = "This commands create facilities"

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Parking",
            "Gym",
            "Pool",
            "Elevator",
            "Paid parking on premises",
            "Paid parking off premises",
        ]
        num_of_facilities = 0
        for facility in facilities:
            if not Facility.objects.filter(name=facility):
                num_of_facilities += 1
                Facility.objects.create(name=facility)
        self.stdout.write(
            self.style.SUCCESS(f"✅ {num_of_facilities} Facilities created")
        )
