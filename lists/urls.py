from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    path("add/<int:room_pk>", views.toggle_room, name="toggle-room"),
    path("favs/", views.SeeFabsView.as_view(), name="see-favs"),
]
