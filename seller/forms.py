from random import random
from django import forms
from django.urls import reverse_lazy

from .models import Seller
from buyer.forms import SwitchFormsWidget
from buyer.models import Clad


class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = [
            "first_name",
            "last_name",
            "patronymic",
            "birth_date",
            "arrest_date",
            "shop_type",
            "shop_name",
            "shop_address",
            "crime_place",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "arrest_date": forms.DateInput(attrs={"type": "date"}),
            "shop_type": SwitchFormsWidget(
                group_switch="shop",
                swithces=["shop_type_1", "shop_type_2", "shop_type_3"],
            ),
            # "payment": SwitchFormsWidget(
            #     group_switch="payment",
            #     swithces=["payment_type_1", "payment_type_2", "payment_type_3"],
            # ),
        }


class MasterCladForm(forms.ModelForm):
    class Meta:
        model = Clad
        fields = ["lng", "lat", "photo"]
