from django.urls import path

from . import views

urlpatterns = [
    path("seller/", views.seller_index, name="seller"),
]
