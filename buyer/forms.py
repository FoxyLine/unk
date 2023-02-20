from random import random
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
            "clad_coordinates",
            "bank_name",
            "bank_card_number",
            "online_pay_name",
            "online_pay_account",
            "crypto_name",
            "crypto_address_wallet",
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


class AccountBuyerForm(forms.Form):
    login = forms.CharField(
        label="Логин",
        required=False,
    )
    password = forms.CharField(label="Пароль", max_length=100, required=False)
    app_password = forms.CharField(
        label="Пароль приложения", max_length=100, required=False
    )


class MessengerForm(AccountBuyerForm):
    name = forms.CharField(label="Имя аккаунта", max_length=100, required=False)
    account_address = forms.CharField(
        label="«Аккаунт-адрес»", max_length=100, required=False
    )
    number = forms.CharField(
        label="Абонентский номер (привязанный к аккаунту)",
        max_length=100,
        required=False,
    )
    operator_nickname = forms.CharField(
        label="Ник-нейм оператора", max_length=100, required=False
    )
    operator_account = forms.CharField(
        label="Аккаунт оператора", max_length=100, required=False
    )


class SiteForm(AccountBuyerForm):
    ...


class DarkWebForm(AccountBuyerForm):
    ...


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
