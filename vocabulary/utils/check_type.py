from typing import Any


def check_type(value: Any, target_type: type):
    if not isinstance(value, target_type):
        raise TypeError(
            f"{value} with type {type(value)} must be of type {target_type}"
        )
