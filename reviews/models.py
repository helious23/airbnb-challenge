from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """Review Model Definition"""

    review = models.TextField()
    acurrancy = models.IntegerField(
        default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        help_text="Minimum 1, Maximum 5",
    )
    communication = models.IntegerField(
        default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        help_text="Minimum 1, Maximum 5",
    )
    cleanliness = models.IntegerField(
        default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        help_text="Minimum 1, Maximum 5",
    )
    location = models.IntegerField(
        default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        help_text="Minimum 1, Maximum 5",
    )
    check_in = models.IntegerField(
        default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        help_text="Minimum 1, Maximum 5",
    )
    value = models.IntegerField(
        default=5,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        help_text="Minimum 1, Maximum 5",
    )
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"{self.review} by {self.user.email} - {self.room}"

    def rating_average(self):
        avg = (
            self.acurrancy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)  # 소수점 3자리수 에서 반올림

    rating_average.short_description = "AVG."
