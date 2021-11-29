import datetime
from django import template
from reservations import models as reservatoin_models

register = template.Library()


@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return
    try:
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        reservatoin_models.BookedDay.objects.get(day=date, reservation__room=room)
        return True
    except reservatoin_models.BookedDay.DoesNotExist:
        return False
