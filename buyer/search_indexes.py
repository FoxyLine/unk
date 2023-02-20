from email.policy import default
from django.db import models

import datetime
from haystack import indexes
from .models import Buyer, Stuff


class BuyerIndex(indexes.SearchIndex, indexes.Indexable):

    doc_id = indexes.CharField(document=True)
    text = indexes.CharField(use_template=True)
    last_name = indexes.CharField(model_attr="last_name", null=True)
    first_name = indexes.CharField(model_attr="first_name", null=True)
    patronymic = indexes.CharField(model_attr="patronymic", null=True)
    birth_date = indexes.DateField(model_attr="birth_date", null=True)
    stuffs = indexes.MultiValueField()

    def prepare_stuffs(self, obj: Buyer):
        return [s.stuff_type.name for s in Stuff.objects.filter(buyer=obj)]

    def get_model(self):
        return Buyer

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
