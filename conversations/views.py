from django.shortcuts import redirect, render
from django.http import Http404
from django.views.generic import View
from django.urls import reverse
from users import models as user_models
from . import models


def go_conversation(request, host_pk, guest_pk):
    host_user = user_models.User.objects.get_or_none(pk=host_pk)
    guest_user = user_models.User.objects.get_or_none(pk=guest_pk)
    if host_user is not None and guest_user is not None:
        try:
            (conversation,) = models.Conversation.objects.filter(
                participants=host_user
            ).filter(participants=guest_user)
            print(conversation)
        except (models.Conversation.DoesNotExist or ValueError):
            conversation = models.Conversation.objects.create()
            conversation.participants.add(host_user, guest_user)
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {"conversation": conversation},
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        if message is not None:
            models.Message.objects.create(
                message=message, user=self.request.user, conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
