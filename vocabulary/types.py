from vocabulary.utils.check_type import check_type
from typing import Optional, Union
from enum import Enum


class ValidTypesEnum(Enum):
    Int = 0
    Float = 1


class Field:
    def __init__(self, key: str, data_type: Optional[ValidTypesEnum], weight: Optional[float],
                 min_value: Optional[Union[int, float]], max_value: Optional[Union[int, float]]):
        self.__key = key
        self.__data_type = data_type or ValidTypesEnum.Int
        self.__weight = weight or 1.0
        if ((self.__data_type == ValidTypesEnum.Int and isinstance(min_value, int))
                or (self.__data_type == ValidTypesEnum.Float and isinstance(min_value, float))):
            self.__min_value = min_value
        else:
            self.__min_value = None
        if ((self.__data_type == ValidTypesEnum.Int and isinstance(max_value, int))
                or (self.__data_type == ValidTypesEnum.Float and isinstance(max_value, float))):
            self.__max_value = max_value
        else:
            self.__max_value = None

    def change_data_type(self, data_type: ValidTypesEnum):
        check_type(data_type, ValidTypesEnum)
        self.__data_type = data_type

    def change_key(self, key: str):
        check_type(key, str)
        self.__key = key

    def change_weight(self, weight: float):
        check_type(weight, float)
        self.__weight = weight

    def change_min_value(self, min_value: Union[int, float]):
        current_type: type = int
        if self.__data_type == ValidTypesEnum.Float:
            current_type = float
        check_type(min_value, current_type)
        self.__min_value = min_value

    def change_max_value(self, max_value: Union[int, float]):
        current_type: type = int
        if self.__data_type == ValidTypesEnum.Float:
            current_type = float
        check_type(max_value, current_type)
        self.__max_value = max_value

    def get_key(self) -> str:
        return self.__key

    def get_data_type(self) -> ValidTypesEnum:
        return self.__data_type

    def get_weight(self) -> float:
        return self.__weight

    def get_min_value(self) -> Optional[Union[int, float]]:
        return self.__min_value

    def get_max_value(self) -> Optional[Union[int, float]]:
        return self.__max_value


class Vocabulary:
    def __init__(self, key: str, title: Optional[str], version: Optional[str], fields: Optional[list[Field]]):
        self.__key = key
        self.__title = title or None
        self.__version = version or "1.0"
        self.__fields = fields or []

    def append_field(self, field: Field):
        check_type(field, Field)
        self.__fields.append(field)

    def remove_field(self, field_key: str):
        check_type(field_key, str)
        for field in self.__fields:
            if field.get_key() == field_key:
                self.__fields.remove(field)

    def find_field(self, field_key: str) -> Optional[Field]:
        check_type(field_key, str)
        for field in self.__fields:
            if field.get_key() == field_key:
                return field
        return None

    def change_key(self, key: str):
        check_type(key, str)
        self.__key = key

    def change_title(self, title: str):
        check_type(title, str)
        self.__title = title

    def change_version(self, version: str):
        check_type(version, str)
        self.__version = version

    def get_key(self) -> str:
        return self.__key

    def get_title(self) -> Optional[str]:
        return self.__title

    def get_version(self) -> Optional[str]:
        return self.__version

    def get_fields(self) -> list[Field]:
        return self.__fields
