from typing import Callable, Tuple

from src.pgorm.table import Table


class Constraint:
    def __call__(self, cls: Callable[..., Table]) -> Callable[..., Table]:
        def wrapper(*args, **kwargs) -> Table:
            table = cls(*args, **kwargs)
            table._constraints.append(self)
            return table

        return wrapper


class ForeignKey(Constraint):
    def __init__(
        self, field_names: Tuple[str], ref_table: str, ref_field_names: Tuple[str]
    ):
        self.field_names = field_names
        self.ref_table = ref_table
        self.ref_field_names = ref_field_names

    def __repr__(self) -> str:
        fields = ", ".join(self.field_names)
        ref_fields = ", ".join(self.ref_field_names)
        return f"FOREIGN KEY ({fields}) REFERENCES {self.ref_table} ({ref_fields})"


class PrimaryKey(Constraint):
    def __init__(self, field_names: Tuple[str]):
        self.field_names = field_names

    def __repr__(self) -> str:
        return f"PRIMARY KEY ({', '.join(self.field_names)})"


class Unique(Constraint):
    def __init__(self, field_names: Tuple[str]):
        self.field_names = field_names

    def __repr__(self) -> str:
        return f"UNIQUE ({', '.join(self.field_names)})"
