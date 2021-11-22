from django.contrib import admin
from . import models


@admin.register(models.Reservation)
class ReservatoinAdmin(admin.ModelAdmin):

    """Reservation Admin Definition"""

    raw_id_fields = (
        "guest",
        "room",
    )
