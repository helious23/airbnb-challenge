import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.urls import reverse
from core import managers as core_managers


class User(AbstractUser):

    """Custom User Model"""

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"
    GENDER_CHOICES = (
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
        (GENDER_OTHER, _("Other")),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"
    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, _("English")),
        (LANGUAGE_KOREAN, _("Korean")),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"
    CURRENCY_CHOICES = ((CURRENCY_USD, "$ USD"), (CURRENCY_KRW, "₩ 원"))

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"
    LOGIN_NAVER = "naver"
    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "E-mail"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
        (LOGIN_NAVER, "Naver"),
    )

    def user_directory_path(self, filename):
        return "user_{0}/avatar/{1}".format(self.id, filename)

    avatar = models.ImageField(_("avatar"), upload_to=user_directory_path, blank=True)
    gender = models.CharField(
        _("gender"), choices=GENDER_CHOICES, max_length=40, blank=True
    )
    bio = models.TextField(_("bio"), default="", blank=True)
    birthdate = models.DateField(_("birthdate"), null=True, blank=True)
    language = models.CharField(
        _("language"),
        choices=LANGUAGE_CHOICES,
        max_length=2,
        blank=True,
        default=LANGUAGE_KOREAN,
    )
    currency = models.CharField(
        _("currency"),
        choices=CURRENCY_CHOICES,
        max_length=3,
        blank=True,
        default=CURRENCY_KRW,
    )
    superhost = models.BooleanField(_("superhost"), default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)
    login_method = models.CharField(
        _("login_method"), choices=LOGIN_CHOICES, max_length=12, default=LOGIN_EMAIL
    )

    objects = core_managers.CustomUserManager()

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )
            send_mail(
                _("Verify Maxbnb Account"),
                strip_tags(html_message),
                settings.EMAIL_FROM,
                # [self.email], # e-mail 수신자
                ["max16@naver.com"],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})
