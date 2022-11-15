from typing import Tuple

from pyql.utils import to_tuple


class Constraint:
    def __sql_create__(self) -> str:
        raise NotImplementedError()


class ForeignKey(Constraint):
    def __init__(
        self,
        cols: str | Tuple[str],
        ref_table: str,
        ref_cols: str | Tuple[str],
    ):

        self.cols = to_tuple(cols)
        self.ref_table = ref_table
        self.ref_cols = to_tuple(ref_cols)

    def __sql_create__(self) -> str:

        fields = ", ".join(self.cols)
        ref_fields = ", ".join(self.ref_cols)

        return (
            f"FOREIGN KEY ({fields}) REFERENCES {self.ref_table} ({ref_fields})"
        )


class PrimaryKey(Constraint):
    def __init__(self, cols: str | Tuple[str]):

        self.cols = to_tuple(cols)

    def __sql_create__(self) -> str:

        return f"PRIMARY KEY ({', '.join(self.cols)})"


class Unique(Constraint):
    def __init__(self, cols: str | Tuple[str]):

        self.cols = to_tuple(cols)

    def __sql_create__(self) -> str:

        return f"UNIQUE ({', '.join(self.cols)})"
