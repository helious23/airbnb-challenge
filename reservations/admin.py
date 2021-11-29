from django.contrib import admin
from django.utils import timezone
from . import models


class ProgressListFilter(admin.SimpleListFilter):

    title = "In Progress"  # Filter 에 나타날 제목 : By In Progress
    parameter_name = "in_progress"  # Filter 할 대상

    # lookups 멤버 method 는 django 가 찾아서 필터링할 값에 대한 정보를 넣어주는 역할
    def lookups(self, request, model_admin):
        return (("True", "In Progress"), ("False", "Not In Progress"))
        # 첫 번째 인자는 필터링 할 값, 두 번째 인자는 filter에 보여질 값

    #
    def queryset(self, request, queryset):
        now = timezone.now().date()
        if self.value() == "True":  # in_progress 의 return value == True
            return queryset.filter(check_in__lte=now, check_out__gte=now)
            # check_in__lte = now : check_in <= now
        elif self.value() == "False":
            return queryset.exclude(check_in__lte=now, check_out__gte=now)


class FinishListFilter(admin.SimpleListFilter):

    title = "Is Finished"
    parameter_name = "is_finished"

    def lookups(self, request, model_admin):
        return (("True", "Finished"), ("False", "Not Finished"))

    def queryset(self, request, queryset):
        now = timezone.now().date()
        if self.value() == "True":
            return queryset.filter(check_out__lt=now)
        elif self.value() == "False":
            return queryset.exclude(check_out__lt=now)


@admin.register(models.Reservation)
class ReservatoinAdmin(admin.ModelAdmin):

    """Reservation Admin Definition"""

    list_display = (
        "room",
        "check_in",
        "check_out",
        "guest",
        "in_progress",
        "is_finished",
    )

    list_filter = ("status", ProgressListFilter, FinishListFilter)

    raw_id_fields = (
        "guest",
        "room",
    )

    search_fields = (
        "room__name",
        "room__host__username",
    )

    fieldsets = (
        (
            "Reservation Info",
            {
                "fields": ("status", "check_in", "check_out", "guest"),
            },
        ),
        ("Room Info", {"fields": ("room",)}),
    )


@admin.register(models.BookedDay)
class BookedDayAdmin(admin.ModelAdmin):

    """Booked Day Admin Definition"""

    list_display = ("day", "reservation")
