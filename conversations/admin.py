from django.contrib import admin
from . import models


@admin.register(models.Mesages)
class MessageAdmin(admin.ModelAdmin):

    """Message Admin Definition"""

    list_display = ("__str__", "created")
    raw_id_fields = ("user", "conversation")


@admin.register(models.Conversation)
class ConversatoinAdmin(admin.ModelAdmin):

    """Conversation Admin Definition"""

    filter_horizontal = ("participants",)
