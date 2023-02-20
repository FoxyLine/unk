from django.conf import settings
from elasticsearch import Elasticsearch
from .models import Buyer

es: Elasticsearch = settings.ES


def more_like_buyer_by_id(buyer_id, limit=5, fields=None) -> Buyer:

    results = es.search(
        {
            "query": {
                "more_like_this": {
                    "like": [{"_index": "haystack", "_id": f"buyer.buyer.{buyer_id}"}],
                    "min_term_freq": 1,
                }
            }
        },
        size=limit,
    )
    ids = []
    for hit in results["hits"]["hits"]:
        ids.append(hit["_source"]["django_id"])

    return Buyer.objects.filter(id__in=ids)


def find_buyer(limit=5, **kwargs) -> Buyer:
    match_clauses = [{"fuzzy": {k: v}} for k, v in kwargs.items() if v]
    results = es.search({"query": {"bool": {"must": match_clauses}}}, size=limit)
    ids = []
    for hit in results["hits"]["hits"]:
        ids.append(hit["_source"]["django_id"])

    return Buyer.objects.filter(id__in=ids)


def multi_match_find(query, limit=10):
    if query:
        clause = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["last_name", "stuffs", "patronymic", "first_name"],
                },
            }
        }
    else:
        clause = {}

    results = es.search(
        clause,
        size=limit,
    )
    ids = []
    for hit in results["hits"]["hits"]:
        ids.append(hit["_source"]["django_id"])

    return Buyer.objects.filter(id__in=ids)

def search_by_clause(clause, limit=10):
    results = es.search(
        clause,
        size=limit,
    )
    ids = []
    for hit in results["hits"]["hits"]:
        ids.append(hit["_source"]["django_id"])

    return Buyer.objects.filter(id__in=ids)