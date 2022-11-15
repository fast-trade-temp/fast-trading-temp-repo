from src.pgorm.datatype import DataType


class Condition:
    def __init__(self, condition: str):
        self.condition = condition

    def __repr__(self):
        return self.condition

    def __and__(self, other: "Condition") -> "Condition":
        return Condition(f"{self} AND {other}")

    def __or__(self, other: "Condition") -> "Condition":
        return Condition(f"{self} OR {other}")


class Field:
    def __init__(
        self, name: str, data_type: DataType, not_null: bool = False, default_val=None
    ):
        self.name = name
        self.data_type = data_type
        self.not_null = not_null
        self.default_val = default_val

    def __repr__(self) -> str:
        return f"{self.name} {self.data_type} {f'DEFAULT {self.data_type.to_sql(self.default_val)}' if self.default_val is not None else ''} {'NOT NULL' if self.not_null else 'NULL'}"

    def __lt__(self, other: str) -> Condition:
        return Condition(f"{self.name} < {other}")

    def __le__(self, other: str) -> Condition:
        return Condition(f"{self.name} <= {other}")

    def __eq__(self, other: str) -> Condition:
        return Condition(f"{self.name} = {other}")

    def __ne__(self, other: str) -> Condition:
        return Condition(f"{self.name} <> {other}")

    def __gt__(self, other: str) -> Condition:
        return Condition(f"{self.name} > {other}")

    def __ge__(self, other: str) -> Condition:
        return Condition(f"{self.name} >= {other}")

    def between(self, lower: str, upper: str) -> Condition:
        return Condition(f"{self.name} BETWEEN {lower} AND {upper}")
