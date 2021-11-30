from django import forms
from django.utils.translation import gettext_lazy as _


class AddCommentForm(forms.Form):

    message = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": _("Add a comment")})
    )
