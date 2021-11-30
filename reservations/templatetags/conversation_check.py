from django import template
from django.db.models import Q
from conversations import models as conversation_models

register = template.Library()


@register.simple_tag(takes_context=True)
def conversation_check(context, reservation):
    user = context.request.user
    if reservation.room.host == user:
        conversation = conversation_models.Conversation.objects.get(
            Q(participants=user) & Q(participants=reservation.guest)
        )
        print((conversation))
        return conversation
    else:
        print(user)
        print(reservation.room.host)
        conversation = conversation_models.Conversation.objects.get(
            Q(participants=user) & Q(participants=reservation.room.host)
        )
        print((conversation))
        return conversation
