import json
from django.shortcuts import render
from django.http import JsonResponse
from haystack.query import SearchQuerySet
from haystack.forms import SearchForm
from datetime import datetime

# Create your views here.
from buyer.models import Buyer
from buyer.elastic import search_by_clause
from django import forms


class MySearchForm(SearchForm):
    first_name = forms.CharField(required=False, label="Имя")
    start_birth_date = forms.DateField(
        required=False, label="Рожден с", widget=forms.DateInput(attrs={"type": "date"})
    )
    end_birth_date = forms.DateField(
        required=False,
        label="Рожден до",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def search(self):
        if not self.is_valid():
            return search_by_clause({})

        filters = []
        if self.cleaned_data["start_birth_date"] or self.cleaned_data["end_birth_date"]:
            range_clause = {"range": {"birth_date": {}}}
            if self.cleaned_data["start_birth_date"]:
                range_clause["range"]["birth_date"]["gte"] = self.cleaned_data["start_birth_date"].isoformat()
            if self.cleaned_data["end_birth_date"]:
                range_clause["range"]["birth_date"]["lte"] = self.cleaned_data["start_birth_date"].isoformat()

            filters.append(range_clause)


        if self.cleaned_data["first_name"]:
            filters.append({"match": {"first_name": self.cleaned_data["first_name"]}})
        clause = {"query": {"bool": {"must":filters}}}
        return search_by_clause(clause)


def get_autocomplete(model, field):
    def autocomplete_buyer_stuff(request):
        query = request.GET.get("q")
        if query is None:
            return JsonResponse([], safe=False)
        queryset = (
            model.objects.filter(**{field + "__istartswith": query}).values(field).all()
        )
        return JsonResponse([obj[field] for obj in queryset], safe=False)

    return autocomplete_buyer_stuff


def search_index(request):
    result = None
    if request.method == "POST":
        form = MySearchForm(request.POST)
        result = form.search()
    else:
        form = MySearchForm()
        result = form.search()

    return render(
        request, template_name="search.html", context={"form": form, "result": result}
    )
