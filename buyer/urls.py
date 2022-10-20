from django.urls import path

from . import views

urlpatterns = [
    path("buyer/", views.buyer_index, name="buyer"),
]
