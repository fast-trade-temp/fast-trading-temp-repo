class DataType:
    def __init__(self, data_type: str):

        self.data_type = data_type

    def __sql_create__(self) -> str:

        return f"{self.data_type}"


class CharacterVarying(DataType):
    def __init__(self, n: int):

        super().__init__(f"CHARACTER VARYING ({n})")


class Integer(DataType):
    def __init__(self):

        super().__init__("INTEGER")


class Numeric(DataType):
    def __init__(self, n: int, p: int):

        super().__init__(f"NUMERIC ({n}, {p})")


class Serial(DataType):
    def __init__(self):

        super().__init__("SERIAL")


class Timestamp(DataType):
    def __init__(self, n):

        super().__init__(f"TIMESTAMP ({n})")
