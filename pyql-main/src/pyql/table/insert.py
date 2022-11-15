from typing import TYPE_CHECKING, List, Tuple

from pyql.utils import to_tuple

if TYPE_CHECKING:
    from pyql.table import Table
    from pyql.table.select import Select


class Insert:
    def __init__(self, table: "Table", cols: str | Tuple[str]):

        self.sql = [
            f"INSERT INTO {table.__sql__()} ({', '.join(to_tuple(cols))})"
        ]

    def __sql__(self) -> str:

        return " ".join(self.sql)

    def values(self, values: List[Tuple[str, ...]]):

        self.sql.append(
            f"VALUES ({'), ('.join([', '.join(value) for value in values])})"
        )

        return self

    def select(self, select: "Select"):

        self.sql.append(select.__sql__())

        return self
