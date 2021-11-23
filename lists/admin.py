from django.contrib import admin
from . import models


@admin.register(models.List)
class ListAdming(admin.ModelAdmin):

    """List Admin Definition"""

    list_display = ("name", "user", "count_rooms")

    search_fields = ("name",)

    raw_id_fields = ("user",)
    filter_horizontal = ("rooms",)
