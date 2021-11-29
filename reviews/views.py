from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from rooms import models as room_models
from . import forms, models


def create_review(request, room):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = request.user
            review.save()
            messages.success(request, "Room review is registered")
            return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))


def delete_review(request, room, review):
    room = room_models.Room.objects.get_or_none(pk=room)
    if not room:
        messages.error(request, "Can't delete the review")
        return redirect(reverse("core:home"))
    models.Review.objects.get(pk=review).delete()
    messages.info(request, "Review Deleted")
    return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
