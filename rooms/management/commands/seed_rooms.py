import os
from pathlib import Path
import random
import shutil
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from config.settings import BASE_DIR, MEDIA_ROOT
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    help = "This commands create rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many rooms do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(1, 500),
                "guests": lambda x: random.randint(1, 20),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        created_rooms = seeder.execute()
        created_clean = flatten(list(created_rooms.values()))
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        house_rules = room_models.HouseRule.objects.all()
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(5, random.randint(10, 30)):
                photo_num = random.randint(1, 31)
                user_id = room.host.id
                room_id = room.id
                directory = f"user_{user_id}/room_photos/room_{room_id}"
                path = Path.joinpath(MEDIA_ROOT, directory)
                os.makedirs(path, exist_ok=True)
                src = Path.joinpath(BASE_DIR, "photos_seed")
                des = path
                shutil.copyfile(f"{src}/{photo_num}.webp", f"{des}/{photo_num}.webp")
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"/user_{user_id}/room_photos/room_{room.id}/{photo_num}.webp",
                )
            for amenity in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(amenity)

            for facility in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(facility)

            for house_rule in house_rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(house_rule)

        self.stdout.write(self.style.SUCCESS(f"{number}  rooms Created"))
