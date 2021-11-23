from django.contrib import admin
from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    """Review Admin Definition"""

    raw_id_fields = ("user", "room")

    list_display = ("__str__", "rating_average")

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "user",
                    "room",
                    "review",
                )
            },
        ),
        (
            "Score",
            {
                "fields": (
                    "acurrancy",
                    "communication",
                    "cleanliness",
                    "location",
                    "check_in",
                    "value",
                ),
            },
        ),
    )
