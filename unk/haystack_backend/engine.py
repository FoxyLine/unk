from haystack.backends.elasticsearch7_backend import (
    Elasticsearch7SearchEngine,
    FIELD_MAPPINGS,
)

FIELD_MAPPINGS["object"] = {"type": "object"}


class Engine(Elasticsearch7SearchEngine):
    ...
