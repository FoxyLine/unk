import json
from django.shortcuts import render
from django.http import JsonResponse
from .forms import MySearchForm


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
