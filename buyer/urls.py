from django.urls import path

from . import views

urlpatterns = [
    path("create-buyer/<int:buyer_id>", views.create_buyer, name="update-buyer"),
    path("create-buyer/", views.create_buyer, name="create-buyer"),
    path("buyer/", views.buyer, name="buyer"),
]
