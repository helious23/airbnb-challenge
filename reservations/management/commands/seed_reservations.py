import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from reservations import models as reservation_models
from users import models as user_models
from rooms import models as room_models


NAME = "reservations"


class Command(BaseCommand):
    help = f"This commands create {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help=f"How many {NAME} do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        guests = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder.add_entity(
            reservation_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda x: random.choice(guests),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: datetime.now()
                + timedelta(days=random.randint(-10, 25)),
            },
        )
        created_reservation = seeder.execute()
        created_clean = flatten(list(created_reservation.values()))
        for pk in created_clean:
            reservation = reservation_models.Reservation.objects.get(pk=pk)
            check_in = reservation.check_in
            # print(vars(reservation))
            check_out = check_in + timedelta(days=random.randint(3, 25))
            reservation.check_out = check_out
            reservation.save()

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} Created"))
