from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext
from django.contrib import messages
from . import models


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):

    """Item Admin Definition"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):

    model = models.Photo
    classes = ("collapse",)

    fieldsets = (
        (
            "Photo Info",
            {
                "fields": (
                    "caption",
                    "file",
                ),
            },
        ),
    )


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    actions = ("make_instant_book",)
    inlines = (PhotoInline,)

    @admin.action(description="Mark selected rooms as instant booking")
    def make_instant_book(self, request, queryset):
        updated = queryset.update(instant_book=True)
        self.message_user(
            request,
            ngettext(
                "%d room was successfully marked as instant booking.",
                "%d rooms were successfully marked as instant booking.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    fieldsets = (
        (
            "BasicInfo",
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
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
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
        ("Last Details", {"fields": ("host",)}),
    )

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    search_fields = ("^city", "^host__username")

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    raw_id_fields = ("host",)

    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = "# Amenities"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "# Photos"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """Photo Admin Definition"""

    raw_id_fields = ("room",)

    list_display = ("room", "photo_owner", "caption", "get_thumbnail")

    def photo_owner(self, obj):
        return obj.room.host.username

    photo_owner.short_description = "Room Owner"

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="100px" src="{obj.file.url}" />')
        # input 창의 html 을 실행 시키기 위해 mark_safe 사용

    get_thumbnail.short_description = "Thumbnail"
