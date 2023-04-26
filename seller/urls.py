from django.urls import path

from . import views

urlpatterns = [
    path("create-seller/<int:seller_id>", views.create_seller, name="update-seller"),
    path("create-seller/", views.create_seller, name="create-seller"),
    path("seller/", views.seller_index, name="seller"),
]
