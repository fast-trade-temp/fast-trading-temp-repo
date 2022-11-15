from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.pgorm.table import Table
    from src.pgorm.table import Select


class Insert:
    def __init__(
        self,
        table: "Table",
        columns: List[str],
        values: List[str] = None,
        select: "Select" = None,
    ):
        if values is not None:
            self.stmt = f"INSERT INTO {table}({', '.join(columns)}) VALUES ({', '.join(values)})"
        elif select is not None:
            self.stmt = f"INSERT INTO {table}({', '.join(columns)}) {select}"

    def conflict_do_nothing(self, field=None) -> "Insert":
        self.stmt += (
            f" ON CONFLICT {'' if field is None else f'({field.name})'} DO NOTHING"
        )
        return self

    def returning(self, field=None) -> "Insert":
        self.stmt += f" RETURNING {'*' if field is None else field.name}"
        return self

    def __repr__(self):
        return self.stmt
