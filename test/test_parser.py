from vocabulary.types import Field, Vocabulary, ValidTypesEnum
from test import TestCase
from vocabulary.voc_parser.functions import ParserFunctions
from vocabulary.voc_parser.types import KeyValuePair
from vocabulary.voc_parser.parser import Parser

INCOME_FIELD = Field(
    key="income", max_value=None, min_value=None, weight=None, data_type=None
)


def test_make_field():
    test_cases: list[TestCase] = [
        TestCase(input="[income]", expected_output=INCOME_FIELD),
        TestCase(input="   [income]", expected_output=INCOME_FIELD),
        TestCase(input="[   income]", expected_output=INCOME_FIELD),
        TestCase(input="[income    ]", expected_output=INCOME_FIELD),
        TestCase(input="[income]#testing", expected_output=INCOME_FIELD),
    ]

    for test_case in test_cases:
        result = ParserFunctions.make_field(test_case.input)
        assert type(result) == Field
        assert result.get_key() == INCOME_FIELD.get_key()


def test_make_key_value_pair():
    test_cases: list[TestCase] = [
        TestCase(
            input="type = 'float'",
            expected_output=KeyValuePair(key="type", value="float"),
        ),
        TestCase(
            input="type='float'",
            expected_output=KeyValuePair(key="type", value="float"),
        ),
        TestCase(
            input="type='float'#testing",
            expected_output=KeyValuePair(key="type", value="float"),
        ),
        TestCase(
            input='type="float"',
            expected_output=KeyValuePair(key="type", value="float"),
        ),
        TestCase(
            input="weight=1.0",
            expected_output=KeyValuePair(key="weight", value=1.0),
        ),
        TestCase(input="min=1", expected_output=KeyValuePair(key="min", value=1)),
    ]

    for test_case in test_cases:
        result = ParserFunctions.make_key_value_pair(test_case.input)
        assert type(result) == KeyValuePair
        assert result == test_case.expected_output


def test_parse_vocabulary():
    parser = Parser("./examples/credit_score.toml")
    result = parser.parse_from_file()
    expected_result = Vocabulary(
        key="credit_score",
        title="Credit Score",
        version="1.0",
        fields=[
            Field(
                key="income",
                data_type=ValidTypesEnum.Float,
                weight=2.0,
                min_value=0.0,
                max_value=None,
            ),
            Field(
                key="account_balance",
                data_type=ValidTypesEnum.Float,
                weight=1.5,
                min_value=None,
                max_value=None,
            ),
            Field(
                key="average_expenses",
                data_type=ValidTypesEnum.Float,
                weight=1.75,
                min_value=0.0,
                max_value=None,
            ),
            Field(
                key="age",
                data_type=ValidTypesEnum.Int,
                weight=None,
                min_value=0,
                max_value=None,
            ),
            Field(
                key="count_balance_in_dispo",
                data_type=ValidTypesEnum.Int,
                weight=2.5,
                min_value=0,
                max_value=None,
            ),
        ],
    )

    assert result.get_key() == expected_result.get_key()
    assert result.get_title() == expected_result.get_title()
    assert result.get_version() == expected_result.get_version()
    assert len(result.get_fields()) == len(expected_result.get_fields())
    expected_fields = expected_result.get_fields()
    for i, field in enumerate(result.get_fields()):
        assert field.get_key() == expected_fields[i].get_key()
        assert field.get_data_type() == expected_fields[i].get_data_type()
        assert field.get_weight() == expected_fields[i].get_weight()
        assert field.get_min_value() == expected_fields[i].get_min_value()
        assert field.get_max_value() == expected_fields[i].get_max_value()
