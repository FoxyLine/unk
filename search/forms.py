from haystack.query import SearchQuerySet
from haystack.forms import SearchForm
from datetime import datetime
from django.urls import reverse_lazy

# Create your views here.
from buyer.models import Buyer, Stuff
from buyer.forms import AutoCompleteWidget
from buyer.elastic import search_by_clause
from django import forms


def insensitive_part_clause(field, query: str):
    return {
        "wildcard": {
            field: {
                "value": f"*{query.lower()}*",
                "case_insensitive": True,
            }
        }
    }


SEPARATOR = ","

SEARCH_OPTION = {
    1: lambda query: f"*{query}*",
    2: lambda query: f"{query}*",
    3: lambda query: f"*{query}",
}


class MySearchForm(SearchForm):
    full_text = forms.CharField(required=False, label="Общий поиск")
    first_name = forms.CharField(required=False, label="Имя")
    last_name = forms.CharField(required=False, label="Фамилия")
    patronymic = forms.CharField(required=False, label="Отчество")

    shop_name = forms.CharField(required=False, label="Наименование интернет-магазина")
    shop_type = forms.ChoiceField(
        required=False, label="Тип магазина", choices=Buyer.SHOP_CHOICES
    )
    shop_address = forms.CharField(required=False, label="Адресс магазина")
    shop_messanger_name = forms.CharField(
        required=False, label="Наименование мессенджера"
    )
    payment = forms.ChoiceField(
        required=False, label="Способ оплаты", choices=Buyer.PAYMENT_CHOICES
    )

    crime_place = forms.ChoiceField(
        required=False,
        label="Место совершения преступления",
        choices=Buyer.CRIME_PLACE_CHOICES,
    )
    start_arrest_date = forms.DateField(
        required=False,
        label="Аррест с",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    end_arrest_date = forms.DateField(
        required=False,
        label="Аррест до",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    start_birth_date = forms.DateField(
        required=False, label="Рожден с", widget=forms.DateInput(attrs={"type": "date"})
    )
    end_birth_date = forms.DateField(
        required=False,
        label="Рожден до",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    stuffs = forms.CharField(
        required=False,
        label="Вещества",
        widget=AutoCompleteWidget(
            data_endpoint=reverse_lazy("autocomplete-buyer-stuff"), separator=SEPARATOR
        ),
    )
    all_stuffs = forms.BooleanField(label="Содержит все", required=False)

    start_stuff_mass = forms.FloatField(required=False, label="От")
    start_stuff_mass_unit = forms.ChoiceField(
        required=False, label="", choices=Stuff.UNIT_CHOICES
    )

    end_stuff_mass = forms.FloatField(required=False, label="До")
    end_stuff_mass_unit = forms.ChoiceField(
        required=False, label="", choices=Stuff.UNIT_CHOICES
    )

    mobile_imei = forms.CharField(required=False, label="IMEI-номер")
    mobile_brand = forms.CharField(required=False, label="Марка")
    mobile_model = forms.CharField(required=False, label="Модель")
    mobile_password = forms.CharField(required=False, label="Пароль")

    mobile_number = forms.CharField(required=False, label="Номер телефона")
    mobile_number_search_option = forms.ChoiceField(
        choices=[(1, "Включает"), (2, "Начинается"), (3, "Оканчивается")],
        required=False,
    )

    bank_name = forms.CharField(required=False, label="Название банка")
    bank_card_number = forms.CharField(required=False, label="Номер банковской карты")
    online_pay_name = forms.CharField(required=False, label="Название платежной системы")
    online_pay_account = forms.CharField(required=False, label="Номер счета")
    crypto_name = forms.CharField(required=False, label="Название криптовалюты")
    crypto_address_wallet = forms.CharField(required=False, label="Адрес кошелька")

    account_login = forms.CharField(required=False, label="Логин")
    account_password = forms.CharField(required=False, label="Пароль")
    account_app_password = forms.CharField(required=False, label="Пароль приложения")
    account_name = forms.CharField(required=False, label="Имя аккаунта")
    account_address = forms.CharField(required=False, label="«Аккаунт-адрес»")
    account_number = forms.CharField(required=False, label="Абонентский номер (привязанный к аккаунту)")
    account_operator_nickname = forms.CharField(required=False, label="Ник-нейм оператора")
    account_operator_account = forms.CharField(required=False, label="Аккаунт оператора")

    def search(self):
        if not self.is_valid():
            return search_by_clause({})

        data = self.cleaned_data

        filters = []
        if data["start_birth_date"] or data["end_birth_date"]:
            range_clause = {"range": {"birth_date": {}}}
            if data["start_birth_date"]:
                range_clause["range"]["birth_date"]["gte"] = data[
                    "start_birth_date"
                ].isoformat()
            if data["end_birth_date"]:
                range_clause["range"]["birth_date"]["lte"] = data[
                    "start_birth_date"
                ].isoformat()

            filters.append(range_clause)

        for es_field, data_field in [
            ("first_name", "first_name"),
            ("banks.name", "bank_name"),
            ("banks.card_number", "bank_card_number"),
            ("online_pays.name", "online_pay_name"),
            ("online_pays.account", "online_pay_account"),
            ("cryptos.name", "crypto_name"),
            ("cryptos.address_wallet", "crypto_address_wallet"),
            ("last_name", "last_name"),
            ("patronymic", "patronymic"),
            ("mobiles.password", "mobile_password"),
            ("mobiles.imei", "mobile_imei"),
            ("mobiles.mobile_brand", "mobile_brand"),
            ("mobiles.mobile_model", "mobile_model"),
            ("accounts.login", "account_login"),
            ("accounts.password", "account_password"),
            ("accounts.app_password", "account_app_password"),
            ("accounts.name", "account_name"),
            ("accounts.address", "account_address"),
            ("accounts.number", "account_number"),
            ("accounts.operator_nickname", "account_operator_nickname"),
            ("accounts.operator_account", "account_operator_account"),
        ]:
            if data[data_field]:
                filters.append(insensitive_part_clause(es_field, data[data_field]))

        if data['full_text']:
            filters.append(
                {"match": {"full_text": {"query": data['full_text']}}}
            )

        if data["stuffs"]:
            operator = "AND" if data["all_stuffs"] else "or"
            query = data["stuffs"].replace(SEPARATOR, " ")

            filters.append(
                {"match": {"stuffs.name": {"query": query, "operator": operator}}}
            )


        if data["start_stuff_mass"] or data["end_stuff_mass"]:
            range_clause = {"range": {"stuffs.mass": {}}}
            if data["start_stuff_mass"]:
                mass = Stuff.normalize_mass(
                    data["start_stuff_mass"], data["start_stuff_mass_unit"]
                )
                range_clause["range"]["stuffs.mass"]["gte"] = mass
            if data["end_stuff_mass"]:
                mass = Stuff.normalize_mass(
                    data["end_stuff_mass"], data["end_stuff_mass_unit"]
                )
                range_clause["range"]["stuffs.mass"]["lte"] = mass

            filters.append(range_clause)

        if data["mobile_number"]:
            search_clause = SEARCH_OPTION[int(data["mobile_number_search_option"]) or 1]

            query = search_clause(query=data["mobile_number"].lower())
            filters.append(
                {
                    "wildcard": {
                        "mobile_numbers.number": {
                            "value": query,
                            "case_insensitive": True,
                        }
                    }
                }
            )

        clause = {"query": {"bool": {"must": filters}}}
        import pprint

        pprint.pprint(clause)
        return search_by_clause(clause)
