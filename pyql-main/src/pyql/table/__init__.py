from typing import TYPE_CHECKING, Dict, List, Tuple

from pyql.field import Field

from pyql.table.insert import Insert
from pyql.table.select import Select

if TYPE_CHECKING:
    from pyql.constraint import Constraint
    from pyql.data_type import DataType


class Table:
    def __init__(self, name: str):

        self.__name = name
        self.__fields: Dict[str, "Field"] = {}
        self.__cstrts: List["Constraint"] = []

    def __getattr__(self, __field_name: str) -> "Field":

        if __field_name in self.__fields:

            return self.__fields[__field_name]

        else:

            raise NameError(
                f"field name '{__field_name}' is not defined in table '{self.__name}'"
            )

    def __sql__(self) -> str:

        return self.__name

    def field(
        self,
        name: str,
        data_type: "DataType",
        not_null: bool = False,
        unique: bool = False,
    ) -> "Table":

        self.__fields[name] = Field(
            f"{self.__sql__()}.{name}", data_type, not_null, unique
        )

        return self

    def constraint(self, constraint: "Constraint") -> "Table":

        self.__cstrts.append(constraint)

        return self

    def create(self) -> str:

        fields = [f"{k} {v.__sql_create__()}" for k, v in self.__fields.items()]
        cstrts = [cstrt.__sql_create__() for cstrt in self.__cstrts]

        return f"CREATE TABLE IF NOT EXISTS {self.__name} ({', '.join(fields + cstrts)})"

    def drop(self) -> str:

        return f"DROP TABLE IF EXISTS {self.__name}"

    def select(self, fields: "Field" | Tuple["Field"]) -> "Select":

        return Select(fields, self)

    def insert(self, cols: str | Tuple[str]) -> "Insert":

        return Insert(self, cols)

    def delete(self):
        pass

    def update(self):
        pass
