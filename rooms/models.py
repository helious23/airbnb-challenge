from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django_countries.fields import CountryField
from core import models as core_models


class AbstractItem(core_models.TimeStampedModel):

    """Abstract Item"""

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """RoomType Model Definition"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ["created"]


class Amenity(AbstractItem):

    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"  # 복수형 Text 설정


class Facility(AbstractItem):

    """Facility Model Definition"""

    class Meta:
        verbose_name_plural = "Facilities"  # 복수형 Text 설정


class HouseRule(AbstractItem):

    """HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """Photo Model Definition"""

    def user_directory_path(self, filename):
        return "user_{0}/room_photos/room_{1}/{2}".format(
            self.room.host.id, self.room.id, filename
        )

    caption = models.CharField(max_length=120)
    file = models.ImageField(upload_to=user_directory_path)
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """Room Model Definition"""

    name = models.CharField(max_length=140, help_text="Maximum 140 Characters")
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=140)
    price = models.IntegerField(
        help_text="Minimum $ 5",
        validators=[MinValueValidator(5)],
    )

    guests = models.IntegerField(
        help_text="How many people will be staying?",
        validators=[MaxValueValidator(50), MinValueValidator(1)],
    )
    beds = models.IntegerField(
        help_text="Maximum 50, Minimum 0",
        validators=[MaxValueValidator(50), MinValueValidator(0)],
    )
    bedrooms = models.IntegerField(
        help_text="Maximum 50, Minimum 0",
        validators=[MaxValueValidator(50), MinValueValidator(0)],
    )
    baths = models.IntegerField(
        help_text="Maximum 50, Minimum 0",
        validators=[MaxValueValidator(50), MinValueValidator(0)],
    )

    check_in = models.TimeField()
    check_out = models.TimeField()

    instant_book = models.BooleanField(default=False)

    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType",
        related_name="rooms",
        on_delete=models.SET_NULL,
        null=True,
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def save(self, *args, **kwargs):
        self.city = self.city.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def total_acurrancy(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.acurrancy
        try:
            return round(all_ratings / len(all_reviews), 1)
        except ZeroDivisionError:
            return 0

    def acurrancy_percent(self):
        acurrancy = self.total_acurrancy()
        return acurrancy / 5 * 100

    def total_communication(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.communication
        try:
            return round(all_ratings / len(all_reviews), 1)
        except ZeroDivisionError:
            return 0

    def communication_percent(self):
        communication = self.total_communication()
        return communication / 5 * 100

    def total_cleanliness(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.cleanliness
        try:
            return round(all_ratings / len(all_reviews), 1)
        except ZeroDivisionError:
            return 0

    def cleanliness_percent(self):
        cleanliness = self.total_cleanliness()
        return cleanliness / 5 * 100

    def total_location(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.location
        try:
            return round(all_ratings / len(all_reviews), 1)
        except ZeroDivisionError:
            return 0

    def location_percent(self):
        location = self.total_location()
        return location / 5 * 100

    def total_check_in(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.check_in
        try:
            return round(all_ratings / len(all_reviews), 1)
        except ZeroDivisionError:
            return 0

    def check_in_percent(self):
        check_in = self.total_check_in()
        return check_in / 5 * 100

    def total_value(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.value
        try:
            return round(all_ratings / len(all_reviews), 1)
        except ZeroDivisionError:
            return 0

    def value_percent(self):
        value = self.total_value()
        return value / 5 * 100

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()
        try:
            return round(all_ratings / len(all_reviews), 2)
        except ZeroDivisionError:
            return 0
