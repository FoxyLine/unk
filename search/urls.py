from django.urls import path

from buyer.models import Stuff, StuffType

from . import views


urlpatterns = [
    path("search/", views.search_index, name="search"),
    path(
        "autocomplete/buyer/stuff",
        views.get_autocomplete(StuffType, "name"),
        name="autocomplete-buyer-stuff",
    ),
]
