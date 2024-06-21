from vocabulary.voc_parser.types import KeyValuePair, ContextTypeEnum
from vocabulary.types import Field
from re import match, search
from vocabulary.utils.exception import ParsingError
from vocabulary.voc_parser.constants import (
    VALID_VOCABULARY_ATTRIBUTES,
    VALID_FIELD_ATTRIBUTES,
)
from typing import Optional, Union


class ParserFunctions:
    @staticmethod
    def check_pair(pair: KeyValuePair) -> (bool, Optional[ContextTypeEnum]):
        """
        With this method someone can check whether the provided key value pair can be used for the vocabulary.
        @param pair: KeyValuePair
        @return: boolean
        """
        if pair.key in VALID_VOCABULARY_ATTRIBUTES:
            return True, ContextTypeEnum.Vocabulary
        elif pair.key in VALID_FIELD_ATTRIBUTES:
            return True, ContextTypeEnum.Field
        return False, None

    @staticmethod
    def generate_vocabulary_key_from_file(file_path: str) -> str:
        """
        Generate a key for the vocabulary from the file path.
        The method will basically take the file name without file extension or path.
        @param file_path: string
        @return: string
        """
        split_list = file_path.split("/")
        last_val = split_list[len(split_list) - 1]
        split_point = last_val.split(".")
        return split_point[0] or "empty_key"

    @staticmethod
    def make_field(raw_value: str) -> Field:
        """
        With this method you can generate a field by providing the raw string value.
        It's part of the parsing algorithm.
        @param raw_value: string
        @return: Field
        """
        definition_pattern = r"^\s*\[{1}\s*[a-zA-Z0-9-_]+\s*\]{1}#?.*$"
        extract_key_pattern = r"\[{1}\s*([a-zA-Z0-9-_]+)\s*\]{1}"
        valid_definition = match(definition_pattern, raw_value)
        if not valid_definition:
            raise ParsingError("Invalid field definition")
        key = search(extract_key_pattern, raw_value).group(1)
        if not key:
            raise ParsingError("Invalid field definition")
        return Field(
            key=key, max_value=None, min_value=None, data_type=None, weight=None
        )

    @staticmethod
    def convert(raw_value: str) -> Union[int, float, str]:
        string_pattern = r'"([^"]*)"|\'([^\']*)\''
        int_pattern = r"[-+]?\d+"
        float_pattern = r"[-+]?\d*\.\d+([eE][-+]?\d+)?"

        string_match = match(string_pattern, raw_value)
        if string_match:
            return (
                string_match.group(1)
                if string_match.group(1) is not None
                else string_match.group(2)
            )

        float_match = match(float_pattern, raw_value)
        if float_match:
            return float(float_match.group(0))

        int_match = match(int_pattern, raw_value)
        if int_match:
            return int(int_match.group(0))
        raise ValueError("Invalid TOML line: Value type not supported")

    @staticmethod
    def make_key_value_pair(raw_value: str) -> KeyValuePair:
        key_pattern = r"^\s*([A-Za-z0-9_-]+)\s*=\s*"

        # Extract the key
        key_match = match(key_pattern, raw_value)
        if not key_match:
            raise ValueError("Invalid TOML line: Key not found")

        key = key_match.group(1)
        rest_of_line = raw_value[key_match.end() :].strip()

        value = ParserFunctions.convert(rest_of_line)
        return KeyValuePair(key=key, value=value)
