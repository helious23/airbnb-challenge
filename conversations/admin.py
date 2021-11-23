from django.contrib import admin
from . import models


@admin.register(models.Conversation)
class ConversatoinAdmin(admin.ModelAdmin):

    """Conversation Admin Definition"""

    filter_horizontal = ("participants",)
    list_display = (
        "__str__",
        "count_participants",
        "count_messages",
    )


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """Message Admin Definition"""

    list_display = ("__str__", "show_users", "created")
    fieldsets = (("Message", {"fields": ("message", "user", "conversation")}),)
    raw_id_fields = ("user", "conversation")

    def show_users(self, obj):
        return obj.conversation

    show_users.short_description = "Participants"
