from django.contrib import admin
from . import models


@admin.register(models.List)
class ListAdming(admin.ModelAdmin):

    """List Admin Definition"""

    raw_id_fields = ("user",)
    filter_horizontal = ("rooms",)
