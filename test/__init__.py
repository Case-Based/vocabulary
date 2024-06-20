from dataclasses import dataclass
from typing import Any


@dataclass
class TestCase:
    input: Any
    expected_output: Any
