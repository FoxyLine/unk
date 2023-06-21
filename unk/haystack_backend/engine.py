from haystack.backends.elasticsearch7_backend import (
    Elasticsearch7SearchEngine,
    FIELD_MAPPINGS,
)

FIELD_MAPPINGS["object"] = {"type": "object"}
FIELD_MAPPINGS["geo_shape"] = {"type": "geo_shape"}


class Engine(Elasticsearch7SearchEngine):
    ...
