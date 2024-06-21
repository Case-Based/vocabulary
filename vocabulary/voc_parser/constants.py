import string

VALID_FIELD_ATTRIBUTES = frozenset(
    [
        "weight",
        "type",
        "data_type",  # Synonym for type
        "min_value",
        "min",  # Synonym for min_value
        "max_value",
        "max",  # Synonym for max_value
    ]
)
VALID_VOCABULARY_ATTRIBUTES = frozenset(["key", "title", "version"])
TYPES = frozenset([int, float, str])
VALID_CHARS = tuple(string.ascii_letters + string.digits + "-_")
