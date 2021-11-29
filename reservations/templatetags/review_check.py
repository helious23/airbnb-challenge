from django import template

register = template.Library()


@register.simple_tag
def review_check(user, reservation):
    try:
        (review,) = user.reviews.filter(room=reservation.room)
        return review
    except ValueError:
        return None
