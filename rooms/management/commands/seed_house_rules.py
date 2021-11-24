from django.core.management.base import BaseCommand
from rooms.models import HouseRule


class Command(BaseCommand):
    help = "This commands create facilities"

    def handle(self, *args, **options):
        house_rules = ["No Smoking", "No Pets", "No Parties or Events"]
        num_of_house_rules = 0
        for facility in house_rules:
            if not HouseRule.objects.filter(name=facility):
                num_of_house_rules += 1
                HouseRule.objects.create(name=facility)
        self.stdout.write(
            self.style.SUCCESS(f"✅ {num_of_house_rules} House Rules created")
        )
