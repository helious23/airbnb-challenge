from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ngettext
from django.contrib import messages
from . import models
from rooms import models as room_models


class RoomInline(admin.StackedInline):

    classes = ("collapse",)
    model = room_models.Room
    extra = 0

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "city",
                    "address",
                    "price",
                    "room_type",
                ),
            },
        ),
        (
            "Times",
            {
                "classes": ("collapse",),
                "fields": ("check_in", "check_out", "instant_book"),
            },
        ),
        (
            "Spaces",
            {
                "classes": ("collapse",),
                "fields": (
                    "guests",
                    "beds",
                    "bedrooms",
                    "baths",
                ),
            },
        ),
        (
            "More About the Space",
            {
                "classes": ("collapse",),
                "fields": (
                    "amenities",
                    "facilities",
                    "house_rules",
                ),
            },
        ),
    )

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    inlines = (RoomInline,)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custum profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
    )

    actions = ["make_superhost"]

    @admin.action(description="Mark selected users as Superhost")
    def make_superhost(self, request, queryset):
        updated = queryset.update(superhost=True)
        self.message_user(
            request,
            ngettext(
                "%d user was successfully marked as Superhost.",
                "%d users were successfully marked as Superhost.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )
