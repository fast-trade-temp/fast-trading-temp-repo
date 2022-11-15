from typing import TYPE_CHECKING

from src.pgorm.field import Condition
from src.pgorm.field import Field

import copy


if TYPE_CHECKING:
    from src.pgorm.table import Table


class Select:

    selector_fields = []

    def __init__(self, table: "Table", distinct, *fields):
        self.selector_fields = [field.name for field in fields]
        self.distinct = distinct
        self.table = copy.deepcopy(table)
        self.stmts = ["SELECT {distinct} {selector} FROM {table}"]

    def __repr__(self) -> str:
        selector = "*" if not self.selector_fields else ", ".join(self.selector_fields)

        statement = self.stmts[0].format(
            distinct="DISTINCT" if self.distinct else "",
            selector=selector,
            table=self.table,
        )

        return statement + " " + " ".join(self.stmts[1:])

    def where(self, condition: Condition) -> "Select":
        self.stmts.append(f"WHERE {condition}")
        return self

    def inner_join(
        self, t_field: Field, o_select: "Select", alias: str, o_field: Field
    ) -> "Select":
        self.stmts.append(
            f"INNER JOIN ({o_select}) {alias} ON {self.table}.{t_field.name} = {alias}.{o_field.name}"
        )
        return self

    def inner_join_table(
        self, t_field: Field, o_table: "Table", o_field: Field, *add_fields
    ) -> "Select":
        self.stmts.append(
            f"INNER JOIN {o_table} ON {self.table}.{t_field.name} = {o_table}.{o_field.name}"
        )
        self.selector_fields.extend([f"{o_table}.{field.name}" for field in add_fields])
        return self
