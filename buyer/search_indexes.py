from email.policy import default
from django.db import models
from django.forms.models import model_to_dict

import datetime
from haystack import indexes
from .models import Buyer, Stuff


class MultiValueObjectField(indexes.MultiValueField):
    field_type = "object"


class BuyerIndex(indexes.SearchIndex, indexes.Indexable):
    doc_id = indexes.CharField(document=True)
    text = indexes.CharField(use_template=True)
    last_name = indexes.CharField(model_attr="last_name", null=True)
    first_name = indexes.CharField(model_attr="first_name", null=True)
    patronymic = indexes.CharField(model_attr="patronymic", null=True)
    birth_date = indexes.DateField(model_attr="birth_date", null=True)
    payment = indexes.CharField(model_attr="payment", null=True)
    crime_place = indexes.CharField(model_attr="crime_place", null=True)
    arrest_date = indexes.DateField(model_attr="arrest_date", null=True)

    stuffs = MultiValueObjectField()
    cryptos = MultiValueObjectField()
    online_pays = MultiValueObjectField()
    banks = MultiValueObjectField()
    mobiles = MultiValueObjectField()
    # clads = MultiValueObjectField()
    mobile_numbers = MultiValueObjectField()
    accounts = MultiValueObjectField()

    def prepare_cryptos(self, obj: Buyer):
        return [model_to_dict(c) for c in obj.cryptos.all()]

    def prepare_stuffs(self, obj: Buyer):
        return [
            {"name": s.stuff_type.name, "mass": s.mass and s.std_mass()}
            for s in obj.stuffs.all()
        ]

    def prepare_cryptos(self, obj: Buyer):
        return [model_to_dict(c) for c in obj.cryptos.all()]

    def prepare_online_pays(self, obj):
        return [model_to_dict(online_pay) for online_pay in obj.online_pays.all()]

    def prepare_banks(self, obj):
        return [model_to_dict(bank) for bank in obj.banks.all()]

    def prepare_mobiles(self, obj):
        return [model_to_dict(mobile) for mobile in obj.mobiles.all()]

    # def prepare_clads(self, obj):
    # return [model_to_dict(clad) for clad in obj.clads.all()]

    def prepare_mobile_numbers(self, obj):
        return [
            model_to_dict(mobile_number) for mobile_number in obj.mobile_numbers.all()
        ]

    def prepare_accounts(self, obj):
        return [model_to_dict(account) for account in obj.accounts.all()]

    def get_model(self):
        return Buyer

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
