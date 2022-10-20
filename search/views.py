import json
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.


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
    return render(request, template_name="search.html")
