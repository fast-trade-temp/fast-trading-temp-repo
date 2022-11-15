from datetime import datetime
from typing import Any


class DataType:
    def __init__(self, type: str):
        self.type = type

    def __repr__(self) -> str:
        return f"{self.type}"

    def python_type(self) -> Any:
        raise NotImplementedError

    def to_sql(self, value):
        return f"{value}"


class CharacterVarying(DataType):
    def __init__(self, n: int):
        super().__init__(f"CHARACTER VARYING ({n})")

    def python_type(self):
        return str

    def to_sql(self, value):
        return f"'{value}'"


class Integer(DataType):
    def __init__(self):
        super().__init__("INTEGER")

    def python_type(self):
        return int


class Numeric(DataType):
    def __init__(self, n: int, p: int):
        super().__init__(f"NUMERIC ({n}, {p})")

    def python_type(self):
        return float


class Serial(DataType):
    def __init__(self):
        super().__init__("SERIAL")

    def python_type(self):
        return int


class Timestamp(DataType):
    def __init__(self, n):
        super().__init__(f"TIMESTAMP ({n})")

    def python_type(self):
        return datetime

    def to_sql(self, value):
        return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"


class Boolean(DataType):
    def __init__(self):
        super().__init__("BOOLEAN")

    def python_type(self):
        return bool
