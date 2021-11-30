from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def review_check(context, reservation):
    user = context.request.user
    try:
        (review,) = user.reviews.filter(room=reservation.room)
        return review
    except ValueError:
        return None
