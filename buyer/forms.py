from random import random
from django import forms
from django.urls import reverse_lazy

from .models import (
    Buyer,
    Mobile,
    MobileNumber,
    Stuff,
    Clad,
    OnlinePay,
    Crypto,
    Bank,
    InternetAccount,
)


class AutoCompleteWidget(forms.TextInput):
    def __init__(self, data_endpoint, separator=None, attrs=None) -> None:
        self.data_endpoint = data_endpoint
        self.separator = separator
        super().__init__(attrs)

    class Media:
        # js here
        js = ("widgets/autocomplete/autocomplete.js",)
        css = {"all": ["widgets/autocomplete/autocomplete.css"]}

    def render(self, name, value, attrs=None, renderer=None):
        if not attrs:
            attrs = {}

        attrs["autocomplete"] = "off"
        if self.separator:
            attrs["separator"] = self.separator
        attrs["autocomplete-endpoint"] = self.data_endpoint
        html = super().render(name, value, attrs, renderer)
        return html


class SwitchFormsWidget(forms.Select):
    class Media:
        # js here
        js = ("widgets/switch_form_widget/switch_form_widget.js",)

    def __init__(self, group_switch, swithces=(), attrs=None) -> None:
        if attrs is None:
            attrs = {"switcher": ""}
        attrs["onchange"] = f"switchForm(event, '{group_switch}', {swithces})"
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if not attrs:
            attrs = {}
        html = super().render(name, value, attrs, renderer)
        return html

    def create_option(self, *args, **kwargs):
        kwargs["attrs"]["test"] = "ASD"
        args = ["test" + str(random()), *args[1:]]
        return super().create_option(*args, **kwargs)


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
            "shop_type",
            "shop_name",
            "shop_address",
            "shop_messanger_name",
            "payment",
            "crime_place",
            "arrest_date",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "arrest_date": forms.DateInput(attrs={"type": "date"}),
            "shop_type": SwitchFormsWidget(
                group_switch="shop",
                swithces=["shop_type_1", "shop_type_2", "shop_type_3"],
            ),
            "payment": SwitchFormsWidget(
                group_switch="payment",
                swithces=["payment_type_1", "payment_type_2", "payment_type_3"],
            ),
        }


class InternetAccountForm(forms.ModelForm):
    class Meta:
        model = InternetAccount
        fields = [
            "login",
            "password",
            "app_password",
            "name",
            "account_address",
            "number",
            "operator_nickname",
            "operator_account",
        ]


class MobileNumberForm(forms.ModelForm):
    class Meta:
        model = MobileNumber
        fields = ["number"]


class CladForm(forms.ModelForm):
    class Meta:
        model = Clad
        fields = ["photo", "latitude", "longitude"]
        widgets = {"photo": forms.FileInput(attrs={"onchange": "setFileName(event)"})}


class MobileForm(forms.ModelForm):
    forms.CharField

    class Meta:
        model = Mobile
        fields = [
            "imei",
            "mobile_brand",
            "mobile_model",
            "password",
        ]


class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = [
            "name",
            "card_number",
        ]


class OnlinePayForm(forms.ModelForm):
    class Meta:
        model = OnlinePay
        fields = [
            "name",
            "account",
        ]


class CryptoForm(forms.ModelForm):
    class Meta:
        model = Crypto
        fields = [
            "name",
            "address_wallet",
        ]
