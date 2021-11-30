from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "This commands create superuser"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username="ebadmin")
        if not admin:
            User.objects.create_superuser("ebadmin", "max16@naver.com", "ebadmin")
            self.stdout.write(self.style.SUCCESS("Superuser Created"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser Exists"))
