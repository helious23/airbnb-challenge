from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):

    """Search Form Definition"""

    city = forms.CharField(initial="Anywhere", required=False)
    country = CountryField(blank=True, blank_label="Select Country").formfield()
    price = forms.IntegerField(required=False)
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any Kind", queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(required=False, min_value=5)
    guests = forms.IntegerField(required=False, min_value=1)
    bedrooms = forms.IntegerField(required=False, min_value=0)
    beds = forms.IntegerField(required=False, min_value=0)
    baths = forms.IntegerField(required=False, min_value=0)

    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)

    # amenities = forms.ModelMultipleChoiceField(
    #     queryset=models.Amenity.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False,
    # )
    # facilities = forms.ModelMultipleChoiceField(
    #     queryset=models.Facility.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False,
    # )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("caption", "file")

    def save(self, *args, **kwargs):
        photo = super().save(commit=False)
        return photo


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "address",
            "price",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "instant_book",
            "room_type",
            "amenities",
            "facilities",
            "house_rules",
        )

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        return room
