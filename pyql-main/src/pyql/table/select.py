from typing import TYPE_CHECKING, Tuple

from pyql.utils import to_tuple

if TYPE_CHECKING:
    from pyql.field import Field
    from pyql.ops import Operation
    from pyql.table import Table


class Select:
    def __init__(self, fields: "Field" | Tuple["Field"], table: "Table"):

        fields = [field.__sql__() for field in to_tuple(fields)]
        self.sql = [f"SELECT {', '.join(fields)} FROM {table.__sql__()}"]

    def __sql__(self) -> str:

        return " ".join(self.sql)

    def where(self, condition: "Operation") -> "Select":

        self.sql.append(f"WHERE {condition.__sql__()}")

        return self

    def inner_join(self, table: "Table", on: "Operation"):

        self.sql.append(f"JOIN {table.__sql__()} ON {on.__sql__()}")

        return self

    def left_join(self, table: "Table", on: "Operation"):

        self.sql.append(f"LEFT JOIN {table.__sql__()} ON {on.__sql__()}")

        return self

    def right_join(self, table: "Table", on: "Operation"):

        self.sql.append(f"RIGHT JOIN {table.__sql__()} ON {on.__sql__()}")

        return self

    def full_join(self, table: "Table", on: "Operation"):

        self.sql.append(f"FULL JOIN {table.__sql__()} ON {on.__sql__()}")

        return self
