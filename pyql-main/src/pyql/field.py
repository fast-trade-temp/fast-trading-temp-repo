from typing import TYPE_CHECKING

from pyql.ops import Operand

if TYPE_CHECKING:
    from pyql.data_type import DataType


class Field(Operand):
    def __init__(
        self,
        name: str,
        data_type: "DataType",
        not_null: bool = False,
        unique: bool = False,
    ):

        super().__init__(name)
        self.data_type = data_type
        self.not_null = not_null
        self.unique = unique

    def __sql_create__(self) -> str:

        _t = [self.data_type.__sql_create__()]
        _t = _t + (["NOT NULL"] if self.not_null else [])
        _t = _t + (["UNIQUE"] if self.unique else [])

        return " ".join(_t)
