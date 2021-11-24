from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.core.paginator import Paginator
from django.shortcuts import render
from . import models, forms


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 24
    paginate_orphans = 5
    ordering = "created"
    page_kwarg = "page"
    context_object_name = "rooms"


class RoomDetail(DetailView):

    """Room Detail Definition"""

    model = models.Room


class SearchView(View):

    """Search View Definition"""

    def get(self, request):
        city = request.GET.get("city")
        if city:
            form = forms.SearchForm(request.GET)  # form 내용 받아옴
            if form.is_valid():
                # cleaned_data.get 으로 form 안의 data 를 바로 받을 수 있음
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                price = form.cleaned_data.get("price")
                room_type = form.cleaned_data.get("room_type")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                # amenities = form.cleaned_data.get("amenities")  # queryset 으로 받음
                # facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city
                if country != "":
                    filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                # for amenity in amenities:
                #     filter_args["amenities"] = amenity

                # for facility in facilities:
                #     filter_args["facilities"] = facility

                print(filter_args)
                qs = models.Room.objects.filter(**filter_args).order_by("-created")
                # paginator 사용 시 queryset 의 order 기준이 필요함

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request,
                    "rooms/search.html",
                    {"form": form, "rooms": rooms},
                )
        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})
