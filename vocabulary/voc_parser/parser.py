from vocabulary.types import Vocabulary, ValidTypesEnum
from vocabulary.voc_parser.constants import VALID_CHARS
from vocabulary.voc_parser.functions import ParserFunctions
from vocabulary.voc_parser.types import ContextTypeEnum


class Parser:
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def parse_from_file(self) -> Vocabulary:
        """
        Read a vocabulary file and create an actual vocabulary object from it.
        This object can be used for the process of Case-Based Reasoning.
        @return:
        """
        file = open(self.__file_path, "r")
        lines = file.readlines()
        vocabulary = Vocabulary(
            key=ParserFunctions.generate_vocabulary_key_from_file(self.__file_path),
            version=None,
            title=None,
            fields=list()
        )
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Create field from raw value
            if line.startswith('['):
                vocabulary.append_field(ParserFunctions.make_field(line))
            # Create key-value pair from raw value
            elif line.startswith(VALID_CHARS):
                result = ParserFunctions.make_key_value_pair(line)
                fields = vocabulary.get_fields()
                if len(fields) < 1:
                    is_valid_key, key_context = ParserFunctions.check_pair(result)
                    if is_valid_key and key_context == ContextTypeEnum.Vocabulary:
                        if result.key == "title":
                            vocabulary.change_title(result.value)
                        elif result.key == "version":
                            vocabulary.change_version(result.value)
                        elif result.key == "key":
                            vocabulary.change_key(result.value)
                    continue
                current_field = fields[len(fields)-1]
                # check for valid key value pair
                is_valid_key, key_context = ParserFunctions.check_pair(result)
                if is_valid_key and key_context == ContextTypeEnum.Vocabulary:
                    if result.key == "title":
                        vocabulary.change_title(result.value)
                    elif result.key == "version":
                        vocabulary.change_version(result.value)
                    elif result.key == "key":
                        vocabulary.change_key(result.value)
                elif is_valid_key and key_context == ContextTypeEnum.Field:
                    if result.key == "weight":
                        current_field.change_weight(result.value)
                    elif result.key == "type" or result.key == "data_type":
                        if result.value == "int":
                            current_field.change_data_type(ValidTypesEnum.Int)
                        elif result.value == "float":
                            current_field.change_data_type(ValidTypesEnum.Float)
                    elif result.key == "min_value" or result.key == "min":
                        current_field.change_min_value(result.value)
                    elif result.key == "max_value" or result.key == "max":
                        current_field.change_max_value(result.value)

        return vocabulary
