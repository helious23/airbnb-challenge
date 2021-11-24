from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    """Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"
    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"
    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_KOREAN, "Korean"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"
    CURRENCY_CHOICES = ((CURRENCY_USD, "$ USD"), (CURRENCY_KRW, "₩ 원"))

    def user_directory_path(self, filename):
        return "user_{0}/avatar/{1}".format(self.id, filename)

    avatar = models.ImageField(upload_to=user_directory_path, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=40, blank=True)
    bio = models.TextField(default="", blank=True)
    birthdate = models.DateField(null=True, blank=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES,
        max_length=2,
        blank=True,
        # default=LANGUAGE_KOREAN,
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES,
        max_length=3,
        blank=True,
        # default=CURRENCY_KRW,
    )
    superhost = models.BooleanField(default=False)
