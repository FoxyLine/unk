from django import forms
from django.urls import reverse_lazy

from .models import Buyer, Mobile, MobileNumber, Stuff


class AutoCompleteWidget(forms.TextInput):
    def __init__(self, data_endpoint, attrs=None) -> None:
        self.data_endpoint = data_endpoint
        super().__init__(attrs)

    class Media:
        # js here
        js = ("widgets/autocomplete/autocomplete.js",)
        css = {"all": ["widgets/autocomplete/autocomplete.css"]}

    def render(self, name, value, attrs=None, renderer=None):
        if not attrs:
            attrs = {}

        attrs["autocomplete"] = "off"
        attrs["autocomplete-endpoint"] = self.data_endpoint
        html = super().render(name, value, attrs, renderer)
        return html


class StuffForm(forms.ModelForm):
    class Meta:
        model = Stuff
        fields = [
            "stuff_type",
            "mass",
            "unit",
        ]
        widgets = {
            "stuff_type": AutoCompleteWidget(
                data_endpoint=reverse_lazy("autocomplete-buyer-stuff")
            ),
        }


class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = [
            "first_name",
            "last_name",
            "patronymic",
            "birth_date",
            "shop_name",
            "shop_address",
            "shop_messanger_name",
            "account_name",
            "account_address",
            "account_number",
            "account_login",
            "account_password",
            "account_password_app",
            "payment",
            "crime_place",
            "arrest_date",
            "clad_coordinates",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "arrest_date": forms.DateInput(attrs={"type": "date"}),
        }


class MobileNumberForm(forms.ModelForm):
    class Meta:
        model = MobileNumber
        fields = ["code", "number"]


class MobileForm(forms.ModelForm):
    class Meta:
        model = Mobile
        fields = [
            "imei",
            "mobile_brand",
            "mobile_model",
            "password",
        ]

        # fields = [
        #     "imei",
        #     "mobile_brand",
        #     "mobile_model",
        #     "password",
        #     "mobile_number",
        #     "stuff_type",
        #     "stuff_mass",
        #     "unit",
        #     "shop_name",
        #     "shop_info",
        #     "operator_nickname",
        #     "operator_account",
        #     "account",
        #     "payment_type",
        #     "crime_place",
        #     "arrest_date",
        #     "clad_coordinates",
        # ]
